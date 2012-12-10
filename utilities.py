# coding: latin-1

import re
import unicodedata
import os
import traceback

def change(dic, obj):
    if isinstance(obj, list):
        for n, i in enumerate(obj):
            for k, v in dic.items():
                obj[n] = i.replace(k, v)
                i = obj[n]
    else:
        if isinstance(obj, str):
            for k, v in dic.items():
                obj = obj.replace(k, v)
    return obj

dra = {'\xc3\x81':'�', '\xc3\x80':'�', '\xc3\x82':'�', '\xc3\x83':'�',
       '\xc3\x84':'�', '\xc3\x89':'�', '\xc3\x88':'�', '\xc3\x8a':'�',
       '\xc3\x8b':'�', '\xc3\x8d':'�', '\xc3\x8c':'�', '\xc3\x8e':'�',
       '\xc3\x8f':'�', '\xc3\x93':'�', '\xc3\x92':'�', '\xc3\x94':'�',
       '\xc3\x95':'�', '\xc3\x96':'�', '\xc3\x9a':'�', '\xc3\x99':'�',
       '\xc3\x9b':'�', '\xc3\x9c':'�', '\xc3\x87':'�', '\xc3\xa1':'�',
       '\xc3\xa0':'�', '\xc3\xa2':'�', '\xc3\xa3':'�', '\xc3\xa4':'�',
       '\xc3\xa9':'�', '\xc3\xa8':'�', '\xc3\xaa':'�', '\xc3\xab':'�',
       '\xc3\xad':'�', '\xc3\xac':'�', '\xc3\xae':'�', '\xc3\xaf':'�',
       '\xc3\xb3':'�', '\xc3\xb2':'�', '\xc3\xb4':'�', '\xc3\xb5':'�',
       '\xc3\xb6':'�', '\xc3\xba':'�', '\xc3\xb9':'�', '\xc3\xbb':'�',
       '\xc3\xbc':'�', '\xc3\xa7':'�'}

def nUni2Uni(txt):
    return change(dra, txt)

def remover_acentos(txt, codif='latin-1'):
    return unicodedata.normalize('NFKD', nUni2Uni(txt).decode(codif)).encode('ASCII','ignore')

wordsRe = re.compile(r'\w+', re.UNICODE)

def words(args):
    return wordsRe.findall(args)

def word(texto, idx):
    return words(texto)[idx]

def txtAbrev(txt, lgt):
    txt=remover_acentos(txt)
    for w in words(txt):
        if len(txt) <= lgt:
            break
        if w+' '  in txt:
            txt=txt.replace(w+' ',w[0:3]+'.')
        else:
            txt=txt.replace(w,w[0:3]+'.')
    return txt[0:lgt]

def insAster72(txt):
    ts=''
    tl=txt.split('\n')
    for l in tl:
         if l[6:7] == '*':
             if len(l) < 72:
                 l+=(' '*(71-len(l))+'*')
         ts+=l+'\n'
    return ts

def Capitalize(string, N=2):

    if  not string:
        return ''

    words  = string.split()
    result = words[0].capitalize() if words else ''

    if  words: del(words[0])

    for word in words:
        if len(word) > N:
            if word[1] == "'":
                result += ' ' + word[:2].lower() + word[2:].capitalize()
            else:
                result += ' ' + word.capitalize()
        else:
            result += ' ' + word

    return result


def remarks(op, texto=None):
    if  not texto:
        texto = 'RSRC'
    if  op == 'D':
        return texto + '-D*'
    if  op == 'U':
        return texto + '-U '
    if  op == 'I':
        return texto + '-I '
    if  op == 'R':
        return texto + '-R*'
    if  op == 'V':
        return texto + '-V '
    if  op == 'W':
        return texto + '-W@'
    if  op == '@':
        return texto + '-??'

def remarksInitial(texto, arquivo):
    if  type(arquivo) is file:
        arquivo.write('{0}{1}\n'.format(remarks('R'),'%'*65))
        for t in texto:
            arquivo.write('{0}{1}{2:45}{1}\n'.format(remarks('R'),'%'*10, t))
        arquivo.write('{0}{1}\n'.format(remarks('R'),'%'*65))
