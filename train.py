import json
import os
import sys
import random
import datetime
import pprint as pp

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
        print(n + 1, '\t\t', data[s]['info'])
    print('Enter\t', 'Alle Fächer')
    while True:
        subject_id = input('Wählen: ')
        if subject_id is None:
            break
        elif subject_id in str(list(range(1, n + 2))):
            break

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

    print('\nZum Beenden bitte "e" eingeben!!!')
    while True:
        random_choice = random.choice(questions)
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
                    if control.get(random_choice[0]):
                        if control[random_choice[0]].get(random_choice[1]):
                            control[random_choice[0]][random_choice[1]]['counter'] += 1
                            control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()
                        else:
                            control[random_choice[0]] = dict()
                            control[random_choice[0]][random_choice[1]] = dict()
                            control[random_choice[0]][random_choice[1]]['counter'] = 0
                            control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

                    else:
                        control[random_choice[0]] = dict()
                        control[random_choice[0]][random_choice[1]] = dict()
                        control[random_choice[0]][random_choice[1]]['counter'] = 1
                        control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

                elif answer == 'f':
                    if control.get(random_choice[0]):
                        if control[random_choice[0]].get(random_choice[1]):
                            control[random_choice[0]][random_choice[1]]['counter'] = 0
                            control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()
                        else:
                            control[random_choice[0]] = dict()
                            control[random_choice[0]][random_choice[1]] = dict()
                            control[random_choice[0]][random_choice[1]]['counter'] = 0
                            control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

                    else:
                        control[random_choice[0]] = dict()
                        control[random_choice[0]][random_choice[1]] = dict()
                        control[random_choice[0]][random_choice[1]]['counter'] = 0
                        control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

            if answer == 'e':
                while True:
                    close = input('Soll das Training beendet werden (j/n)?')
                    if close in ['j', 'n']:
                        break
                if close == 'j':
                    break
        # multiple
        elif data[subjects[random_choice[0]]][random_choice[1]]['type'] == 'multiple_choice':
            print('\nFrage {}-{}:\n{}\n'.format(random_choice[0]+1, random_choice[1], data[subjects[random_choice[0]]][random_choice[1]]['question']))
            for n, c in enumerate(data[subjects[random_choice[0]]][random_choice[1]]['answer']['choice']):
                print('\t', n + 1, c)
            while True:
                answer = input('Antwort:')
                if answer in ['e'] or answer.isdigit():
                    break
            if answer is 'e':
                while True:
                    close = input('Soll das Training beendet werden (j/n)?')
                    if close in ['j', 'n']:
                        break
                if close == 'j':
                    break

            elif int(answer) - 1 in data[subjects[random_choice[0]]][random_choice[1]]['answer']['correct']:
                print('Richtig')
                if control.get(random_choice[0]):
                    if control[random_choice[0]].get(random_choice[1]):
                        control[random_choice[0]][random_choice[1]]['counter'] += 1
                        control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()
                    else:
                        control[random_choice[0]] = dict()
                        control[random_choice[0]][random_choice[1]] = dict()
                        control[random_choice[0]][random_choice[1]]['counter'] = 0
                        control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

                else:
                    control[random_choice[0]] = dict()
                    control[random_choice[0]][random_choice[1]] = dict()
                    control[random_choice[0]][random_choice[1]]['counter'] = 1
                    control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

            else:
                print('Falsch', data[subjects[random_choice[0]]][random_choice[1]]['answer']['correct'])

                if control.get(random_choice[0]):
                    if control[random_choice[0]].get(random_choice[1]):
                        control[random_choice[0]][random_choice[1]]['counter'] = 0
                        control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()
                    else:
                        control[random_choice[0]] = dict()
                        control[random_choice[0]][random_choice[1]] = dict()
                        control[random_choice[0]][random_choice[1]]['counter'] = 0
                        control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

                else:
                    control[random_choice[0]] = dict()
                    control[random_choice[0]][random_choice[1]] = dict()
                    control[random_choice[0]][random_choice[1]]['counter'] = 0
                    control[random_choice[0]][random_choice[1]]['date'] = datetime.datetime.now().isoformat()

    with open(os.path.join('data', '{}.json'.format(directory)), 'w') as file:
        json.dump(control, file)

    print('Das Training wird beendet, Aktueller Stand wird gespeichert!')





