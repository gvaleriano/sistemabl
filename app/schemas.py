# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemBase(BaseModel):
    title: str
    description: str
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#Bancos
class BancosBase(BaseModel):
    b_ag: str
    b_cta: str
    b_nome: str
    is_active: bool = True

class BancosCreate(BancosBase):
    pass

class Bancos(BancosBase):
    b_cod: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
#Cambio
class CambioBase(BaseModel):
    mo_cod: str
    mo_data: datetime
    camb_valr: float
    camb_valu: float

class CambioCreate(CambioBase):
    pass

class Cambio(CambioBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#Cash
class CashBase(BaseModel):
   c_data : datetime
   c_descricao : str
   c_nome : str
   c_valor_debito : float
   c_valor_credito : float
   c_saldo : float
   c_imp_cod : str
   c_vend_cod : str
   c_fat_cod : str
   c_pag_cod : str

class CashCreate(CashBase):
    pass

class Cash(CashBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#Ativos e Amostras

class AtivoEAmostrasBase(BaseModel):
    descr: str
    ativo_fixo: bool
    valor_ent: float
    valor_lista: float
    moeda: str
    valornota: float
    dataentrada: datetime
    nf_entrada: str
    repcod: str
    courier_di: str
    out: bool

class AtivoEAmostrasCreate(AtivoEAmostrasBase):
    pass

class AtivoEAmostras(AtivoEAmostrasBase):
    cod: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

#Faturamento
class FaturamentoBase(BaseModel):
    fat_tipo: str
    fat_cliente: str
    fat_data_entrada: datetime
    fat_data_saida: datetime
    fat_valor: float
    fat_comissao: float
    fat_desconto: float
    fat_data_prevista: datetime
    fat_data_reais: datetime

class FaturamentoCreate(FaturamentoBase):
    pass

class Faturamento(FaturamentoBase):
    fat_cod: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#Contatos
class ContatosBase(BaseModel):
    trat: str
    nome: str
    sobrenome: str
    preffone: str
    fone: str
    ramal: str
    email: str
    depto: str
    cargo: str
    prioridade: str
    origem: str
    cp_outros: str
    cli_cod: int

class ContatosCreate(ContatosBase):
    pass

class Contatos(ContatosBase):
    id: int
    cliente: dict
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#Clientes
class ClientesBase(BaseModel):
    cli_nomecom: str
    cli_nomered: str
    endereco: str
    enumero: str
    complemento: str
    cep: str
    bairro: str
    cidade: str
    estado: str
    website: str
    ramo: str
    porte: str
    cgc: str
    ie: str
    responsavel: str
    origem: str
    observ: str
    cli_ativo: bool

class ClientesCreate(ClientesBase):
    pass

class Clientes(ClientesBase):
    cli_cod: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#Representadas
class RepresentadasBase(BaseModel):
    rep_preff_inv: str
    rep_nome: str
    moeda: int
    simbolo: str
    rep_crit_page: str
    rep_com1: str
    rep_com2: str
    rep_com3: str
    bl_emite_invoice: bool
    aeitacarta: bool
    rep_tem_contrato: bool
    rep_contr_tem_validade: bool
    rep_dat_venc_contr: datetime
    rep_banking: str
    rep_form_precos: str
    rep_endereco: str
    rep_ship_form: str
    repr: str
    repw: str
    repc: str

class RepresentadasCreate(RepresentadasBase):
    pass

class Representadas(RepresentadasBase):
    rep_cod: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class MoedasBase(BaseModel):
    mo_nome: str
    simbolo: str

class MoedasCreate(MoedasBase):
    pass

class Moedas(MoedasBase):
    mo_cod: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True