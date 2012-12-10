from attribute import Attribute
attr = Attribute()
at   = attr.attributeSql('COMP-3', 24, picture='S9(13)V99', occurs='OCCURS 3 TIMES')
print at
at   = attr.attributeSql('DISPLAY',6)
print at
at   = attr.attributeSql('COMP-3', 3, picture='9(05)')
print at
at   = attr.attributeSql('COMP-3', 8, picture='S9(13)V99')
print at
at   = attr.attributeSql('COMP', 4, picture='S9(08)')
print at
at   = attr.attributeSql('COMP', 2, picture='S9(04)')
print at
at   = attr.attributeSql('COMP-3', 2, picture='S9(13)V99')
print at
at   = attr.attributeSql('DISPLAY', 2, picture='XX')
print at
at   = attr.attributeSql('COMP-3', 3, picture='S99V999')
print at
at   = attr.attributeSql('DISPLAY',78, occurs='OCCURS 3 TIMES')
print at
at   = attr.attributeSql('DISPLAY',30, picture='X(02)',occurs='OCCURS 15 TIMES')
print at
at   = attr.attributeSql('DISPLAY',516, occurs='OCCURS 0 TO 43 TIMES DEPENDING ON PPR10INDICEB04')
print at


from attribute import Attribute
attr = Attribute()
at   = attr.attributeCob('DISPLAY',6)
print at
at   = attr.attributeCob('COMP-3', 3, picture='9(05)')
print at
at   = attr.attributeCob('COMP-3', 8, picture='S9(13)V99')
print at
at   = attr.attributeCob('DISPLAY', 2, picture='S9(13)V99')
print at
at   = attr.attributeCob('DISPLAY', 2, picture='XX')
print at
at   = attr.attributeCob('DISPLAY', 220, picture='X(220)')
print at
at   = attr.attributeCob('COMP-3', 3, picture='S99V999')
print at
at   = attr.attributeCob('COMP', 4, picture='S9(08)')
print at
at   = attr.attributeCob('COMP', 2, picture='S9(04)')
print at

import CreateTable as ct
from time import time
t0 = time()
crt = ct.CreateTable(schema=r"C:\web2py\applications\Resource\modules\schemaB.txt", owner="DB2DES", startRec = 1)
crt.createTable()
print 'tempo transcorrido:', time()-t0

nameSet    = map(splitIS, findSet)
nameOwner  = map(splitIS, findOwner)

isSet      = lambda line: line.strip().startswith('SET NAME IS')
isOwner    = lambda line: line.strip().startswith('OWNER IS')
isMember   = lambda line: line.strip().startswith('MEMBER IS')
splitIS    = lambda line: line.split('IS')[1].strip()

lines      = open(r'C:\web2py\applications\Resource\modules\schemaC.txt').readlines()

findSet    = filter(isSet, lines)

findOwner  = filter(isOwner, lines)

dicSetOwner = {k:v for k, v in zip(map(splitIS, findSet),map(splitIS, findOwner))}

findMember  = filter(isMember, lines)

dicMemberSet = {k:v for k, v in zip(map(splitIS, findMember), map(splitIS, findSet))}

firstLevel = lambda line: line['FIELD_LEVEL']==lvl

for r in lisRecords:
    print '>>> ', r['RECORD_NAME']
    if r['RECORD_NAME'] == 'BPPO00':
        pdb.set_trace
    lvl=r['FIELDS'][0]['FIELD_LEVEL']
    lisFields = filter(firstLevel, r['FIELDS'])
    for f in lisFields:
        if 'PICTURE' in f:
            at = attr.attribute(f['USAGE'], int(f['LENGTH']), picture=f['PICTURE'])
        else:
            at = attr.attribute(f['USAGE'], int(f['LENGTH']))
        print f['FIELD_LEVEL'], ' - ', f['FIELD_NAME'], at

for r in lisRecords:
    if  r['RECORD_NAME'] == 'BPPO00':
        for f in r['FIELDS']:
            if  'PICTURE' in f:
                print f['FIELD_LEVEL'], ' - ', f['FIELD_NAME'],
                print f['USAGE'], f['LENGTH'], f['PICTURE']
            else:
                print f['FIELD_LEVEL'], ' - ', f['FIELD_NAME'],
                print f['USAGE'], f['LENGTH']


