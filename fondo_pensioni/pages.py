from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random


class Introduction(Page):

    def is_displayed(self):
        """
        Questa pagina deve essere visualizzata solamente all'inizio, quindi
        nel primo round.
        """

        return self.round_number == 1

def get_fake_hc_series(round_number):

    values_price = list()
    values_prediction = list()

    # for i in range(round_number-1):
    for i in range(20):
        values_price.append(random.randint(1, 100))
        values_prediction.append(random.randint(1, 100))

    # for i in range(round_number-1):
    for i in range(5):
        values_price.append(None)
        values_prediction.append(None)

    series_price = {
        'name': "Price",
        'data': values_price
    }

    series_prediction = {
        'name': "Prediction",
        'data': values_prediction
    }

    return [series_price, series_prediction]

class Investi(Page):

    form_model = 'player'
    form_fields = ['investimento']


    def vars_for_template(self):
        highcharts_series = get_fake_hc_series(self.round_number)

        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'highcharts_series': highcharts_series
        }



class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    # Introduction,  # TODO disabilitata per debug
    Investi,
    ResultsWaitPage,
    Results
]
