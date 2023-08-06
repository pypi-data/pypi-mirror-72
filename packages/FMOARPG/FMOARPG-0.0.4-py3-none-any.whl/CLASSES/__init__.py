from enum import Enum

class Conteudo:
    nome = ""
    conteudoId = ""
    pjtId = ""
    items = []
    fullPath = []
    tipo = ""
    customAtts = []
    def __init__(self, Nome, contID, pjtID):
        self.nome = Nome
        self.conteudoId = contID
        self.pjtId = pjtID
        self.items = []
        self.fullPath = []


class Tipo(Enum):
    PASTA = 1
    ARQUIVO = 2


class Atividade:
    data = ""
    generator = ""
    agente_nome = ""
    agente_email = ""
    agente_tipo = ""
    verb = ""
    objeto_displayName = ""
    objeto_id = ""
    objeto_tipo = ""
    projeto_id = ""
    projeto_nome = ""
    def __init__(self, Data, gerador, AgntNome, Verbo, ObjNome, ObjId, PjtId, PjtNome):
        self.data = Data
        self.generator = gerador
        self.agente_nome = AgntNome
        self.verb = Verbo
        self.objeto_displayName = ObjNome
        self.objeto_id = ObjId
        self.projeto_id = PjtId
        self.projeto_nome = PjtNome


class CustomAttribute:
    fullpath = []
    name = ""
    value = ""
    def __init__(self, Nome, Valor):
        self.name = Nome
        self.value = Valor


class MapHub:
    hubName = ""
    hubId = ""
    projetos = []
    def __init__(self, hubNome, hubid):
        self.hubName = hubNome
        self.hubId = hubid


class Projeto:
    nome = ""
    pjtId = ""
    hubId = ""
    city = ""
    state_or_province = ""
    status = ""
    country = ""
    start_date = ""
    end_date = ""
    project_type = ""
    construction_type = ""
    Items = []
    container = ""
    def __init__(self, name, pjtID, hubID, container):
        self.Nome = name
        self.pjtId = pjtID
        self.hubId = hubID
        self.container = container
        self.Items = []


class Token:
    access_token = ""
    token_type = ""
    expires_in = 0
    date_origin = None
    def __init__(self, token, tipo, validade, tempo):
        self.access_token = token
        self.token_type = tipo
        self.expires_in = validade
        self.date_origin = tempo


class User:
    userId = ""
    nome = ""
    email = ""
    role = ""
    roleId = ""
    doc_man_access = ""
    insight_access = ""
    project_admin_access = ""
    def __init__(self, userID, Email, Nome, Role, RoleID):
        self.userId = userID
        self.email = Email
        self.role = Role
        self.roleId = RoleID
        self.nome = Nome

class Issue:
    created_at = ""
    updated_at = ""
    closed_at = ""
    closed_by = ""
    created_by = ""
    opened_at = ""
    opened_by = ""
    updated_by = ""
    title = ""
    description = ""
    due_date = ""
    due_date = ""
    status = ""
    assigned_to = ""
    assigned_to_type = ""
    created_at = ""
    created_by = ""