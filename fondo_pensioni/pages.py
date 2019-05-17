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
    title_text = "Attendere prego..."
    body_text = "Attendere prego..."

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


def build_series(player, group, round_number):

    values_price = list()
    # values_prediction = list()
    values_prediction = [None]

    player_in_previous_rounds = player.in_previous_rounds()
    group_in_previous_rounds = group.in_previous_rounds()

    # for i in range(len(player_in_previous_rounds)):
        # p = player_in_previous_rounds[i]
        # print("Round {}: c: {}".format(i+1, p.contribution))

    for i in range(len(player_in_previous_rounds)):

        p = player_in_previous_rounds[i]
        g = group_in_previous_rounds[i]

        values_prediction.append(p.contribution)
        values_price.append(g.price)

    # Hide last price
    # values_price[-1] = None

    values_price.append(None)

    # Il turno attuale
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


    # print(len(series_price['data']))

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
        # print(len(range(2, Constants.num_rounds + 1)))

        # Numero di round totali:
        series_df['Periodo'] = range(1, Constants.num_rounds + 1)

        rn = self.round_number

        # if rn == 1:
            # # Taglia la prima riga relativa al periodo 1
            # series_df = series_df.iloc[1:, :]

        # Taglia la prima riga relativa al periodo 1
        series_df = series_df.iloc[1:, :]

        # print(series_df)

        series_df = series_df[series_df['Periodo'] <= rn]
        series_df = series_df[series_df['Periodo'] > rn-20]

        # Sostituire "None" con "" (stringa vuota)
        series_df_fixed = series_df.copy()
        mask = series_df.applymap(lambda x: x is None)
        cols = series_df.columns[(mask).any()]
        for col in series_df_fixed[cols]:
            series_df_fixed.loc[mask[col], col] = ''

        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'highcharts_series': highcharts_series,
            'interest_rate': "{:.2f}%".format(Constants.R*100),
            'mean_dividend': "{:.2f}".format(Constants.D),
            'series_df_html': series_df_fixed.to_html(
                index=False, classes=['table', 'table-sm'], na_rep="")
        }


def compute_price(contributions):
    """
    Compute the price at round t, given the contributions of players
    """

    mean_contribution = float(sum(contributions))/Constants.players_per_group
    price = float(mean_contribution + Constants.D)/(1 + Constants.R)

    return price


def compute_payoff(player_prediction, price):
    """
    Calcola il guadagno
    """

    coefficient = (price - player_prediction)**2

    payoff = max(
        Constants.S - ((Constants.S/Constants.F)*coefficient),
        0)

    return payoff


class ResultsWaitPage(WaitPage):

    title_text = "Attendere prego..."
    body_text = "Attendere prego..."

    def after_all_players_arrive(self):

        group = self.group
        players = group.get_players()

        if self.round_number > 1:

            contributions = list()

            for p in players:

                player_in_previous_rounds = p.in_previous_rounds()
                # Il player al round precedente p_tm1 = player at t minus 1
                p_tm1 = player_in_previous_rounds[
                    len(player_in_previous_rounds)-1]

                contributions.append(p_tm1.contribution)

            group.price = compute_price(contributions)

            for p in players:

                player_in_previous_rounds = p.in_previous_rounds()
                # Il player al round precedente p_tm1 = player at t minus 1
                p_tm1 = player_in_previous_rounds[
                    len(player_in_previous_rounds)-1]

                p_tm1.contribution
                # Calcola il guadagno al turno corrente
                payoff = compute_payoff(p_tm1.contribution, group.price)
                p.payoff = payoff

        else:
            for p in players:
                # TODO da controllare
                p.payoff = 0


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    # Introduction,
    # Controllo1,
    # Controllo2,
    # Questionario,
    # QuestionarioWaitPage,
    Investi,
    ResultsWaitPage,
    FinalResults,
]
