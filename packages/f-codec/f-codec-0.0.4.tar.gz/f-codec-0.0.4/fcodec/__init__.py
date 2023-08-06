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
'''
"""

import codecs
from encodings import utf_8

CODEC_NAME  = 'f'

#   ---------------------------------------------------------------------------
F_STR_BEGIN   = "f'''"
F_STR_END     = "'''"
F_STR_HEAD    = "print("
F_STR_TAIL    = ", end='')"
F_STR_LF_TAIL = ")"

#   ---------------------------------------------------------------------------
def f_string_decode(input, errors='strict', final=False):
    """
    -----------------------------------
    f'''string
    '''
    ↓
    print(f'''string\\
    ''', end='')
    -----------------------------------
    f'''
    string
    '''
    ↓
    print(f'''
    string\\
    ''', end='')
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
            pos = ln.index(F_STR_BEGIN)
            if saml.endswith(F_STR_END, len(F_STR_BEGIN)):
#               -- a single line string
#                  interpret an empty string as a line break
                tail = F_STR_LF_TAIL if saml == F_STR_BEGIN + F_STR_END else F_STR_TAIL
                result += ln[ :pos] + F_STR_HEAD + ln[pos: ] + tail + '\n'
            else:
#               -- postpone a line break adding
                result += ln[ :pos] + F_STR_HEAD + ln[pos: ]
                begun = True
        elif begun:
            if saml.startswith(F_STR_END):
                pos = ln.index(F_STR_END) + len(F_STR_END)
#               -- escape the latest line break
                result += '\n' if result.rstrip(' \t').endswith('\\') else '\\\n'
                result += ln[ :pos] + F_STR_TAIL + ln[pos: ] + '\n'
                begun = False
            else:
                result += '\n' + ln
        else:
            result += ln + '\n'
    return result, bytesencoded

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
