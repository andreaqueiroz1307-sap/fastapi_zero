from fastapi_zero.auth import hash_senha
from fastapi_zero.models.category import Category
from fastapi_zero.models.user import User


class Command:
    def execute(self):
        raise NotImplementedError()


class CriarUserCommand(Command):
    def __init__(self, db, user_data):
        self.db = db
        self.user_data = user_data

    def execute(self):
        dados = self.user_data.copy()
        dados['senha'] = hash_senha(dados['senha'])

        user = User(**dados)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        categoria_padrao = Category(
            nome='TODAS',
            user_id=user.id,
        )
        self.db.add(categoria_padrao)
        self.db.commit()
        self.db.refresh(user)

        return user


class AtualizarUserCommand(Command):
    def __init__(self, db, db_user, user_data):
        self.db = db
        self.db_user = db_user
        self.user_data = user_data

    def execute(self):
        dados = self.user_data.copy()

        if 'senha' in dados:
            dados['senha'] = hash_senha(dados['senha'])

        for key, value in dados.items():
            setattr(self.db_user, key, value)

        self.db.commit()
        self.db.refresh(self.db_user)
        return self.db_user