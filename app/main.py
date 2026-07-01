from fastapi import FastAPI, HTTPException, UploadFile, File
from .database import engine, Base, SessionLocal
from .models import Usuario, Tarefa
from .schemas import UsuarioCreate, TarefaCreate, Login

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"mensagem": "CloudTask AI SaaS funcionando!"}


# ==========================
# USUÁRIOS
# ==========================

@app.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate):

    db = SessionLocal()

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    db.close()

    return {
        "mensagem": "Usuário cadastrado com sucesso",
        "id": novo_usuario.id
    }


@app.get("/usuarios")
def listar_usuarios():

    db = SessionLocal()

    usuarios = db.query(Usuario).all()

    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        })

    db.close()

    return resultado


# ==========================
# TAREFAS
# ==========================

@app.post("/tarefas")
def criar_tarefa(tarefa: TarefaCreate):

    db = SessionLocal()

    nova_tarefa = Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        prioridade=tarefa.prioridade,
        status=tarefa.status
    )

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    db.close()

    return {
        "mensagem": "Tarefa criada com sucesso",
        "id": nova_tarefa.id
    }


@app.get("/tarefas")
def listar_tarefas():

    db = SessionLocal()

    tarefas = db.query(Tarefa).all()

    resultado = []

    for tarefa in tarefas:
        resultado.append({
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "prioridade": tarefa.prioridade,
            "status": tarefa.status
        })

    db.close()

    return resultado


@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa: TarefaCreate):

    db = SessionLocal()

    tarefa_db = db.query(Tarefa).filter(Tarefa.id == id).first()

    if not tarefa_db:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    tarefa_db.titulo = tarefa.titulo
    tarefa_db.descricao = tarefa.descricao
    tarefa_db.prioridade = tarefa.prioridade
    tarefa_db.status = tarefa.status

    db.commit()

    db.close()

    return {
        "mensagem": "Tarefa atualizada com sucesso"
    }


@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int):

    db = SessionLocal()

    tarefa_db = db.query(Tarefa).filter(Tarefa.id == id).first()

    if not tarefa_db:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    db.delete(tarefa_db)
    db.commit()

    db.close()

    return {
        "mensagem": "Tarefa excluída com sucesso"
    }


# ==========================
# LOGIN
# ==========================

@app.post("/login")
def login(login: Login):

    db = SessionLocal()

    usuario = db.query(Usuario).filter(
        Usuario.email == login.email
    ).first()

    db.close()

    if usuario:
        return {
            "mensagem": "Login realizado com sucesso!",
            "usuario": usuario.nome
        }

    return {
        "mensagem": "Usuário não encontrado."
    }


# ==========================
# UPLOAD DE ARQUIVOS
# ==========================

@app.post("/upload")
async def upload_arquivo(arquivo: UploadFile = File(...)):

    conteudo = await arquivo.read()

    with open(arquivo.filename, "wb") as f:
        f.write(conteudo)

    return {
        "mensagem": "Arquivo enviado com sucesso!",
        "arquivo": arquivo.filename
    }