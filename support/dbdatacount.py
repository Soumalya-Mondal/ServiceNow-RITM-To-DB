# define "db_data_count" function
def db_data_count(db_name: str, username: str, password: str, db_host: str, db_port: str):
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        import psycopg2
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Count:S01] - {str(error)}', 'row_count' : 0}

    # importing "log_writer" function:S02
    try:
        sys.path.append(str(Path.cwd()))
        from support.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Total-Ticket-Count:S02] - {str(error)}', 'row_count' : 0}

    # define db connection parameter:S03
    try:
        db_connection_parameter = {
            "dbname" : str(db_name),
            "user" : str(username),
            "password" : str(password),
            "host" : str(db_host),
            "port" : str(db_port)
        }
        log_writer(file_name = 'DB-Data-Count', steps = '03', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(file_name = 'DB-Data-Count', steps = '03', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Count:S03] - {str(error)}', 'row_count' : 0}

    # check if "incident_data" table present and fetch row count:S04
    try:
        with psycopg2.connect(**db_connection_parameter) as database_connection:  # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute('''
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'incident_data'
                );''')
                table_exists = database_cursor.fetchone()[0]
                # check if "incident_data" table present
                if table_exists:
                    # fetch row count from "incident_data" table
                    database_cursor.execute('SELECT COUNT(*) FROM incident_data;')
                    records_count = database_cursor.fetchone()[0]
                    log_writer(file_name = 'DB-Data-Count', steps = '04', status = 'SUCCESS', message = f'Total {int(records_count)} Rows Count Fetched From "incident_data" Table')
                    return {'status' : 'SUCCESS', 'message' : 'Total Rows Count Fetched From "incident_data" Table', 'row_count' : int(records_count)}
                else:
                    log_writer(file_name = 'DB-Data-Count', steps = '04', status = 'ERROR', message = 'Table "incident_data" Not Present Inside Database')
                    return {'status' : 'ERROR', 'message' : '"incident_data" Table Not Present Inside Database', 'row_count' : 0}
    except Exception as error:
        log_writer(file_name = 'DB-Data-Count', steps = '04', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Count:S04] - {str(error)}', 'row_count' : 0}