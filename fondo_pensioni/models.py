from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django.core.validators import MinValueValidator, MaxValueValidator

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'fondo_pensioni'
    players_per_group = 6
    # players_per_group =2
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
        min=0, max=Constants.endowment,
        verbose_name="Contributo"
    )

    payoff = models.CurrencyField()

    # Campi per il questionario
    crt_bat = models.StringField(
        verbose_name='''
            Qual è il tuo impiego attuale?'''
    )

    experience = models.StringField(
        choices=['0-5', '6-10', '11-15', '16-20', '21+'],
        verbose_name='Da quanti anni lavori nei mercati finanziari?',
        widget=widgets.RadioSelect)

    sector = models.StringField(
        choices=['Spot', 'Derivati', 'Futures', 'Altro'],
        verbose_name='In quale ambito di mercato svolgi la tua attività?'
    )

    education = models.StringField(
        choices=['Laurea', 'Master', 'Dottorato', 'Altro'],
        verbose_name='Qual è il tuo livello di istruzione?'
    )

    age = models.StringField(
        choices=['20-30', '31-40', '41-50', '51-60', '60+'],
        verbose_name='Quanti anni hai?'
    )

    gender = models.StringField(
        choices=['Uomo', 'Donna'],
        verbose_name='Di che sesso sei?',
        widget=widgets.RadioSelect)

    domanda_controllo_1 = models.FloatField(
        verbose_name='Domanda 1: La tua previsione è pari a 34,38 '
        'mentre il prezzo di mercato è 28,02. Qual è in questo caso '
        'il tuo guadagno (in punti?)',
        validators=[
            MinValueValidator(230, message="SBAGLIATO. La tua risposta non è "
                              "corretta. Calcola nuovamente il tuo errore di "
                              "previsione e successivamente consulta i punti "
                              "nella tabella."),
            MaxValueValidator(230, message="SBAGLIATO. La tua risposta non è "
                              "corretta. Calcola nuovamente il tuo errore di "
                              "previsione e successivamente consulta i punti "
                              "nella tabella."),
        ]
    )

    domanda_controllo_2 = models.FloatField(
        verbose_name='La tua previsione è pari a 88.33 mentre il prezzo di '
        'mercato è 86.11. Qual è in questo caso il tuo guadagno (in punti?)',
        validators=[
            MinValueValidator(1172, message="SBAGLIATO”. La tua risposta non è "
                              "corretta. Calcola nuovamente il tuo errore di "
                              "previsione e successivamente consulta i punti "
                              "nella tabella."),
            MaxValueValidator(1172, message="SBAGLIATO”. La tua risposta non è "
                              "corretta. Calcola nuovamente il tuo errore di "
                              "previsione e successivamente consulta i punti "
                              "nella tabella."),
        ]
    )

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
