#!/usr/bin/env python3

# Python 'f' Codec
# Wrap lonesome f-strings in `print()`.

"""
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

f'''
Godspeed!
''' > ' ' * 8
"""

import codecs
from encodings import utf_8

CODEC_NAME  = 'f'

#   ---------------------------------------------------------------------------
F_STR_BEGIN    = "f'''"
F_STR_END      = "'''"

F_STR_HEAD     = "print((lambda x: x.join("
F_STR_TAIL     = ".splitlines(True)))({}), end='')"
F_STR_INDENT   = ">"
F_STR_HEAD_1   = "print("
F_STR_TAIL_1   = ", end='')"
F_STR_TAIL_1LF = ")"

#   ---------------------------------------------------------------------------
def f_string_decode(input, errors='strict', final=False):
    """
    -----------------------------------
    f'''string
    '''
    ↓
    print((lambda x: x.join(f'''string\\
    '''.splitlines(True)))(''), end='')
    -----------------------------------
    f'''
    string
    ''' > indent
    ↓
    print((lambda x: x.join(f'''
    string\\
    '''.splitlines(True)))(indent), end='')
    -----------------------------------
    f''''''
    ↓
    print(f'''''')
    -----------------------------------
    """
    data, bytesencoded = codecs.utf_8_decode(input, errors, final)
    result = ''
    begun = False
    for ln in data.splitlines():
        saml = ln.strip()
        if not begun and saml.startswith(F_STR_BEGIN):
#           -- f'''
            pos = ln.index(F_STR_BEGIN)
            if saml.endswith(F_STR_END, len(F_STR_BEGIN)):
#               -- a single line string
#                  interpret an empty string as a line break
                tail = F_STR_TAIL_1LF if saml == F_STR_BEGIN + F_STR_END else F_STR_TAIL_1
                result += ln[ :pos] + F_STR_HEAD_1 + ln[pos: ] + tail + '\n'
            else:
#               -- postpone a line break adding
                result += ln[ :pos] + F_STR_HEAD + ln[pos: ]
                begun = True
        elif begun:
            if saml.startswith(F_STR_END):
#               -- '''
                pos = ln.index(F_STR_END) + len(F_STR_END)
#               -- escape the latest line break
                result += '\n' if result.rstrip(' \t').endswith('\\') else '\\\n'
                tail = ln[pos: ]
                indent = "''"
                if F_STR_INDENT in tail:
                    pos_indent = tail.index(F_STR_INDENT)
                    indent = tail[pos_indent + len(F_STR_INDENT): ].strip()
                    tail = tail[ :pos_indent]
                result += ln[ :pos] + F_STR_TAIL.format(indent) + tail + '\n'
                begun = False
            else:
                result += '\n' + ln
        else:
            result += ln + '\n'
    return result, bytesencoded

#   ---------------------------------------------------------------------------
def indent(text, indentation=None):
    return indentation.join(text.splitlines(True)) if indentation else text

#   ---------------------------------------------------------------------------
def decode(input, errors='strict'):
    return f_string_decode(input, errors, True)

#   ---------------------------------------------------------------------------
class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, input, errors, final):
        return f_string_decode(input, errors, final)

#   ---------------------------------------------------------------------------
class StreamReader(codecs.StreamReader):
    def decode(self, input, errors='strict'):
        return f_string_decode(input, errors, True)

#   ---------------------------------------------------------------------------
def search_function(coding):
    if coding.lower() != CODEC_NAME:
        return None

    return codecs.CodecInfo(
        name=CODEC_NAME,
        encode=utf_8.encode,
        decode=decode,
        incrementalencoder=utf_8.IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=utf_8.StreamWriter,
    )

#   ---------------------------------------------------------------------------
codecs.register(search_function)

if __name__ == '__main__':
    code =__doc__.encode().decode('f')
    print(code)
    exec(code)
