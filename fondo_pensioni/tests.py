from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants, Player

import random


class PlayerBot(Bot):

    def play_round(self):
        # Only on first round
        if self.round_number == 1:
            print(Player.experience)
            yield (pages.Introduction)
            yield (pages.Questionario,
                   {
                       'crt_bat': "Impiegato normale",
                       'experience': random.choice(
                           Player._meta.get_field('experience').choices),
                       'sector': random.choice(
                           Player._meta.get_field('sector').choices),
                       'education': random.choice(
                           Player._meta.get_field('education').choices),
                       'age': random.choice(
                           Player._meta.get_field('age').choices),
                       'gender': random.choice(
                           Player._meta.get_field('gender').choices),
                   })

        yield (pages.Investi, {'contribution': random.randint(1,100)})
        # yield (pages.Results)
        pass
