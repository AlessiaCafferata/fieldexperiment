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
    # players_per_group = 6
    players_per_group =2
    num_rounds = 10  # TODO deve essere 100
    instructions_template = "fondo_pensioni/Instructions.html"

    R = c(0.05)
    D = c(3)
    F = c(49)
    S = c(1300)

    endowment = 100

class Subsession(BaseSubsession):

    def price_update(self):
        contributions = [p.contribution for p in self.get_players()]
        return (sum(contributions)/Constants.players_per_group+Constants.D)/(1+Constants.R)

class Group(BaseGroup):
    mean_contribution = models.CurrencyField()
    price = models.CurrencyField()

    pass


class Player(BasePlayer):

    contribution = models.CurrencyField(
        min=0, max=Constants.endowment
    )

    guess = models.CurrencyField()

    payoff = models.CurrencyField()



