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
    players_per_group = 6
    #players_per_group =2
    num_rounds = 10  # TODO deve essere 100
    instructions_template = "fondo_pensioni/Instructions.html"

    # R = c(0.05)
    R = 0.05

    # D = c(3)
    D = 3.0

    F = c(49)

    S = c(1300)

    endowment = 1000

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

    @property
    def last_payoff(self):
        """
        Guadagno dell'ultimo investimento.
        """

        player_in_previous_rounds = self.in_previous_rounds()

        # Se la lista non e' vuota, restituisci il payoff dell'ultimo periodo
        if player_in_previous_rounds:
            return player_in_previous_rounds[-1].payoff
        # Altrimenti, zero
        else:
            return 0

    @property
    def total_payoff(self):
        """
        Guadagno totale dato dalla somma di tutti i guadagni fino al round
        attuale (incluso).
        """
        tp = 0
        for p in self.in_previous_rounds():
            tp += p.payoff

        tp += self.payoff

        return tp
