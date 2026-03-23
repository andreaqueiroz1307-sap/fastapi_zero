from http import HTTPStatus


def test_root_retorna_mensagem(client):
    response = client.get("/")
    assert response.json() == {"message": "API funcionando"}
    assert response.status_code == HTTPStatus.OK


def test_criar_user(client):
    response = client.post(
        "/users",
        json={
            "nome": "Andrea",
            "email": "AandreaQueiroz1307@gmail.com",
            "senha": "1234##",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "nome": "Andrea",
        "email": "AandreaQueiroz1307@gmail.com",
    }


def test_listar_users(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK


def test_criar_task(client):
    response = client.post(
        "/tarefas",
        json={
            "titulo": "Estudar API",
            "descricao": "Fazer a API em python",
            "prioridade": "alta",
            "user_id": 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "titulo": "Estudar API",
        "descricao": "Fazer a API em python",
        "prioridade": "alta",
        "concluida": False,
    }


def test_listar_tarefas(client):
    response = client.get("/tarefas")
    assert response.status_code == HTTPStatus.OK


def test_atualizar_user(client):

    response = client.post(
        "/users",
        json={
            "nome": "Andrea",
            "email": "teeste@teste.com",
            "senha": "1234##",
        },
    )

    response = client.put(
        "/users/1",
        json={
            "nome": "Andrea Queiroz",
            "email": "aandrea@teste.com",
            "senha": "1234##",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "nome": "Andrea Queiroz",
        "email": "aandrea@teste.com",
    }
