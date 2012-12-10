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

dra = {'\xc3\x81':'Á', '\xc3\x80':'À', '\xc3\x82':'Â', '\xc3\x83':'Ã',
       '\xc3\x84':'Ä', '\xc3\x89':'É', '\xc3\x88':'È', '\xc3\x8a':'Ê',
       '\xc3\x8b':'Ë', '\xc3\x8d':'Í', '\xc3\x8c':'Ì', '\xc3\x8e':'Î',
       '\xc3\x8f':'Ï', '\xc3\x93':'Ó', '\xc3\x92':'Ò', '\xc3\x94':'Ô',
       '\xc3\x95':'Õ', '\xc3\x96':'Ö', '\xc3\x9a':'Ú', '\xc3\x99':'Ù',
       '\xc3\x9b':'Û', '\xc3\x9c':'Ü', '\xc3\x87':'Ç', '\xc3\xa1':'á',
       '\xc3\xa0':'à', '\xc3\xa2':'â', '\xc3\xa3':'ã', '\xc3\xa4':'ä',
       '\xc3\xa9':'é', '\xc3\xa8':'è', '\xc3\xaa':'ê', '\xc3\xab':'ë',
       '\xc3\xad':'í', '\xc3\xac':'ì', '\xc3\xae':'î', '\xc3\xaf':'ï',
       '\xc3\xb3':'ó', '\xc3\xb2':'ò', '\xc3\xb4':'ô', '\xc3\xb5':'õ',
       '\xc3\xb6':'ö', '\xc3\xba':'ú', '\xc3\xb9':'ù', '\xc3\xbb':'û',
       '\xc3\xbc':'ü', '\xc3\xa7':'ç'}

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
