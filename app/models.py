# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Float, Date, Index, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

#items
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

#Bancos
class Bancos(Base):
    __tablename__ = "bancos"
    
    b_cod = Column(Integer, primary_key=True, index=True, autoincrement=True)
    b_ag = Column(String(20), nullable=False)
    b_cta = Column(String(20), nullable=False)
    b_nome = Column(String(20), nullable=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
       {'schema': 'public'}
    )
#Ativos e Amostras
class AtivoEAmostras(Base):
    __tablename__ = "ativo_e_amostras"

    cod = Column(Integer, primary_key=True, autoincrement=True)
    descr = Column(String(50))
    ativo_fixo = Column(Boolean, default=False)
    valor_ent = Column(Numeric(precision=11, scale=2))  # Número decimal
    valor_lista = Column(Numeric(precision=11, scale=2))
    moeda = Column(String(6))
    valornota = Column(Numeric(precision=11, scale=2))
    dataentrada = Column(DateTime)
    nf_entrada = Column(String(8))
    repcod = Column(String(6))
    courier_di = Column(String(6))
    out = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

#Cambios
class Cambio(Base):
    __tablename__ = "cambio"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mo_cod = Column(String(6), nullable=False)
    mo_data = Column(String(8), nullable=False)
    camb_valr = Column(Float(15), nullable=False)
    camb_valu = Column(Float(15), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('ix_cambio_mo_cod_mo_data', 'mo_cod', 'mo_data'),
        Index('ix_cambio_mo_cod', 'mo_cod'),
        {'schema': 'public'}
    )
#Cash
class Cash(Base):
    __tablename__ = "cash"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    c_data = Column(Date, nullable=False)
    c_descricao = Column(String(50), nullable=False)
    c_nome = Column(String(20), nullable=False)
    c_valor_debito = Column(Float(14), nullable=False)
    c_valor_credito = Column(Float(14), nullable=False)
    c_saldo = Column(Float(14), nullable=False)
    c_imp_cod = Column(String(6), nullable=False)
    c_vend_cod = Column(String(6), nullable=False)
    c_fat_cod = Column(String(6), nullable=False)
    c_pag_cod = Column(String(6), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('ix_cash_composite', 'c_data', 'c_descricao', 'c_valor_debito'),
        Index('ix_cash_fat_cod', 'c_fat_cod'),
        Index('ix_cash_imp_cod', 'c_imp_cod'),
        Index('ix_cash_creditos', 'c_data', 'c_valor_credito'),
        {'schema': 'public'}
    )
#Clientes
class Clientes(Base):
    __tablename__ = 'clientes'
    
    cli_cod = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cli_nomecomp = Column(Text, nullable=False)
    cli_nomered = Column(String(35), nullable=True)
    endereco = Column(String(50), nullable=False)
    enumero = Column(String(6), nullable=False)
    complemento = Column(String(25), nullable=True)
    cep = Column(String(9), nullable=False)
    bairro = Column(String(25), nullable=False)
    cidade = Column(String(30), nullable=False)
    estado = Column(String(2), nullable=False)
    website = Column(String(60), nullable=True)
    ramo = Column(String(35), nullable=True)
    porte = Column(String(25), nullable=True)
    cgc = Column(String(18), nullable=True)
    ie = Column(String(14), nullable=True)
    responsavel = Column(String(6), nullable=True)
    origem = Column(String(45), nullable=True)
    observ = Column(Text, nullable=True)
    cli_ativo = Column(Boolean)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_cep', 'cep', unique=False),
        Index('ix_codigo', 'cli_cod', unique=True),
        Index('ix_endredeco', 'endereco', 'enumero', unique=False),
        Index('ix_nome_reduzido', 'cli_nomered', unique=True),
        {'schema': 'public'}
    )
