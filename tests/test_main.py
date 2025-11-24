from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


def test_listar_alunos():
    response = client.get("/alunos")
    assert response.status_code == 200
    assert "alunos" in response.json()


def test_criar_aluno():
    novo_aluno = {
        "nome": "Gabriel Henrique",
        "email": "gabriel.email@example.com",
    }
    response = client.post("/alunos", json=novo_aluno)
    assert response.status_code == 200
    assert response.json()["aluno"]["nome"] == "Gabriel Henrique"


def test_criar_aluno_dados_incompletos():
    aluno_incompleto = {"nome": "Somente nome"}
    response = client.post("/alunos", json=aluno_incompleto)
    assert response.status_code == 200
    assert response.json()["aluno"]["email"] is None


@pytest.mark.xfail(reason="Este teste demonstra uma falha esperada.")
def test_criar_aluno_sem_campo_obrigatorio():
    response = client.post(
        "/alunos",
        json={"email": "semnome@example.com"},
    )
    assert response.status_code == 422
    assert "Campo 'nome' é obrigatório" in response.json()["detail"]

# Novos Testes

def test_get_existing_aluno():
    aluno_id = 1
    response = client.get(f"/alunos/{aluno_id}")
    assert response.status_code == 200
    assert response.json() == {
        "aluno": {
            "id": 1,
            "nome": "Gabriel Henrique",
            "email": "gabriel.email@example.com"
        }
    }

def test_get_notexisting_aluno():
    aluno_id = 999
    response = client.get(f"/alunos/{aluno_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Aluno não encontrado"}