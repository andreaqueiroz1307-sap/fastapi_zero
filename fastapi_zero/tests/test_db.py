from fastapi_zero.models.user import User


def test_creat_user():
    user = User(
        nome="Andrea", email="andreaqueiroz1307@gmail.com", senha="Fifi1307!"
    )

    assert user.nome == "Andrea"
