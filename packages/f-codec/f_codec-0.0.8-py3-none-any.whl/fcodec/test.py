# -*- coding: f -*-

import sys

f'''
Python
'''
if sys.version_info > (3, 0):
    f''' {sys.version}
'''
else:
    f'''
The sunset for Python 2 has passed.
'''

f''''''

def dictionary(inst, depth=0):
    ಠ_ಠ = '    ' * depth

    f''' {{
'''

    for name, val in inst.items():
        if isinstance(val, dict):
            f'''
    {name} =
''' > ಠ_ಠ
            dictionary(val, depth + 1)
        else:
            f'''
    {name} = {val},
''' > ಠ_ಠ

    f'''
}}
''' > ಠ_ಠ

decl = {
    'a': 1,
    'b': 2,
    'c': { 'a': 3, 'b': 4 },
    'd': { 'a': 5, 'b': { 'a': 6, 'b': 7 }, 'c': 8 },
    'e': 9
}

f'''
decl =
'''
dictionary(decl)
