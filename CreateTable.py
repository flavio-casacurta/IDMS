# -*- coding: utf-8 -*-

import pdb
import os
import attribute as attr
import idms2db2  as idms
import calcKey
import setKeyIs

dicRelationship= {'MANDATORY AUTOMATIC':('CASCADE', ' NOT NULL')
                 ,'MANDATORY MANUAL':('CASCADE', '')
                 ,'OPTIONAL MANUAL':('SET NULL', '')
                 ,'OPTIONAL AUTOMATIC':('SET NULL', '')}

dicIndex= {'LAST':'      '
          ,'FIRST':'      '
          ,'NOT ALLOWED':'UNIQUE'}

dicAscDesc= {'ASCENDING':'ASC'
            ,'DESCENDING':'DESC'}

class CreateTable(object):

    def __init__(self, schema=None, owner=None, startRec = 0):
        self.schema   = schema
        self.owner    = owner or 'DB2PRD'
        self.startRec = startRec
        i2d           = idms.Idms2db2(schema=self.schema, startRec=self.startRec)
        self.id       = i2d.idms2db2()
        self.at       = attr.Attribute()

    def createTable(self):

#        pdb.set_trace()

        createtable = os.path.join(os.getenv('HOMEDRIVE'), os.sep, 'temp', 'Scripts', 'createTable.sql')
        crT = open(createtable, 'w')

        dicSchema    = self.id[0]
        dicSetOwner  = self.id[1]
#        dicSetMember = self.id[2]
        dicSets      = self.id[3]
        lisRecords   = self.id[4]
        dicRecords   = self.id[5]

        setKeyIs.SetKeyIs(dicSets, dicRecords).setKeyIs()
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
            crT.write('CREATE TABLE ' + self.owner + '.' + recName + '\n')
            crT.write('(' + '\n')
            comma  = ' '
            occurs = False
            redefn = False
            fieldLevel = '0'
            for f in r['FIELDS']:
                if  occurs:
                    if  f['FIELD_LEVEL'] > fieldLevel:
                        continue
                    else:
                        occurs = False
                if  redefn:
                    if  f['FIELD_LEVEL'] > fieldLevel:
                        continue
                    else:
                        redefn = False
                if  'OCCURS' in f and not 'PICTURE' in f:
                    occurs = True
                    fieldLevel = f['FIELD_LEVEL']
                    at = self.at.attributeSql(f['USAGE'], int(f['LENGTH']), occurs=f['OCCURS'])
                    crT.write('{:}{:<23} {:}{:}'.format(comma, f['FIELD_NAME'].replace('-','_')+'_VC', at,'\n'))

                elif 'REDEFINES' in f:
                    redefn = True
                    fieldLevel = f['FIELD_LEVEL']
                    continue

                elif 'PICTURE' in f:
                    OCCURS=None
                    if  'OCCURS' in f:
                        OCCURS=f['OCCURS']
                    at = self.at.attributeSql(f['USAGE'], int(f['LENGTH']), picture=f['PICTURE'], occurs=OCCURS)
                    var='_VC' if at[0:7] == 'VARCHAR' else ''
                    crT.write('{:}{:<23} {:}{:}{:}'.format(comma
                                                          ,f['FIELD_NAME'].replace('-','_')+var
                                                          , at
                                                          , self.notNull(r, f, dicSetOwner, dicSets, dicCalcKeys)
                                                          ,'\n'))
                comma = ','

            if  'CALC_KEY' in r:
                commaSpace = ''
                primaryKey = '{:}{:<23} {:}'.format(comma
                                                   , 'CONSTRAINT '+ recName + 'PK'
                                                   , 'PRIMARY KEY (')
                for ck in dicCalcKeys[recName]:
                    primaryKey += commaSpace + ck['FIELD_NAME'].replace('-','_')
                    commaSpace  = ', '
                primaryKey +=')'
                crT.write(primaryKey[:80] +'\n')
                if  len(primaryKey) > 80:
                    crT.write(primaryKey[80:] +'\n')

            if  'MEMBER_OF_SET' in r:
                for n, m in enumerate(r['MEMBER_OF_SET']):
                    if  dicSetOwner[m] != 'SYSTEM':
                        if  dicSetOwner[m] in dicCalcKeys:
                            foreignKey = '{:}{:<23} {:}'.format(comma
                                                               , 'CONSTRAINT '+ recName + 'FK' + str(n)
                                                               , 'FOREIGN KEY (')
                            commaSpace = ''
                            for ck in dicCalcKeys[dicSetOwner[m]]:
                                foreignKey += commaSpace + ck['FIELD_NAME'].replace('-','_')
                                commaSpace = ', '
                            foreignKey +=')'
                            crT.write(foreignKey[:80] +'\n')
                            if  len(foreignKey) > 80:
                                crT.write(foreignKey[80:] +'\n')

                            foreignKey = '  {:<18} {:} ('.format('REFERENCES'
                                                                , self.owner + '.' + dicSetOwner[m])
                            commaSpace = ''
                            for ck in dicCalcKeys[dicSetOwner[m]]:
                                foreignKey += commaSpace + ck['FIELD_NAME'].replace('-','_')
                                commaSpace = ', '
                            foreignKey +=')'
                            crT.write(foreignKey[:80] +'\n')
                            if  len(foreignKey) > 80:
                                crT.write(foreignKey[80:] +'\n')
                            crT.write('  ON DELETE '
                                     + dicRelationship[dicSets[m]['RELATIONSHIP']][0]
                                     +'\n')

                crT.write(');' + '\n')
                crT.write('\n')

                for n, m in enumerate(r['MEMBER_OF_SET']):
                    if  'KEY_IS' in dicSets[m]:
                        crT.write('CREATE {0} INDEX {1} ON {2}\n'.format(dicIndex[dicSets[m]['DUPLICATES_ARE']]
                                                                        , self.owner + '.' + recName + 'IX' + str(n)
                                                                        , self.owner + '.' + recName))
                        comma = '('
                        for t in dicSets[m]['KEY_IS']:
                            crT.write('{:}{:<23} {:}\n'.format(comma, t[0].replace('-','_'), dicAscDesc[t[1]]))
                            comma = ','
                        crT.write(');' + '\n')
                        crT.write('\n')
            else:
                crT.write(');' + '\n')
                crT.write('\n')
        crT.close()
        print '>>>>>>>>>>>>>>><<<<<<<<<<<<<<<'
        print '>>> Create Table gerado OK <<<'
        print '>>>>>>>>>>>>>>><<<<<<<<<<<<<<<'

    def notNull(self, r, f, dicSetOwner, dicSets, dicCalcKeys):
        notNull = ''
        if  'CALC_KEY' in r:
            for ck in dicCalcKeys[r['RECORD_NAME']]:
                if  f['FIELD_NAME'] == ck['FIELD_NAME']:
                    notNull = ' NOT NULL'
                    return notNull
        if  'MEMBER_OF_SET' in r:
            for m in r['MEMBER_OF_SET']:
                if  dicSetOwner[m] != 'SYSTEM':
                    if  dicSetOwner[m] in dicCalcKeys:
                        for ck in dicCalcKeys[dicSetOwner[m]]:
                            if  f['FIELD_NAME'] == ck['FIELD_NAME']:
                                notNull = dicRelationship[dicSets[m]['RELATIONSHIP']][1]
        return notNull



