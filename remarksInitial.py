from time import gmtime, strftime

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

txt = [' MODULO GERADO A PARTIR DO SCHEMA @SCHEMA'
      ,' PARA MANUTENCAO DA TABELA @TABLE')
      ,' POR  RESOURCE ITSOLUTIONS'
      ,'   visite www.resource.com.br '
      ,'   Engenharia de SoftWare:'
      ,'      Flavio A. Casacurta'
      ,'EM %s' % strftime("%a, %d %b %Y AS %H:%M:%S", gmtime())]

print '{0}{1}'.format(remarks('R'),'%'*65)

for t in txt:
    print '{0}{1}{2:45}{1}'.format(remarks('R'),'%'*10, t)

print '{0}{1}'.format(remarks('R'),'%'*65)
