import io
import json

def transform(ein):
    '''
    This program takes as input an txt file generated with Hyperspy in form of a hyperspy tree. it converts it to a json file.
    '''
    f2 = io.StringIO()
    with open(ein) as f1:
        i = 0 #test whether next line is part of a aubgroup
        b = False #True for the first line of a subgroup to avoid the comma
        c = True #True only for the very first line to avoid the comma
        count = 1
        #aus = ein[:-4]
        #aus = aus + 't.json'

        f2.write('{\n')
        for line in f1:
            line = line.rstrip()
            if(line != ''):
                if(line[0] != '├' and line[0] != '└' and line[0] != '│'):
                    if(i == 1):
                        f2.write(',\n    ')
                        f2.write('    "additionalInformation' + str(count) + '": "' + line + '"')
                    else:
                        f2.write(',\n    "additionalInformation' + str(count) + '": "' + line + '"')
                    count += 1
                else:
                    if(i == 1 and line[0] == '│'):
                        if(b):
                            f2.write('\n    ')
                            b = False
                        else:
                            f2.write(',\n    ')
                    if(i == 1 and (line[0] == '├' or line[0] == '└')):
                        f2.write('\n    }')
                        i = 0
                    temp = line.lstrip('├ ─ └ │')
                    #print(temp)
                    pos = temp.find('=')
                    if(pos==-1):
                        if(c):
                            f2.write('    "' + temp + '": {')
                        else:
                            f2.write(',\n    "' + temp + '": {')
                        i = 1
                        b = True
                    else:
                        temp1 = temp[:pos-1]
                        temp2 = temp[pos+2:]
                        if(i==1):
                            f2.write('    "' + temp1 + '": "' + temp2 + '"')
                        else:
                            if(c):
                                f2.write('    "' + temp1 + '": "' + temp2 + '"')
                            else:
                                f2.write(',\n    "' + temp1 + '": "' + temp2 + '"')
                c = False
        f2.write('\n}\n')

    return json.loads(f2.getvalue())
