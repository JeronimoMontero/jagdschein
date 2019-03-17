import json
import os
import random

if __name__ == '__main__':
    # select region
    states = os.listdir(os.path.join('data'))
    # for n, s in enumerate(states):
    #    print(n + 1, s)
    # state = states[int(input('select state: ')) - 1]

    path = os.path.join('data', states[0])

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
                    questions.append((n + 1, q))
    else:
        # selected subject
        for q in list(data[subjects[int(subject_id) - 1]].keys()):
            if 'info' not in q:
                questions.append((int(subject_id) - 1, q))

    print('Anzahl Fragen:', len(questions))

    print('\nZum Beenden bitte "e" eingeben!!!')
    while True:
        random_choice = random.choice(questions)
        # text
        answer = ''
        if data[subjects[random_choice[0]]][random_choice[1]]['type'] == 'text':
            print('\nFrage {}:\n{}\n'.format(random_choice[1], data[subjects[random_choice[0]]][random_choice[1]]['question']))
            while True:
                answer = input('Richtig(r), Falsch(f)')
                if answer in ['r', 'f', 'e']:
                    break
            if answer == 'e':
                while True:
                    close = input('Soll das Training beendet werden (j/n)?')
                    if close in ['j', 'n']:
                        break
                if close == 'j':
                    break
            else:
                print('Antwort:\n{}\n'.format(data[subjects[random_choice[0]]][random_choice[1]]['answer']))
        # multiple
        elif data[subjects[random_choice[0]]][random_choice[1]]['type'] == 'multiple_choice':
            print('\nFrage {}:\n{}'.format(random_choice[1], data[subjects[random_choice[0]]][random_choice[1]]['question']))
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
            else:
                print('Falsch', data[subjects[random_choice[0]]][random_choice[1]]['answer']['correct'])

    print('Das Training wird beendet, Aktueller Stand wird gespeichert!')





