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


# class Contribute(Page):
    # form_model = 'player'
    # form_fields = ['contribution']

def build_series(player, group, round_number):

    values_price = list()
    values_prediction = list()


    player_in_previous_rounds = player.in_previous_rounds()
    group_in_previous_rounds = group.in_previous_rounds()

    for i in range(len(player_in_previous_rounds)):
        rn = i + 1

        p = player_in_previous_rounds[i]
        g = group_in_previous_rounds[i]

        values_prediction.append(p.contribution)

        if rn > (round_number - 2):
            values_price.append(None)
        else:
            values_price.append(g.price)

    # Serve per dopo
    rn = len(player_in_previous_rounds) + 1

    # for i in range(round_number-1):
    for i in range(Constants.num_rounds - rn):
        values_price.append(None)
        values_prediction.append(None)

    series_price = {
        'name': "Prezzo",
        'data': values_price
    }

    series_prediction = {
        'name': "Previsione",
        'data': values_prediction
    }

    return [series_prediction, series_price]


class Investi(Page):

    form_model = 'giocatore'
    form_fields = ['previsione']

    def vars_for_template(self):
        # highcharts_series = get_fake_hc_series(self.round_number)
        highcharts_series = build_series(
            self.player, self.group, self.round_number)

        series_df = pd.DataFrame(columns=['Periodo', 'Previsione', 'Prezzo'])
        series_df['Previsione'] = highcharts_series[0]['data']
        series_df['Prezzo'] = highcharts_series[1]['data']

        # print(series_df.shape)
        # print(len(range(1, Constants.num_rounds)))

        # Numero di round totali:
        series_df['Periodo'] = range(1, Constants.num_rounds)

        rn = self.round_number
        series_df = series_df[series_df['Periodo'] < rn]
        series_df = series_df[series_df['Periodo'] >= rn-20]

        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'highcharts_series': highcharts_series,
            'tasso_di_interesse': "{:.2f}%".format(Constants.R*100),
            'Dividendo': "{:.2f}%".format(Constants.D),
            'Prezzi_generati': series_df.to_html(
                index=False, classes=['table', 'table-sm'])
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        group = self.group
        group_in_previous_rounds = group.in_previous_rounds()
        group.prev = group.in_previous_rounds[len(group_in_previous_rounds)-1]
        players = group.get_players()
        contributions = [p.contribution for p in players]
        group.mean_contribution = sum(contributions)/Constants.players_per_group
        group.price = (group.mean_contribution + Constants.D)/(1 + Constants.R)
        for p in players:
            p.guess = p.contribution
        if group.price == p.contribution:
            p.payoff = Constants.S
        else:
            #p.payoff = max(Constants.S-(Constants.S/(Constants.F*(group.price.in_previous_rounds[len(group_in_previous_rounds)-1] - p.contribution)**2)),0)
            p.payoff = max(Constants.S-(Constants.S/(Constants.F*(group.prev.price - p.contribution)**2)),0)


class Results(Page):
    pass


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    Introduction,  # TODO disabilitata per debug
    Investi,
    ResultsWaitPage,
    Results
]