for r in lisRecords:
    if  r['RECORD_NAME'] == 'BPPC40':
        print '>>> ', r['RECORD_NAME'], ' - ',
        print r



isKey   = lambda line: 'KEY_IS' in line
keyIs   = lambda line: [k for k in line['KEY_IS'].keys()]
setName = lambda line: line['SET_NAME']
ki = filter(isKey, ls)

isSystem = lambda line: line[1]=='SYSTEM'

isys=filter(isSystem, so.items())


dicCalcKeys={}
for r in lisRecords:
    attribFields=[]
    if 'CALC_KEY' in r:
        for ck in r['CALC_KEY']:
            for f in r['FIELDS']:
                if  ck == f['FIELD_NAME']:
                    attribFields.append(f)
        dicCalcKeys[r['RECORD_NAME']]=attribFields

for r in lisRecords:
    if  'MEMBER_OF_SET' in r:
        print r['RECORD_NAME'], ' - ', len(r['FIELDS'])

for r in lisRecords:
    if  'MEMBER_OF_SET' in r:
        for m in r['MEMBER_OF_SET']:
            if dicSetOwner[m] in dicCalcKeys:
                for ck in dicCalcKeys[dicSetOwner[m]]:
                    r['FIELDS'].append(ck)


for r in lisRecords:
    if  'MEMBER_OF_SET' in r:
        print r['RECORD_NAME']
        for m in r['MEMBER_OF_SET']:
            owner = dicSetOwner[m]
            print 'set   - ',m
            print 'owner - ', owner


for r in lisRecords:
    if  'MEMBER_OF_SET' in r:
        print r['RECORD_NAME']
        for m in r['MEMBER_OF_SET']:
            print '  ',m


for r in lisRecords:
    if  'MEMBER_OF_SET' in r:
        for m in r['MEMBER_OF_SET']:
            if  dicSetOwner[m] != 'SYSTEM':
                if  dicSetOwner[m] not in dicCalcKeys:
                    print dicSetOwner[m], ' - Nao tem Calc Key'
                    if  dicSetOwner[m] in dicMemberSet:
                        print "          Mas e' Membro de ", dicMemberSet[dicSetOwner[m]]
                    else:
                        print '          E nao e Membro de ninguem'


import idms2db2 as idms
i2d = idms.Idms2db2(schema=r"C:\web2py\applications\Resource\modules\schemaC.txt")
id  = i2d.idms2db2()
lisRecords   = id[3]

import calcKey
dicCalcKeys = calcKey.CalcKey(lisRecords).calcKeys()


CREATE UNIQUE INDEX DB2PRD.ACDVX700     ON DB2PRD.VNCLO_QUOTA
    (CIDTFD_EMPR_CTSTA                  ASC,
     CACNST_CTSTA                       ASC,
     CPSSOA_ENVOL_CTSTA                 ASC,
     CIDTFD_EMPR                        ASC,
     CEMISS_QUOTA                       ASC,
     CSERIE_QUOTA                       ASC,
     CTPO_VNCLO_ACAO                    ASC,
     CIDTFD_EST_INTLZ                   ASC,
     CVNCLO_ACAO                        ASC,
     CLOTE_QUOTA_VNCLO                  ASC)
    BUFFERPOOL BP2
    CLOSE      NO
    USING VCAT SIG
;

  CREATE UNIQUE INDEX DB2PRD.BACBX070 ON DB2PRD.P322LST
(
     LOCATION_CODE,
     TABLE_TYPE_CODE,
     CACS_STATE_CODE
) CLUSTER
  CLOSE NO
  SUBPAGES 4
  USING VCAT SIG

;

CREATE TYPE 2 UNIQUE INDEX DB2PRD.FABEX090 ON DB2PRD.POSIC_TRIBU_FABE
(
       CFUNDO_INVES                   ASC,
       CBCO                           ASC,
       CAG_BCRIA                      ASC,
       CCTA_CORR_EXTER                ASC,
       CCERTF_MULTF                   ASC
)
       USING VCAT SIG
       CLUSTER
       BUFFERPOOL BP2
       CLOSE NO
