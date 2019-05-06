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
    num_rounds = 4  # TODO deve essere 100
    instructions_template = "fondo_pensioni/Instructions.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):


    investimento = models.CurrencyField(
        min=0,
        label="Quanto vuoi investire?"
    )


    pass
