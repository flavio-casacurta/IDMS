# -*- coding: utf-8 -*-

import pdb

# HOFs

isSchema        = lambda line: line.strip().startswith('SCHEMA NAME IS')
isSet           = lambda line: line.strip().startswith('SET NAME IS')
isOwner         = lambda line: line.strip().startswith('OWNER IS')
isMember        = lambda line: line.strip().startswith('MEMBER IS')
isKey           = lambda line: line.strip().startswith('KEY IS (')
isOrder         = lambda line: line.strip().startswith('ORDER IS')
isMode          = lambda line: line.strip().startswith('MODE IS')
isMandatory     = lambda line: line.strip().startswith('MANDATORY')
isOptional      = lambda line: line.strip().startswith('OPTIONAL')
isRelationship  = lambda line: isMandatory(line) or isOptional(line)
isDuplicates    = lambda line: line.strip().startswith('DUPLICATES ARE')
isOwnerOfSet    = lambda line: line.strip().startswith('OWNER OF')
isMemberOfSet   = lambda line: line.strip().startswith('MEMBER OF')
ofSet           = lambda line: line.split('OF SET')[1].strip()
splitIS         = lambda line: line.split(' IS ')[1].strip()
isRecord        = lambda line: line.strip().startswith('RECORD NAME IS')
isFimRecordSet  = lambda line: line.strip().startswith('ADD')
setNameVia      = lambda line: line.split('VIA')[1].split()[0]
isLocation      = lambda line: line.strip().startswith('LOCATION MODE IS')
isFimBloco      = lambda line: line.strip().startswith('.')
locationMode    = lambda line: line.split()[3]
isCalcKey       = lambda line: locationMode(line)=='CALC'
calcKeys        = lambda line: line[line.find('USING')+5:].replace('(','').split()
isField         = lambda line: line.strip()[0:2].isdigit()
isPicture       = lambda line: line.strip().startswith('PICTURE')
isUsage         = lambda line: line.strip().startswith('USAGE')
isLength        = lambda line: line.strip().startswith('ELEMENT LENGTH')
isOccurs        = lambda line: line.strip().startswith('OCCURS')
isRedefines     = lambda line: line.strip().startswith('REDEFINES')
isValue         = lambda line: line.strip().startswith('VALUE')

class Idms2db2(object):

    def __init__(self, schema, startRec = 0):
        self.schema   = schema
        self.startRec = startRec


    def idms2db2(self):

        lines         = open(self.schema).readlines()

        findSet       = filter(isSet, lines)
        findOwner     = filter(isOwner, lines)
        dicSetOwner   = {k:v for k, v in zip(map(splitIS, findSet),map(splitIS, findOwner))}

        findMember    = filter(isMember, lines)
        if  len(findSet) == len(findMember):
            dicSetMember  = {k:v for k, v in zip(map(splitIS, findSet), map(splitIS, findMember))}
        else:
            dicSetMember  = ''

#       schema
        dicSchema     = {}

#       control records
        records       = 0
        lisRecords    = []
        dicRecords    = {}
        recordOpen    = False
        attribRecords = {}
        lisCalcKey    = []
        lisOwners     = []
        lisMembers    = []
        lisFields     = []
        record        = False
        field         = False
        calcKey       = False

#       control sets
        set           = False
        sets          = 0
        set_name      = ''
        dicSets       = {}
        lisKeys       = []
        lisKeysTmp    = []
        setOpen       = False
        attribSets    = {}
        key           = False

#       control fields
        attribFields  = {}
        picture       = ''
        usage         = ''
        length        = 0
        field         = False
        fieldValue    = False
        lisValues     = []

        for line in lines:

#           schema
            if  isSchema(line):
                dicSchema['SCHEMA']=line.split('NAME IS')[1].split()[0]

#           fim de record or set
            elif isFimRecordSet(line):
                if  records > 0 and recordOpen:
                    if  lisOwners:
                        attribRecords['OWNER_OF_SET']=lisOwners
                    if  lisMembers:
                        attribRecords['MEMBER_OF_SET']=lisMembers
                    attribRecords['FIELDS']=lisFields
                    lisRecords.append(attribRecords)
                    dicRecords[attribRecords['RECORD_NAME']]=attribRecords['FIELDS']
                    recordOpen    = False
                    attribRecords = {}
                    lisCalcKey    = []
                    lisOwners     = []
                    lisMembers    = []
                    lisFields     = []
                    record        = False
                    field         = False
                    fieldValue    = False
                    calcKey       = False
                elif  sets > 0 and setOpen:
                    dicSets[set_name]=attribSets
                    lisKeys       = []
                    lisKeysTmp    = []
                    setOpen       = False
                    attribSets    = {}
                    key           = False

