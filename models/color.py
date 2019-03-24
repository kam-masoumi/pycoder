from peewee import *

from models.model_manager import DATA_BASE


class ColorScheme(Model):
    keywords = CharField(max_length=15, default='#E36209')
    builtin = CharField(max_length=15, default='#660099')
    comment = CharField(max_length=15, default='#FF0000',)
    quotation = CharField(max_length=15, default='#008000')
    function = CharField(max_length=15, default='#005CC5')
    decorator = CharField(max_length=15, default='#6699FF')
    dark_theme = BooleanField(default=False)

    def changeTheme(self):
        if self.dark_theme is False:
            self.dark_theme = True
            self.save()
        else:
            self.dark_theme = False
            self.save()

    def setDefault(self):
        self.keywords = '#E36209'
        self.builtin = '#660099'
        self.comment = '#FF0000'
        self.quotation = '#008000'
        self.function = '#005CC5'
        self.decorator = '#669r9FF'
        self.save()

    class Meta:
        database = DATA_BASE
