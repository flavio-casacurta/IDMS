# -*- coding: utf-8 -*-

import pdb
import os
import attribute as attr
import idms2db2  as idms
import calcKey

class CreateBooks(object):

    def __init__(self, schema=None, startRec = 0):
        self.schema   = schema
        self.startRec = startRec
        i2d           = idms.Idms2db2(schema=self.schema, startRec=self.startRec)
        self.id       = i2d.idms2db2()
        self.at       = attr.Attribute()

    def createBooks(self):

#        pdb.set_trace()

        dicSetOwner   = self.id[1]
        lisRecords    = self.id[4]

        dicCalcKeys  = calcKey.CalcKey(lisRecords).calcKeys()

        for r in lisRecords:
            if  'MEMBER_OF_SET' in r:
                lisFields =[]
                for f in r['FIELDS']:
                    lisFields.append(f['FIELD_NAME'])
                for m in r['MEMBER_OF_SET']:
                    if  dicSetOwner[m] != 'SYSTEM':
                        if dicSetOwner[m] in dicCalcKeys:
                            for ck in dicCalcKeys[dicSetOwner[m]]:
                                if  ck['FIELD_NAME'] not in lisFields:
                                    r['FIELDS'].append(ck)



        for r in lisRecords:
            recName = r['RECORD_NAME']
            book = recName + '.cpy'
            bookName = os.path.join(os.getenv('HOMEDRIVE'), os.sep, 'temp', 'books', book)
            crB = open(bookName, 'w')
            crB.write('{:>9}{:2}{}.\n'.format('01', ' ', recName))
            recName = recName[self.startRec:]
            addLevel   = 0
            fieldLevel = 0
            levelVarch = 0
            dicFieldsLevel = {}

            for f in r['FIELDS']:
                fieldName  = f['FIELD_NAME']
                if  addLevel:
                    if  int(f['FIELD_LEVEL']) <= levelVarch:
                        addLevel = 0
                    elif int(f['FIELD_LEVEL']) < fieldLevel:
                        addLevel -= 1
                if  f['FIELD_LEVEL'] != '88':
                    fieldLevel = int(f['FIELD_LEVEL'])
                fl = fieldLevel + addLevel - 2
                sp = ' ' * (11 + fl)
                dn = 8-fl
                occ = f['OCCURS'] if 'OCCURS' in f else ''
                pic = f['PICTURE'] if 'PICTURE' in f else ''

                if  'PICTURE' in f or 'OCCURS' in f:
                    var=self.at.attributeSql(f['USAGE'], int(f['LENGTH']), picture=pic, occurs=occ)
                else:
                    var='       '

                if  var[0:7] == 'VARCHAR':
                    addLevel = 1
                    levelVarch = fieldLevel
                    crB.write('{}{:{}}{}.\n'.format(sp
                                                   ,'{:02}'.format(fieldLevel)
                                                   ,dn
                                                   ,fieldName + '-VC'))
                    sp += ' '
                    dn -= addLevel
                    field = fieldName + '-LEN'
                    du = 6
                    if  len(field) > 19:
                        lf = 25 - len(field)
                        du = lf if lf > 0 else 1
                    crB.write('{}{:{}}{:19} PIC S9(004){}USAGE COMP.\n'
                                            .format(sp
                                            ,'{:02}'.format(fieldLevel + addLevel)
                                            ,dn
                                            ,field
                                            ,' '*du))

                    crB.write('{}{:{}}{}.\n'.format(sp
                                            ,'{:02}'.format(fieldLevel + addLevel)
                                            ,dn
                                            ,fieldName + '-TEXT'))
                    addLevel  += 1
                    dn -= 1
                    sp += ' '

                pt = ' ' if  'OCCURS' in f else '.'
                if 'PICTURE' in f:
                    fieldlvl = '{:02}'.format(fieldLevel + addLevel)
                    attribut = self.at.attributeCob(f['USAGE'], int(f['LENGTH']), picture=f['PICTURE'])
                    if 'REDEFINES' in f:
                        newFieldlvl = dicFieldsLevel[f['REDEFINES']]
                        addLevel    = int(newFieldlvl) - int(fieldlvl)
                        fieldlvl    = newFieldlvl
                        sp += (' ' * addLevel)
                        dn -= addLevel
                        crB.write('{}{:{}}{:19} REDEFINES \n'.format(sp
                                                                    ,fieldlvl
                                                                    ,dn
                                                                    ,fieldName))
                        fieldlvl = '  '
                        fieldName = f['REDEFINES']
                    else:
                        dicFieldsLevel[fieldName]=fieldlvl
                    crB.write('{}{:{}}{:19} PIC {}{}\n'.format(sp
                                                       ,fieldlvl
                                                       ,dn
                                                       ,fieldName
                                                       ,attribut
                                                       ,pt))
                elif f['FIELD_LEVEL'] == '88':
                    pt = ' ' if  len(f['VALUE']) > 1 else '.'

                    field = '{}{:{}}{}'.format(sp + '  '
                                           ,'{:02}'.format(88)
                                           , dn-2
                                           ,fieldName)
                    value = 'VALUE ' + f['VALUE'][0] + pt
                    crB.write('{}{:>{}}\n'.format(field, value, 72 - len(field)))

                    for xr in xrange(1,len(f['VALUE'])):
                        if  xr + 1  ==  len(f['VALUE']):
                            pt = '.'
                        value = ','.format
                        crB.write('{:>72}\n'.format(', {}{}'.format(f['VALUE'][xr].strip(), pt)))
                else:
                    fieldlvl = '{:02}'.format(fieldLevel + addLevel)
                    if  'REDEFINES' in f:
                        newFieldlvl = dicFieldsLevel[f['REDEFINES']]
                        addLevel    = int(newFieldlvl) - int(fieldlvl)
                        fieldlvl    = newFieldlvl
                        sp += (' ' * addLevel)
                        dn -= addLevel
                        crB.write('{}{:{}}{:19} REDEFINES \n'.format(sp
                                                                    ,fieldlvl
                                                                    ,dn
                                                                    ,fieldName))
                        fieldlvl = '  '
                        fieldName = f['REDEFINES']
                    else:
                        dicFieldsLevel[fieldName]=fieldlvl
                    crB.write('{}{:{}}{}{}\n'.format(sp
                                                    ,fieldlvl
                                                    , dn
                                                    ,fieldName
                                                    , pt))

                self.occurs(f, crB, recName)
            crB.close()

    def occurs(self, f, crB, recName):
        if  'OCCURS' in f:
            oc  = f['OCCURS']
            oc1 = oc[:oc.index('TIMES')+5]
            oc2 = oc[oc.index('TIMES')+5:].strip().replace('-','_').replace(recName, '')
            pt  = ' ' if oc2 else '.'
            crB.write('{:39}{}{}\n'.format(' ', oc1, pt))
            if  oc2:
                crB.write('{:39}{}.\n'.format(' ', oc2))
