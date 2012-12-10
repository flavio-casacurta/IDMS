# -*- coding:utf-8
'''
   Created on 04/06/2012
   @author: C&C - HardSoft
'''

import io
from   datetime  import date
from   Aplicacao import *
from   Empresa   import *
from   Entidades import *
import utilities as utl

class cabecalhoPGM(object):

    def __init__(self
                , db
                , cAppl=None
                , entidadeId=None
                , objetivo=None
                , pgmid=None
                , servico=None
                , tppgm=None
                , userName=None
                ):
        self.cAppl          = cAppl or 0
        self.entidadeId     = entidadeId or 0
        self.objetivo       = objetivo or 'OBJETIVO'
        self.pgmid          = pgmid.upper() or 'XXX'
        self.servico        = servico.upper() or 'SERVICO'
        self.tppgm          = tppgm or 0
        self.userName       = userName.upper() or 'USER ADMIN'
        self.aplicacao      = Aplicacao(db, self.cAppl)
        self.empresa        = Empresa(db, self.aplicacao.getEmpresaId())
        self.Entidade       = Entidades(db, cAppl=self.cAppl)
        self.entidade       = self.Entidade.selectEntidadesByEntidadeId(self.entidadeId)[1][0]
        self.parametros     = db.parametros
        self.parms          = db(self.parametros).select()[0]


    def montaCabecalho(self):
        dic                 = {}
        dic['@ANALISTA']    = utl.remover_acentos(self.aplicacao.getAnalista()
                                                 + '/' + self.empresa.getNome()).upper()
        dic['@APPLID']      = self.aplicacao.getApplId().upper()
        dic['@APPLNAME']    = utl.remover_acentos(self.aplicacao.getApplName()).upper()
        dic['@AUTHOR']      = utl.remover_acentos(self.userName
                                                 + '/' + self.aplicacao.getContratante()).upper()
        dic['@DATE']        = date.today().strftime('%d/%m/%Y')
        dic['@EMPRESA']     = utl.remover_acentos(self.empresa.getDescricao()).upper()
        dic['@ENTIDADE0']   = self.entidade.nomeExterno + ' - ' + self.entidade.nomeFisico
        dic['@ENTIDADE1']   = self.entidade.nomeAmigavel.upper()[:45]
        dic['@ENTIDADE2']   = self.entidade.nomeAmigavel.upper()[45:]
        dic['@GRUPO']       = self.aplicacao.getGrupo()
        dic['@OBJETIVO']    = self.objetivo.upper()
        dic['@PGMID']       = str(self.pgmid)
        dic['@SERVICO']     = self.servico.upper()
        dic['@TPPGM']       = str(self.tppgm)

        query = db((db.tools.ferramenta == 'ADS_IDMS')
                 & (db.parametros.tool  == db.tools.id)).select()[0]

        template            = os.path.join(query.parametros.drive + ':'
                                          ,os.sep
                                          ,query.parametros.web2py
                                          ,'applications'
                                          ,query.parametros.application
                                          ,'Templates'
                                          ,query.tools.ferramenta
                                          ,'cabecPgm.CBL')

        with open(template) as f:
            templ=str(f.read())

        return utl.change(dic, templ)





