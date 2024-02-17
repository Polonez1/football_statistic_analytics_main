# import scripts.SQL.ssh_sql_connector as conn
import pandas as pd

# sql = conn.SQL_connector()


def get_standings_data(sqlengine, season):
    with open("./scripts/SQL/SQL_queries/standings/standings_general.sql", "r") as file:
        query = file.read()

    params = {
        "season": f"{season}",
    }
    df = sqlengine.get_data_from_query(query=query, params=params)

    return df


def get_fixtures_data(sqlengine):
    with open("./scripts/SQL/SQL_queries/fixtures/fixtures.sql", "r") as file:
        query = file.read()

    df = sqlengine.get_data_from_query(query=query)

    return df
