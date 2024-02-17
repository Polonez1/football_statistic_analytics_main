import ssh_sql_connector as conn
import pandas as pd


sql = conn.SQL_connector()


def get_data_test():
    with open("./scripts/SQL/SQL_queries/test.sql", "r") as file:
        query = file.read()
    params = {
        "feature": f"'FT'",
    }
    df = sql.get_data_from_query(query=query, params=params)
    if type(df) == pd.DataFrame:
        print("test ok")
    else:
        print("test error")


if "__main__" == __name__:
    df = get_data_test()
