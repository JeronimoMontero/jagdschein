import json
import os
import re
import pprint as pp
os.path.join('data')

if __name__ == '__main__':
    states = os.listdir(os.path.join('data'))
    for n, s in enumerate(states):
        print(n + 1, s)
    state = states[int(input('select state: ')) - 1]
    path = os.path.join('data', state)
    
    data_parsed = dict()
    for subject in sorted(os.listdir(path)):
        if 'Fach' in subject:
            if os.path.isfile(os.path.join(path, subject)):
                with open(os.path.join(path, subject), 'r') as file:
                    print(subject)
                    data = file.read()
                topic = subject.replace('.txt', '')
                data_parsed[topic] = dict()
                data_parsed[topic]['info'] = data.split('\n####\n')[0].strip()

                index_list = re.findall('\d\d*\.\s*\t', data.split('\n####\n')[1])
                content_list = list(filter(None, re.split('\d\d*\.\s*\t', data.split('\n####\n')[1])))
                for index in index_list:
                    index = int(index.strip()[:-1])
                    #raw = list(filter(None, re.split('(.*?[!?\.:]+)', content_list[index - 1], flags=re.DOTALL)))
                    raw = list(filter(None, re.split('\n', content_list[index - 1], flags=re.DOTALL)))
                    data_parsed[topic][index] = {}
                    data_parsed[topic][index]['question'] = raw[0].replace('\n', '').replace('\t', '').strip()
                    if ' x' in ''.join(raw[1:]).lower():
                        content = list(filter(None, re.split('[abc]\)', ''.join(raw[1:]), flags=re.DOTALL)))[1:]
                        data_parsed[topic][index]['type'] = 'multiple_choice'
                        data_parsed[topic][index]['answer'] = {}
                        data_parsed[topic][index]['answer']['correct'] = []  # right answers
                        data_parsed[topic][index]['answer']['choice'] = []  # possible answers

                        for number, answer in enumerate(content):
                            if answer.strip()[-1] in ['x', 'X']:
                                answer = answer.replace(' x', '').replace(' X', '')
                                data_parsed[topic][index]['answer']['correct'].append(number)
                            data_parsed[topic][index]['answer']['choice'].append(answer.strip())
                    else:
                        data_parsed[topic][index]['type'] = 'text'
                        data_parsed[topic][index]['answer'] = ''.join(raw[1:]).replace('\n', '').replace('\t', '').strip()

        with open(os.path.join(path, 'jagdschein.json'), 'w') as outfile:
            json.dump(data_parsed, outfile)
