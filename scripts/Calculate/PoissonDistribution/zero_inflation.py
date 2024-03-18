import pandas as pd
import numpy as np
import statsmodels.api as sm

ZERO_RESULTS = [
    "0-0",
    "1-0",
    "2-0",
    "3-0",
    "4-0",
    "5-0",
    "6-0",
    "7-0",
    "8-0",
    "9-0",
    "10-0",
    "0-1",
    "0-2",
    "0-3",
    "0-4",
    "0-5",
    "0-6",
    "0-7",
    "0-8",
    "0-9",
    "0-10",
]


def __get_zero_count_matches(data: pd.DataFrame):
    df = data.loc[data["goals_result"].isin(ZERO_RESULTS)]
    zero_sum = df["count"].sum()
    return zero_sum


def __get_total_count_matches(data: pd.DataFrame):
    return data["count"].sum()


def __create_params(data: pd.DataFrame):
    zero_sum = __get_zero_count_matches(data=data)
    total_sum = __get_total_count_matches(data=data)
    percentage = zero_sum / total_sum
    return {
        "zero_sum_count": zero_sum,
        "total_sum_count": total_sum,
        "percentage": round(percentage, 2),
    }


def zero_inflation_koef(source_data: pd.DataFrame, skellam_data: pd.DataFrame):
    source_params = __create_params(data=source_data)
    skellam_params = __create_params(data=skellam_data)
    diff = source_params["percentage"] - skellam_params["percentage"]
    return {
        "source": source_params,
        "skellam": skellam_params,
        "diff_prc": round(diff, 2),
    }


# ---------------------------------------------------------#


def zero_probability(data):
    # Dopasowanie modelu Zero-Inflated Poisson za pomocą MLE
    model = sm.ZeroInflatedPoisson(data["count"], exog=None, inflation="logit")
    results = model.fit()

    # Pobranie prawdopodobieństwa wystąpienia zera
    zero_prob = results.predict()[0]
    return zero_prob


if "__main__" == __name__:

    # Dane dotyczące liczby goli w meczach piłkarskich
    goals = np.array([0, 2, 1, 0, 1, 3, 0, 0, 2, 1])

    # Przykładowe zmienne egzogeniczne
    ages = np.array([30, 25, 28, 32, 27, 29, 31, 26, 28, 27])

    # Dopasowanie modelu zero-inflated Poissona do danych za pomocą MLE
    model = sm.ZeroInflatedPoisson(goals, exog=ages, inflation="logit")
    results = model.fit()

    # Pobranie oszacowanych parametrów
    params = results.params

    # Obliczenie prawdopodobieństwa zerowego wyniku na podstawie oszacowanych parametrów
    zero_prob = np.exp(params[0]) / (1 + np.exp(params[0]))

    print("Prawdopodobieństwo wyniku 0:", zero_prob)
