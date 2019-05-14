from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import datetime

import pandas as pd


class Introduction(Page):

    def is_displayed(self):
        """
        Questa pagina deve essere visualizzata solamente all'inizio, quindi
        nel primo round.
        """

        return self.round_number == 1


class Questionario(Page):

    def is_displayed(self):
        """
        Questa pagina deve essere visualizzata solamente all'inizio, quindi
        nel primo round.
        """

        return self.round_number == 1

    form_model = 'player'
    form_fields = ['crt_bat', 'experience', 'sector', 'education', 'age',
                   'gender']


class Controllo1(Page):

    def is_displayed(self):
        """
        Questa pagina deve essere visualizzata solamente all'inizio, quindi
        nel primo round.
        """

        return self.round_number == 1

    form_model = 'player'
    form_fields = ['domanda_controllo_1']


class Controllo2(Page):

    def is_displayed(self):
        """
        Questa pagina deve essere visualizzata solamente all'inizio, quindi
        nel primo round.
        """

        return self.round_number == 1

    form_model = 'player'
    form_fields = ['domanda_controllo_2']


class QuestionarioWaitPage(WaitPage):

    def is_displayed(self):
        """
        Questa pagina deve essere visualizzata solamente all'inizio, quindi
        nel primo round.
        """

        return self.round_number == 1


    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()

        questionario_txt_file = "sessione_{}.txt".format(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

        with open(questionario_txt_file, 'w') as qf:

            for p in players:

                qf.write("Giocatore {}:\n".format(p.id_in_group))

                # Campi per il questionario
                qf.write("Impiego attuale: {}\n".format(p.crt_bat))
                qf.write("Esperienza (anni): {} \n".format(p.experience))
                qf.write("Ambito di mercato: {}\n".format(p.sector))
                qf.write("Livello d'istruzione: {}\n".format(p.sector))
                qf.write("Eta': {}\n".format(p.age))
                qf.write("Sesso: {}\n".format(p.gender))

                qf.write("\n")

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

    form_model = 'player'
    form_fields = ['contribution']

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
            'interest_rate': "{:.2f}%".format(Constants.R*100),
            'mean_dividend': "{:.2f}%".format(Constants.D),
            'series_df_html': series_df.to_html(
                index=False, classes=['table', 'table-sm'])
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):

        group = self.group
        players = group.get_players()

        contributions = [p.contribution for p in players]
        group.mean_contribution = float(sum(contributions))/Constants.players_per_group
        group.price = float(group.mean_contribution + Constants.D)/(1 + Constants.R)

        if self.round_number > 1:

            group_in_previous_rounds = group.in_previous_rounds()

            # Il gruppo al round precedente
            group_in_previous_round = group_in_previous_rounds[len(group_in_previous_rounds)-1]

            # TODO da cancellare?
            for p in players:
                # p.guess = p.contribution

                if group.price == p.contribution:
                    p.payoff = Constants.S
                else:

                    # if (group_in_previous_round.price - p.contribution) == 0:
                        # print(20*"#")
                        # print(20*"#")
                        # print(20*"#")
                        # print(group_in_previous_round.price)
                        # print(p.contribution)

                    denominator = (
                        Constants.F *
                        # XXX Occhio, questo denominatore qualche
                        # volta si azzera
                        (group_in_previous_round.price - p.contribution)**2)

                    # XXX occhio qui
                    if denominator == 0:
                        denominator = 0.1

                    p.payoff = max(
                        Constants.S - (
                            Constants.S / denominator),
                        0)

        else:
            for p in players:
                # TODO da controllare
                p.payoff = 0


class Results(Page):
    pass


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    Introduction,
    Controllo1,
    Controllo2,
    Questionario,
    QuestionarioWaitPage,
    Investi,
    ResultsWaitPage,
    # Results
]
