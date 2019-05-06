from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'fondo_pensioni'
    players_per_group = None
    # num_rounds = 4  # TODO deve essere 100
    num_rounds = 100  # TODO deve essere 100
    instructions_template = "fondo_pensioni/Instructions.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    def set_price(self):

        player = self.get_players()[0]
        print(player)

        player.price = 75

        print("In set_price:")


class Player(BasePlayer):

    price = models.CurrencyField(
        min=0,
        # label="Quanto vuoi investire?"
    )

    investimento = models.CurrencyField(
        min=0,
        # label="Quanto vuoi investire?"
        label="What is your prediction for the next period?"
    )


    pass
