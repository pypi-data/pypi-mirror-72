import pyodbc

def exec_sql_srv_proc(sql_srv: str, db_name: str, usr_name: str, usr_pass: str, proc_name: str):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f"SERVER={sql_srv};"
        f"DATABASE={db_name};UID={usr_name};"
        f"PWD={usr_pass}"
    )

    conn.execute(f"EXEC {proc_name}")
    conn.commit()

    conn.close()