from peewee import *

from models.model_manager import DATA_BASE


class Search(Model):
    whole_words = BooleanField(default=False)
    case_sensitively = BooleanField(default=False)

    def changeStateWholeWord(self):
        if self.whole_words is False:
            self.whole_words = True
            self.save()
        else:
            self.whole_words = False
            self.save()

    def changeStateCaseSensitively(self):
        if self.case_sensitively is False:
            self.case_sensitively = True
            self.save()
        else:
            self.case_sensitively = False
            self.save()

    class Meta:
        database = DATA_BASE
