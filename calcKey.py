# -*- coding: utf-8 -*-

import pdb
class CalcKey(object):

    def __init__(self, lisRecords):
        self.lisRecords = lisRecords

    def calcKeys(self):
        dicCalcKeys={}
        for r in self.lisRecords:
            attribFields=[]
            if 'CALC_KEY' in r:
                for ck in r['CALC_KEY']:
                    for n, f in enumerate(r['FIELDS']):
                        if  ck == f['FIELD_NAME']:
                            if  'PICTURE' in f:
                                attribFields.append(self.firstLevel(f))
                            else:
                                for ff in self.elementaryFields(r['FIELDS'][n:]):
                                    attribFields.append(self.firstLevel(ff))
                            break

                dicCalcKeys[r['RECORD_NAME']]=attribFields

        return dicCalcKeys

    def elementaryFields(self, lisFields):
        retFields=[]
        lvl=int(lisFields[0]['FIELD_LEVEL'])
        for n, f in enumerate(lisFields[1:]):
            if  int(f['FIELD_LEVEL']) > lvl:
                if  'PICTURE' in f:
                    retFields.append(f)
                else:
                    self.elementaryFields(lisFields[n+1:])
            else:
                break

        return retFields

    def firstLevel(self, field):
        field['FIELD_LEVEL']='02'
        return field


