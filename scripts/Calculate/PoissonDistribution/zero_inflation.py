import pandas as pd


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


if "__main__" == __name__:
    df = pd.DataFrame(
        {
            "goals_result": ["0-1", "0-0", "1-1", "2-0", "3-3"],
            "count": [10, 10, 50, 10, 20],
        }
    )

    df2 = pd.DataFrame(
        {
            "goals_result": ["0-1", "0-0", "1-1", "2-0", "3-3"],
            "count": [5, 10, 55, 10, 20],
        }
    )
    params = zero_inflation_koef(source_data=df, skellam_data=df2)
    print(params)
