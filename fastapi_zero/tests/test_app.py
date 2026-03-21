from http import HTTPStatus

from fastapi.testclient import TestClient  # recurso da propria FastAPI

from fastapi_zero.app import app  # importando da pasta o nosso arquivo


def test_root_retorna_ola_mundo():  # toda função em teste começa com test_

    # arrange
    client = TestClient(app)  # cliente de teste do FastAPI

    # act - execução (SUT - system under test)
    response = client.get("/")

    # assert - garantir que A = A
    assert response.json() == {"message": "API funcionando"}
    # garante que veio a resposta que esperava
    assert response.status_code == HTTPStatus.OK