;



dicAscDesc= {'ASCENDING':'ASC','DESCENDING':'DESC'}


for s in lisRecords:
    recName = s['RECORD_NAME']
    if  'MEMBER_OF_SET' in s:
        comma = '('
        for n, m in enumerate(s['MEMBER_OF_SET']):
            if  'KEY_IS' in dicSets[m]:
                for k, v in dicSets[m]['KEY_IS'].items():
                    print comma,
                    print k.replace('-','_').replace('_'+ recName, ''),
                    print dicAscDesc[v],
                    print '\n'
                    comma = ','


for s in lisRecords:
    if  'MEMBER_OF_SET' in s:
        for n, m in enumerate(s['MEMBER_OF_SET']):
            if  'KEY_IS' in dicSets[m]:
                print dicSets[m]['KEY_IS']
                    print k.replace('-','_').replace('_'+ recName, ''),
                    print dicAscDesc[v],
                    comma = ','

dicAuxPic={'COMP':'S', 'COMP-3':'S', 'CONDITION-NAME':' ', 'DISPLAY':' '}
for f in lisRecords[0]['FIELDS']:
    fl = int(f['FIELD_LEVEL'])-2
    sp = ' ' * (11 + fl)
    dn = 8-fl
    ap = dicAuxPic[f['USAGE']]
    if 'PICTURE' in f:
        print '{0}{FIELD_LEVEL:{1}}{FIELD_NAME:19} PIC {2}{PICTURE} USAGE {USAGE}.'.format(sp, dn, ap, **f)
    else:
        print '{0}{FIELD_LEVEL:{1}}{FIELD_NAME}.'.format(sp, dn, **f)


print '{0}({1})'.format(dicAttrCob['COMP2'][0], dicAttrCob['COMP2'][1])



import idms2db2 as idms
from time import time
t0 = time()
i2d = idms.Idms2db2(schema=r"C:\web2py\applications\Resource\modules\schemaB.txt", startRec = 1)
id  = i2d.idms2db2()
dicSchema    = id[0]
dicSetOwner  = id[1]
dicMemberSet = id[2]
dicSets      = id[3]
lisRecords   = id[4]
dicRecords   = id[5]
print 'tempo transcorrido:', time()-t0

from time import time
t0 = time()
import idms2db2 as idms
i2d = idms.Idms2db2(schema=r"C:\web2py\applications\Resource\modules\schemaC.txt", startRec = 1)
id  = i2d.idms2db2()
dicSchema    = id[0]
dicSetOwner  = id[1]
dicMemberSet = id[2]
dicSets      = id[3]
lisRecords   = id[4]
dicRecords   = id[5]
print 'tempo transcorrido:', time()-t0

dicFields = {}
for lr in lisRecords:
    for f in lr['FIELDS']:
        FIELD_NAME = f['FIELD_NAME'].replace(lr['RECORD_NAME'][1:],'')
        if  not 'PICTURE' in f:
            f['PICTURE']='X('+str(f['LENGTH'])+')'
        if  FIELD_NAME in dicFields:
            if  dicFields[FIELD_NAME]['LENGTH'] <= f['LENGTH']:
                continue
        dicFields[FIELD_NAME] = {'FIELD_LEVEL':f['FIELD_LEVEL']
                                ,'LENGTH':f['LENGTH']
                                ,'USAGE':f['USAGE']
                                ,'PICTURE':f['PICTURE']}

query = db(db.datatypes).select()
dicDatatypes={}
for l in query:
    dicDatatypes[l.descricao]=l.id

from attribute import Attribute
attr = Attribute()

dicCols = {}
for k in dicFields.keys():
    at = attr.attributeSql( dicFields[k]['USAGE']
                          , dicFields[k]['LENGTH']
                          , dicFields[k]['PICTURE']).split('(')
    dtt = at[0]
    dec = 0
    if  len(at) > 1:
        intdec = at[1].split(',')
        lght   = intdec[0].replace(')','')
        if  len(intdec) > 1:
            dec = intdec[1].replace(')','')
    dicCols[k]={'codigoDatatype':dicDatatypes[dtt]
               ,'tamanhoColuna':lght
               ,'decimais':dec}


