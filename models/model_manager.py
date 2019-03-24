from peewee import SqliteDatabase

DATA_BASE = SqliteDatabase('pycoder.db')
DATA_BASE.connect()


class ModelManager:

    @staticmethod
    def create_model(table):
        DATA_BASE.create_tables([table], safe=True)
        if len(table) == 0:
            table.create()
        return True
