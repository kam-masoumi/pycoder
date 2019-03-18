from peewee import SqliteDatabase

DATA_BASE = SqliteDatabase('pycoder.db')
DATA_BASE.connect()


class ModelManager:

    @staticmethod
    def create_model(data_base):
        DATA_BASE.create_tables([data_base], safe=True)
        return True
