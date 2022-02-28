import psycopg2

def write_to_db(conn, data_dict, table, return_col=""):
    cols= data_dict.keys()
    cols_val_list = [f'%({i})s' for i in cols]
    cols_val=", ".join(cols_val_list)
    cols=", ".join(cols)

    cur = conn.cursor()
    if return_col:
        sql = (
            f"""INSERT INTO {table}({cols}) VALUES ({cols_val}"""
            + """) RETURNING """
            + return_col
        )

    else:
        sql = f"""INSERT INTO {table}({cols}) VALUES ({cols_val})"""
    cur.executemany(sql,[data_dict])
    cur.execute('SELECT LASTVAL()')
    db_run_id = cur.fetchall()[0][0] # fetching the value returned by ".....RETURNING ___"
    conn.commit()
    if db_run_id:
        return db_run_id