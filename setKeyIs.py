# -*- coding: utf-8 -*-

import pdb
class SetKeyIs(object):

    def __init__(self, dicSets, dicRecords):
        self.dicSets      = dicSets
        self.dicRecords   = dicRecords

    def setKeyIs(self):
        for set, value in self.dicSets.items():
            if  'KEY_IS' in value:
                lisKeys=[]
                for field in value['KEY_IS']:
                    for ff in self.fieldsComPicture(set, value, field[0]):
                        lisKeys.append((ff,field[1]))
                self.dicSets[set]['KEY_IS']=lisKeys

    def fieldsComPicture(self, set, value, field):
        retFields = []
        lisFields = self.dicRecords[value['MEMBER']]
        for n, r in enumerate(lisFields):
            if  r['FIELD_NAME'] == field:
                if  'PICTURE' in r:
                    retFields.append(field)
                else:
                    for ff in self.elementaryFields(lisFields[n:]):
                        retFields.append(ff['FIELD_NAME'])
                break
        return retFields


    def elementaryFields(self, lisFields):
        retFields=[]
        lvl=int(lisFields[0]['FIELD_LEVEL'])
        for n, f in enumerate(lisFields[1:]):
            if  int(f['FIELD_LEVEL']) == 88:
                continue
            if  int(f['FIELD_LEVEL']) > lvl:
                if  'PICTURE' in f:
                    retFields.append(f)
                else:
                    self.elementaryFields(lisFields[n+1:])
            else:
                break
        return retFields