import sys
colunas = db.colunas

for k in sorted(dicCols.keys()):
    try:
        colunas.insert(codigoAplicacao = 1
                      ,columnName      = k
                      ,codigoDatatype  = dicCols[k]['codigoDatatype']
                      ,tamanhoColuna   = dicCols[k]['tamanhoColuna']
                      ,decimais        = dicCols[k]['decimais']
                      )
    except:
        raise Exception("Ocorreu um erro no Insert da Tabela Colunas." , sys.exc_info()[1])

for k, v in dicSets.items():
    if  'KEY_IS' in v:
        dicKeys={}
        for kk, vv in v['KEY_IS'].items():
            print kk, '- ',vv

lisFields = dicRecords[dicSetMember['BPPD00-BPPD10']]

ds = open(r"C:\temp\dicSets_new.txt", 'w')
for k, v in dicSets.items():
    ds.write(k + ' - ' + str(v) + '\n')
ds.close()

#banrisul
import CreateTable as ct
from time import time
t0 = time()
crt = ct.CreateTable(schema=r"C:\web2py\applications\Resource\modules\schemaB.txt", owner="DB2DES", startRec = 1)
crt.createTable()
print 'tempo transcorrido:', time()-t0

#banrisul
from time import time
t0 = time()

import CreateBooks as cb
crb = cb.CreateBooks(schema=r"C:\web2py\applications\Resource\modules\schemaB.txt", startRec = 1)
crb.createBooks()
print 'tempo transcorrido:', time()-t0

#banrisul
from time import time
t0 = time()
import CreateBooks_TEXT as cb
crb = cb.CreateBooks(schema=r"C:\web2py\applications\Resource\modules\schemaB.txt", startRec = 1)
crb.createBooks()
print 'tempo transcorrido:', time()-t0

#caixafederal
from time import time
t0 = time()
import CreateTable as ct
crt = ct.CreateTable(schema=r"C:\web2py\applications\Resource\modules\schemaC.txt", owner="DB2CXF")
crt.createTable()
print 'tempo transcorrido:', time()-t0


import CreateBooks as cb
crb = cb.CreateBooks(schema=r"C:\web2py\applications\Resource\modules\schemaC.txt", startRec = 0)
crb.createBooks()



import idms2db2 as idms
from time import time
t0 = time()
i2d = idms.Idms2db2(schema=r"C:\web2py\applications\Resource\modules\schemaC.txt")
id  = i2d.idms2db2()
dicSchema    = id[0]
dicSetOwner  = id[1]
dicSetMember = id[2]
dicSets      = id[3]
lisRecords   = id[4]
dicRecords   = id[5]
print 'tempo transcorrido:', time()-t0

import setKeyIs
setKeyIs.SetKeyIs(dicSetMember, dicSets, dicRecords).setKeyIs()

for set, v in dicSets.items():
    if 'KEY_IS' in v:
        print '{:16} - {}'.format(set,v['KEY_IS'])


for r in lisRecords:
    for f in r['FIELDS']:
        if 'REDEFINES' in f and 'PICTURE' in f:
            print '{} - {:20} - {}'.format(r['RECORD_NAME'], f['FIELD_NAME'], f['REDEFINES'])



for r in lisRecords:
    for f in r['FIELDS']:
        if 'VALUE' in f:
            print '{:8} - {:20} - '.format(r['RECORD_NAME'], f['FIELD_NAME'])
            value = 'VALUE'
            for v in f['VALUE']:
                print '{:>36} {:}'.format(value, v)
                value = '    ,'

for f in dicRecords['SFHRB045']:
    if  f['FIELD_LEVEL'] == '88':
        print f['VALUE']

for n, r in enumerate(lisRecords):
    for f in r['FIELDS']:
        if 'REDEFINES' in f:
            print r['RECORD_NAME'], ' - ', n
