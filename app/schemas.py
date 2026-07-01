from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str


class TarefaCreate(BaseModel):
    titulo: str
    descricao: str
    prioridade: str
    status: str


class Login(BaseModel):
    email: str