import json
import os
import sys
import random
import datetime
import pprint as pp


def update_control(control, count, random_choice):
    cat = str(random_choice[0] + 1)
    index = random_choice[1]
    if control.get(cat, None):

        if control[cat].get(str(index)):
            control[cat][index]['counter'] += count
            control[cat][index]['date'] = datetime.datetime.now().isoformat()
        else:
            control[cat][index] = dict()
            control[cat][index]['counter'] = count
            control[cat][index]['date'] = datetime.datetime.now().isoformat()

    else:
        control[cat] = dict()
        control[cat][index] = dict()
        control[cat][index]['counter'] = count
        control[cat][index]['date'] = datetime.datetime.now().isoformat()

    return control


def check_finishing(control):
    with open(os.path.join('data', '{}.json'.format(directory)), 'w') as file:
        json.dump(control, file)
    while True:
        close = input('Soll das Training beendet werden (j/n)?')
        if close in ['j', 'n']:
            break
    return close


def get_modes():
    modes_list = [#'Fange mit neuen Fragen an',
                  'Gelernt bei 3 richtigen Antworten',
                  'Gelernt bei 1 richtigen Antwort',
                  #'Erst unbekannte, dann nach datum und Anzahl Richtige'
                  ]

    print('Modus:')
    for x, mod in enumerate(modes_list):
        print(x + 1, '\t', mod)

    while True:
        modes = input('Wähle den Übungsmodus:')
        if modes.isdigit():
            if int(modes) in list(range(1, len(modes_list) + 1)):
                break
    return modes


def check_status(question, control, success_count):

    if control.get(str(question[0] + 1), {}).get(question[1]):
        # success_count
        if control.get(str(question[0] + 1), {})[question[1]]['counter'] >= success_count:
            return True
        # success_count constrain not met
        else:
            return False
    # unknown question
    else:
        return False


if __name__ == '__main__':
    path = os.path.join('data', 'Jagdschein MV')
    user = input('enter your name:')

    directory = 'control_{}'.format(user)
    if os.path.isfile(os.path.join('data', '{}.json'.format(directory))):
        with open(os.path.join('data', '{}.json'.format(directory)), 'r') as file:
            control = json.load(file)
    else:
        control = dict()

    with open(os.path.join(path, 'jagdschein.json'), 'r') as file:
        data = json.load(file)

    # select subject or all
    subjects = list(data.keys())
    for n, s in enumerate(subjects):
        print(n + 1, '\t', data[s]['info'])
    print('Enter\t', 'Alle Fächer')
    while True:
        subject_id = input('Wählen: ')
        if subject_id is None:
            break
        elif subject_id in str(list(range(1, n + 2))):
            break
    modes = get_modes()
    questions = []
    if subject_id is '':
        # all subjects
        for n, s in enumerate(subjects):
            print(s)
            for q in data[subjects[n]].keys():
                if 'info' not in q:
                    questions.append((n, q))
    else:
        # selected subject
        for q in list(data[subjects[int(subject_id) - 1]].keys()):
            if 'info' not in q:
                questions.append((int(subject_id) - 1, q))

    print('Anzahl Fragen:', len(questions))

    print('\nZum Beenden und/oder Speichern bitte "e" eingeben!!!')
    while True:
        random_choice = random.choice(questions)

        if modes == '1':
            success_count = 3
        elif modes == '2':
            success_count = 1

        if check_status(random_choice, control, success_count):
            print(control.get(str(random_choice[0] + 1), {}).get(random_choice[1])['counter'])

            if control.get(str(random_choice[0] + 1), {}).get(random_choice[1])['counter'] == success_count:
                questions.remove(random_choice)

        if len(questions) is 0:
            print('Alle Fragen gelernt')
            break

        answer = ''
        if data[subjects[random_choice[0]]][random_choice[1]]['type'] == 'text':
            print('\nFrage {}-{}:\n{}\n'.format(random_choice[0]+1, random_choice[1], data[subjects[random_choice[0]]][random_choice[1]]['question']))
            while True:
                answer = input('\r')
                break
            print('\r\rAntwort:\n{}\n'.format(data[subjects[random_choice[0]]][random_choice[1]]['answer']))

            while True:
                answer = input('Richtig(r), Falsch(f)')
                if answer in ['r', 'f', 'e']:
                    break

            if answer == 'r':
                control = update_control(control, 1, random_choice)
            elif answer == 'f':
                control = update_control(control, 0, random_choice)

            if answer is 'e':
                close = check_finishing(control)
                if close == 'j':
                    break

        elif data[subjects[random_choice[0]]][random_choice[1]]['type'] == 'multiple_choice':
            print('\nFrage {}-{}:\n{}\n'.format(random_choice[0]+1, random_choice[1], data[subjects[random_choice[0]]][random_choice[1]]['question']))
            for n, c in enumerate(data[subjects[random_choice[0]]][random_choice[1]]['answer']['choice']):
                print('\t', n + 1, c)
            while True:
                answer = input('Antwort:')
                if answer in ['e'] or answer.isdigit():
                    break
            if answer is 'e':
                close = check_finishing(control)
                if close == 'j':
                    break

            elif int(answer) - 1 in data[subjects[random_choice[0]]][random_choice[1]]['answer']['correct']:
                print('Richtig')
                control = update_control(control, 1, random_choice)

            else:
                print('Falsch', [x + 1 for x in data[subjects[random_choice[0]]][random_choice[1]]['answer']['correct']])

                control = update_control(control, 0, random_choice)

    with open(os.path.join('data', '{}.json'.format(directory)), 'w') as file:
        json.dump(control, file)

    print('Das Training wird beendet, Aktueller Stand wird gespeichert!')