#Contatos
class Contatos(Base):
    __tablename__ = 'contatos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trat = Column(String(5))
    nome = Column(String(30))
    sobrenome = Column(String(30))
    preffone = Column(String(4))
    fone = Column(String(9))
    ramal = Column(String(5))
    email = Column(String(50))
    depto = Column(String(40))
    cargo = Column(String(35))
    prioridade = Column(String(4))
    origem = Column(String(45))
    cp_outros = Column(String(50))

    cli_cod = Column(String(6), ForeignKey('public.clientes.cli_cod', ondelete="CASCADE"), nullable=False)
    cliente = relationship("Clientes", backref="contatos")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('ix_clicod', 'cli_cod'),
        Index('ix_contatos', 'nome', 'sobrenome'),
        Index('ix_contatos_por_empregado', 'cli_cod', 'nome', 'sobrenome'),
        {'schema': 'public'}
    )

#Faturamento
class Faturamento(Base):
    __tablename__ = "faturamento"

    fat_cod = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fat_tipo = Column(String(35), nullable=False)
    fat_cliente = Column(String(50), nullable=False)
    fat_data_entrada = Column(DateTime(timezone=True), nullable=False)
    fat_data_saida = Column(DateTime(timezone=True), nullable=False)
    fat_valor = Column(Float(15), nullable=False)
    fat_comissao = Column(Float(15), nullable=False)
    fat_desconto = Column(Float(15), nullable=False)
    fat_data_prevista = Column(DateTime(timezone=True), nullable=False)
    fat_data_reais = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('ix_faturamento_fat_cod', 'fat_cod', unique=True),
        Index('ix_faturamento_fat_cliente', 'fat_cliente'),
        {'schema': 'public'}
    )

class FaturamentoDetalhe(Base):
    __tablename__ = "fat_detalhe"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fat_cod = Column(String(6), ForeignKey('public.faturamento.fat_cod', ondelete="CASCADE"), nullable=False, index=True)
    det_item = Column(String(50), nullable=False, index=True)
    det_item_cod_cli = Column(String(50), nullable=False)
    det_qtd = Column(Float(15), nullable=False)
    det_preco_lista = Column(Float(14), nullable=True)
    det_preco_venda = Column(Float(14), nullable=True)
    det_tot_item = Column(Float, nullable=True)
    det_desc = Column(String(4), nullable=True)
    det_com = Column(String(4), nullable=True)
    det_val_com = Column(Float(14), nullable=True)
    det_val_com_tot = Column(Float(14), nullable=True)

    __table_args__ = (
        Index('ix_detalhe', 'fat_cod'),
        Index('ix_por_item', 'det_item'),
        {'schema': 'public'}
    )
#Representadas
class Representadas(Base):
    __tablename__ = "representadas"

    rep_cod = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rep_nome = Column(String(50), nullable=True, index=True)
    moeda = Column(Integer, ForeignKey('public.moedas.mo_cod', ondelete="CASCADE"), nullable=False)
    simbolo = Column(String(10), nullable=True)
    rep_com1 = Column(String(4), nullable=True)
    rep_com2 = Column(String(4), nullable=True)
    rep_com3 = Column(String(4), nullable=True)
    rep_crit_page = Column(String(18), nullable=True)
    rep_banking = Column(Text, nullable=True)
    rep_tem_contrato = Column(Boolean, nullable=False, default=False)
    rep_contr_tem_validade = Column(Boolean, nullable=False, default=False)
    rep_dat_venc_contr = Column(DateTime, nullable=True)
    rep_form_precos = Column(Text, nullable=True)
    rep_endereco = Column(Text, nullable=True)
    rep_preff_inv = Column(String(50), nullable=True)
    bl_emite_invoice = Column(Boolean, nullable=False, default=False)
    rep_ship_form = Column(Text, nullable=True)
    aeitacarta = Column(Boolean, nullable=False, default=False)
    repr = Column(Text, nullable=True)
    repw = Column(Text, nullable=True)
    repc = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('ix_representadas_rep_cod', 'rep_cod'),
        Index('ix_representadas_rep_nome', 'rep_nome'),
        {'schema': 'public'}
    )
#Moedas
class Moedas(Base):
    __tablename__ = "moedas"

    mo_cod = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mo_nome = Column(String(6), nullable=True, index=True)
    simbolo = Column(String(10), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('ix_mo_cod', 'mo_cod'),
        Index('ix_mo_nome', 'mo_nome'),
        {'schema': 'public'}
    )