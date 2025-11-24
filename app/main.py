from fastapi import FastAPI, HTTPException

app = FastAPI()

db = {
    1: {
        "id": 1,
        "nome": "Gabriel Henrique",
        "email": "gabriel.email@example.com",
    },
    2: {
        "id": 2,
        "nome": "João Henrique",
        "email": "joao.email@example.com",
    },
}


@app.get("/alunos")
def listar_alunos():
    return {"alunos": list(db.values())}


@app.get("/alunos/{aluno_id}")
def buscar_aluno(aluno_id: int):
    if aluno_id not in db:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"aluno": db[aluno_id]}


@app.post("/alunos")
def criar_aluno(aluno: dict):
    novo_id = max(db.keys()) + 1 if db else 1
    db[novo_id] = {
        "id": novo_id,
        "nome": aluno.get("nome"),
        "email": aluno.get("email"),
    }
    return {"aluno": db[novo_id]}
