# -*- coding: utf-8 -*-

import pdb

dicAttrSql ={'COMP2'         : 'SMALLINT'
            ,'COMP4'         : 'INTEGER'
            ,'COMP8'         : 'DOUBLE'
            ,'COMP-3'        : 'DECIMAL('
            ,'DISPLAYX'      : 'CHAR('
            ,'OUTROS'        : 'CHAR('
            ,'DISPLAY9'      : 'DECIMAL('
            ,'CONDITION-NAME': ''}

dicAttrCob ={'COMP2'         : ('S9', '004', 'COMP')
            ,'COMP4'         : ('S9', '009', 'COMP')
            ,'COMP8'         : ('S9', '018', 'COMP')
            ,'COMP-3'        : ('S9', '000', 'COMP-3')
            ,'DISPLAYX'      : (' X', '000', 'DISPLAY')
            ,'OUTROS'        : (' X', '000', 'DISPLAY')
            ,'DISPLAY9'      : ('S9', '000', 'COMP-3')
            ,'CONDITION-NAME': ('  ', '000', '')}



class Attribute(object):

    def __init__(self):
        pass

### Atributos SQL

    def attributeSql(self
                    ,usage
                    ,length
                    ,picture=None
                    ,occurs=None
                    ):

#        pdb.set_trace()


        if  usage == 'COMP':
            if str(length) in ('2, 4, 8'):
               return dicAttrSql[usage + str(length)]

# Determina se a picture tem occurs

        if  occurs:
            usage   = 'DISPLAY'
            tamanho = length
            picture = ''

        pic      = picture
        decimais = 0

# Se picture nao informada cria picture
        if  not pic:
            pic = 'X' * length


# Determina a natureza Alpha ou Numerica
        if  pic[0] == 'S':
            pic = pic[1:]
        pic0 = pic[0]

        if  not occurs:
# Determina se a picture tem parenteses
            pap = pic.find('(')

# determina tamanho dos inteiros e decimais SEM parenteses
            if  pap == -1:
                if  'V' in pic:
                    inteiros = pic.index('V')
                    decimais = len(pic)-(pic.index('V')+1)
                else:
                    inteiros = len(pic)
# determina tamanho dos inteiros e decimais COM parenteses
            else:
                if  'V' in pic:
                    intTmp = pic[:pic.index('V')]
                    decTmp = pic[pic.index('V')+1:]
                    if  '('  in intTmp:
                        inteiros = int(intTmp[intTmp.index('(')+1:intTmp.index(')')])
                    else:
                        inteiros = len(intTmp)
                    if  '('  in decTmp:
                        decimais = int(decTmp[decTmp.index('(')+1:decTmp.index(')')])
                    else:
                        decimais = len(decTmp)
                else:
                    inteiros = int(pic[pap+1:pic.index(')')])

            tamanho      = inteiros + decimais


        comma        = ','
        if  decimais == 0:
            decimais = ''
            comma    = ''

        var          = ''
        if  tamanho  > 10 and usage == 'DISPLAY' or occurs:
            var      = 'VAR'

        tamanho      = str(tamanho)
        decimais     = str(decimais)


        if  usage in dicAttrSql:
            return dicAttrSql[usage] + tamanho + comma + decimais + ')'
        if  usage + pic0 in dicAttrSql:
            return var + dicAttrSql[usage + pic0] + tamanho + comma + decimais + ')'
        return dicAttrSql['OUTROS'] + tamanho + comma + decimais + ')'

### Atributos COBOL

    def attributeCob(self
                    ,usage
                    ,length
                    ,picture=None
                    ):

#        pdb.set_trace()

        if  usage == 'COMP':
            if str(length) in ('2, 4, 8'):
               return '{0}({1})      USAGE {2}'.format(dicAttrCob[usage + str(length)][0]
                                                      ,dicAttrCob[usage + str(length)][1]
                                                      ,dicAttrCob[usage + str(length)][2])

        pic, V, pic0 = self.detPicture(length, picture=picture)

        if  not usage in dicAttrCob:
            if  usage + pic0 in dicAttrCob:
                usage = usage + pic0
            else:
                usage = 'OUTROS'

        return '{0}{1}{2} USAGE {3}'.format(dicAttrCob[usage][0]
                                 ,pic
                                 ,V
                                 ,dicAttrCob[usage][2])


    def detPicture(self
                  ,length
                  ,picture=None
                   ):
        pic = picture
        V   = '     '

# Se picture nao informada cria picture
        if  not pic:
             return ['({:03})'.format(length), V, 'X']

# Determina a natureza Alpha ou Numerica
        if  pic[0] == 'S':
            pic = pic[1:]
        pic0 = pic[0]

# Determina se a picture tem parenteses
        pap = pic.find('(')

# Se a picture nao tem parenteses coloca
        decimais = 0
        if  pap == -1:
            if  'V' in pic:
                inteiros = pic.index('V')
                decimais = len(pic)-(inteiros+1)
                V        = 'V({:02})'.format(decimais)
            else:
                inteiros = len(pic)
        else:
            if  'V' in pic:
                intTmp = pic[:pic.index('V')]
                decTmp = pic[pic.index('V')+1:]
                if  '('  in intTmp:
                    inteiros = int(intTmp[intTmp.index('(')+1:intTmp.index(')')])
                else:
                    inteiros = len(intTmp)
                if  '('  in decTmp:
                    decimais = int(decTmp[decTmp.index('(')+1:decTmp.index(')')])
                else:
                    decimais = len(decTmp)
                V        = 'V({:02})'.format(decimais)
            else:
                inteiros = int(pic[pap+1:pic.index(')')])
        return ['({:03})'.format(inteiros), V, pic0]

