from fastapi_zero.models.user import User


class Command:
    def execute(self):
        raise NotImplementedError()


class CriarUserCommand(Command):
    def __init__(self, db, user_data):
        self.db = db
        self.user_data = user_data

    def execute(self):
        user = User(**self.user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class AtualizarUserCommand(Command):
    def __init__(self, db, db_user, user_data):
        self.db = db
        self.db_user = db_user
        self.user_data = user_data

    def execute(self):
        for key, value in self.user_data.items():
            setattr(self.db_user, key, value)

        self.db.commit()
        self.db.refresh(self.db_user)
        return self.db_user
