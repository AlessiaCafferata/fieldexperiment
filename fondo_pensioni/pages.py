from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):

    def is_displayed(self):
        """
        Questa pagina deve essere visualizzata solamente all'inizio, quindi
        nel primo round.
        """

        return self.round_number == 1

class Investi(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Introduction,
    Investi,
    ResultsWaitPage,
    Results
]