#           fim de bloco
            elif isFimBloco(line):
                if  record:
                    record = False
                elif set:
                    set    = False
                elif  field:
                    field  = False
                    lisFields.append(attribFields)
                    lisValues = []

#           tratar Record
            elif record:
                if  calcKey:                  # linha de continuacao da calc key
                    for l in line.split():
                        lisCalcKey.append(l)
                    if ')' in lisCalcKey:
                        lisCalcKey.remove(')')
                        for n, lck in enumerate(lisCalcKey):
                            lisCalcKey[n] = self.recReplace(lck, recReplace)
                        attribRecords['CALC_KEY']=lisCalcKey
                        calcKey = False
                else:
                    if  isLocation(line):
                        attribRecords['LOCATION_MODE']=locationMode(line)
                        if  isCalcKey(line):
                            lisCalcKey=calcKeys(line)
                            if ')' in lisCalcKey:
                                lisCalcKey.remove(')')
                                for n, lck in enumerate(lisCalcKey):
                                    lisCalcKey[n] = self.recReplace(lck, recReplace)
                                attribRecords['CALC_KEY']=lisCalcKey
                            else:
                                calcKey = True
                    elif isOwnerOfSet(line):
                        lisOwners.append(ofSet(line))
                    elif isMemberOfSet(line):
                        lisMembers.append(ofSet(line))

#           tratar Set
            elif set:
                if  isOrder(line):
                    attribSets['ORDER_IS']=splitIS(line)

                elif isMode(line):
                    attribSets['MODE_IS']=splitIS(line)

                elif isMember(line):
                    attribSets['MEMBER']=splitIS(line)
                    setReplace = splitIS(line)[self.startRec:]

                elif isRelationship(line):
                    attribSets['RELATIONSHIP']=line.strip()

                elif isDuplicates(line):
                    attribSets['DUPLICATES_ARE']=line.split(' ARE ')[1].strip()

                elif key:                      # linha de continuacao da key
                    lisKeysTmp.append((line.split()[0], line.split()[1]))
                    if line.find(')') != -1:
                        for t in lisKeysTmp:
                            nt = self.recReplace(t[0], setReplace)
                            lisKeys.append((nt, t[1]))
                        attribSets['KEY_IS']=lisKeys
                        key = False
                elif isKey(line):
                    key = True

#           tratar Field
            elif field:
                if  isPicture(line):
                    attribFields['PICTURE']=splitIS(line)
                elif isUsage(line):
                    attribFields['USAGE']=splitIS(line)
                elif isLength(line):
                    attribFields['LENGTH']=splitIS(line)
                elif isOccurs(line):
                    attribFields['OCCURS']=line.strip()
                elif isRedefines(line):
                    attribFields['REDEFINES']=self.recReplace(line.split()[1], recReplace)
                elif fieldValue:                # linha de continuacao do value
                    lisValues.append(line.strip().replace(')',''))
                    if  ')' in line.strip():
                        attribFields['VALUE']=lisValues
                        fieldValue = False
                elif isValue(line):
                    lisValues.append(splitIS(line).replace('(','').replace(')','').strip())
                    if  ')' in splitIS(line):
                        attribFields['VALUE']=lisValues
                    else:
                        fieldValue = True

#           define se eh record
            elif isRecord(line):
                record       = splitIS(line)
                attribRecords['RECORD_NAME']=record
                recReplace   = record[self.startRec:]
                records     += 1
                recordOpen   = True

#           define se eh set
            elif isSet(line):
                set_name     = splitIS(line)
                sets        += 1
                set          = True
                setOpen      = True

#           define se eh field
            elif isField(line):
                attribFields  = {}
                attribFields['FIELD_LEVEL']=line.split()[0]
                field        = self.recReplace(line.split()[1], recReplace)
                attribFields['FIELD_NAME']=field
                picture      = ''
                usage        = ''
                length       = 0

        if  sets > 0 and setOpen:
            dicSets[set_name]=attribSets

        return [ dicSchema
               , dicSetOwner
               , dicSetMember
               , dicSets
               , lisRecords
               , dicRecords]


    def recReplace(self, arg, recReplace):
        arg = arg.replace(recReplace, '')
        return arg[:-1] if arg[-1] == '-' else arg
