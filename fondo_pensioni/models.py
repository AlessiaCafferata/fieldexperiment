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
    # num_rounds = 4  # TODO deve essere 100
    num_rounds = 100  # TODO deve essere 100
    instructions_template = "fondo_pensioni/Instructions.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    def set_price(self):

        player = self.get_players()[0]
        print(player)

        player.price = 75

        print("In set_price:")


class Player(BasePlayer):

    price = models.CurrencyField(
        min=0,
        # label="Quanto vuoi investire?"
    )

    investimento = models.CurrencyField(
        min=0,
        # label="Quanto vuoi investire?"
        label="What is your prediction for the next period?"
    )

    def build_series(self, round_number):

        values_price = list()
        values_prediction = list()

        # for i in range(round_number-1):
        # for i in range(95):
            # values_price.append(random.randint(1, 100))
            # values_prediction.append(random.randint(1, 100))

        rn = 1
        for p in self.in_previous_rounds():

            values_prediction.append(p.investimento)

            if rn > (round_number - 2):
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
