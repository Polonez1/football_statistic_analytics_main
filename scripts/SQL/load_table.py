# import scripts.SQL.ssh_sql_connector as conn
from datetime import datetime
import pandas as pd

# sql = conn.SQL_connector()


def load_log_table(
    sqlengine,
    table_name: str,
    table_shape: pd.DataFrame.shape,
    success: bool,
    error: str = None,
):
    name: str = "data_log"
    if success:
        result = "succes"
    else:
        result = "failed"
    df = pd.DataFrame(
        {
            "table_name": [table_name],
            "updated_at": [datetime.now()],
            "table_shape": [str(table_shape)],
            "result": [result],
            "error": [error],
        }
    )
    sqlengine.load_data_to_SQL(df=df, table=name)


def data_loader(sqlengine, name: str, df: pd.DataFrame, truncate: bool = True):
    try:
        sqlengine.load_data_to_SQL(
            df=df,
            table=name,
            truncate=truncate,
        )
        success = True
        error_message = None
    except Exception as e:
        success = False
        error_message = str(e)
        print(f"\033[91m {error_message} \033[0m")
    load_log_table(
        table_name=name, table_shape=df.shape, success=success, error=error_message
    )
