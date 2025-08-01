'''
This script parses an existing caps file, and the boolean, numeric, and string capabilities. 
'''

import json

def parse_caps_file():
    with open('caps', 'r') as f: content = f.readlines()

    keep = []
    for line in content:
        # if "%%-STOP-HERE-%%" in line:
        #     break
        if not line.startswith('#'):
            keep.append([o for o in line.split('\t') if o != ''])
    
    keep_bool = [
        elt[1] for elt in keep if any(o == 'bool' for o in elt)
    ]

    keep_num = [
        elt[1] for elt in keep if any(o == 'num' for o in elt)
    ]


    keep_string = [
        elt[1] for elt in keep if any(o == 'str' for o in elt)
    ]
    return {'bool': keep_bool, 'num': keep_num, 'string': keep_string}


if __name__ == '__main__':
    caps = parse_caps_file()
    with open('caps.json', 'w') as f:
        json.dump(caps, f)
