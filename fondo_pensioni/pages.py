from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random

import pandas as pd

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
    for i in range(95):
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

    return [series_prediction, series_price]

class Investi(Page):

    form_model = 'player'
    form_fields = ['investimento']


    def build_series(self):

        values_price = list()
        values_prediction = list()

        # for i in range(round_number-1):
        # for i in range(95):
            # values_price.append(random.randint(1, 100))
            # values_prediction.append(random.randint(1, 100))

        rn = 1
        for p in self.player.in_previous_rounds():

            values_prediction.append(p.investimento)

            if rn > (self.round_number - 2):
                values_price.append(None)
            else:
                values_price.append(p.price)

            rn += 1

        # for i in range(round_number-1):
        for i in range(Constants.num_rounds - rn):
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

        return [series_prediction, series_price]

    def vars_for_template(self):
        # highcharts_series = get_fake_hc_series(self.round_number)
        highcharts_series = self.build_series()

        series_df = pd.DataFrame(columns=['Round', 'Prediction', 'Price'])
        series_df['Prediction'] = highcharts_series[0]['data']
        series_df['Price'] = highcharts_series[1]['data']

        print(series_df.shape)
        print(len(range(1, Constants.num_rounds + 1)))

        # Numero di round totali: 100 - 1
        series_df['Round'] = range(1, Constants.num_rounds)

        # TODO debug, to remove
        # series_df = series_df.head(20)

        # rn = 24
        rn = self.round_number
        series_df = series_df[series_df['Round'] < rn]
        series_df = series_df[series_df['Round'] >= rn-20]


        # print(series_df)

        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'highcharts_series': highcharts_series,
            'series_df_html': series_df.to_html(
                index=False, classes=['table', 'table-sm'])
        }



class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_price()


class Results(Page):
    pass


page_sequence = [
    # Introduction,  # TODO disabilitata per debug
    Investi,
    ResultsWaitPage,
    # Results
]