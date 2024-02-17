import src.pysql.pySQL as sqlconn
import conn as conn

# import pandas as pd
# from datetime import datetime


def SQL_connector():
    ssh = sqlconn.SSHtunnel(
        ssh_host=conn.ssh_host,
        ssh_username=conn.ssh_username,
        ssh_password=conn.ssh_password,
        remote_bind_address=conn.remote_bind_address,
    )
    tunnel = ssh.create_tunnel()
    tunnel.start()
    sql = sqlconn.SQL(
        host=conn.host,
        database=conn.database,
        user=conn.user,
        password=conn.password,
        port=tunnel.local_bind_port,
        connect_type="MySQL",
    )

    return sql


# def load_log_table(
#    table_name: str, table_shape: pd.DataFrame.shape, success: bool, error: str = None
# ):
#    name: str = "data_log"
#    if success:
#        result = "succes"
#    else:
#        result = "failed"
#    df = pd.DataFrame(
#        {
#            "table_name": [table_name],
#            "updated_at": [datetime.now()],
#            "table_shape": [str(table_shape)],
#            "result": [result],
#            "error": [error],
#        }
#    )
#    sql.load_data_to_SQL(df=df, table=name)
#
#
# def data_loader(name: str, df: pd.DataFrame, truncate: bool = True):
#    try:
#        sql.load_data_to_SQL(
#            df=df,
#            table=name,
#            truncate=truncate,
#        )
#        success = True
#        error_message = None
#    except Exception as e:
#        success = False
#        error_message = str(e)
#        print(f"\033[91m {error_message} \033[0m")
#    load_log_table(
#        table_name=name, table_shape=df.shape, success=success, error=error_message
#    )
#
#
# def __delete_last_coma(element_list: list):
#    if len(element_list) > 1:
#        return str(tuple(element_list))
#    string = str(tuple(element_list))
#    last_comma_index = string.rfind(",")
#    if last_comma_index != -1:
#        modified_string = string[:last_comma_index] + string[last_comma_index + 1 :]
#        return modified_string
#
#
# def get_data_test():
#    with open("./SQL/SQL_queries/test.sql", "r") as file:
#        query = file.read()
#    params = {
#        "season": f"'FT'",
#    }
#    df = sql.get_data_from_query(query=query, params=params)
#
#    print(df)
#
#
# def get_standings_data(season):
#    with open("./SQL/SQL_queries/standings/standings_general.sql", "r") as file:
#        query = file.read()
#
#    params = {
#        "season": f"{season}",
#    }
#    df = sql.get_data_from_query(query=query, params=params)
#
#    return df
#
#
# def get_fixtures_data():
#    with open("./SQL/SQL_queries/fixtures/fixtures.sql", "r") as file:
#        query = file.read()
#
#    df = sql.get_data_from_query(query=query)
#
#    return df
#
#
# if "__main__" == __name__:
#    get_standings_data(season=2023)
#
