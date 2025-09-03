# define "db_data_insert" function
def db_data_insert(db_name: str, username: str, password: str, db_host: str, db_port: str, batch_ticket_data: list):
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        import psycopg2
        from psycopg2.extras import execute_values
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S01] - {str(error)}', 'row_count' : 0}

    # importing "log_writer" function:S02
    try:
        sys.path.append(str(Path.cwd()))
        from support.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S02] - {str(error)}', 'row_count' : 0}

    # define db connection parameter:S03
    try:
        db_connection_parameter = {
            "dbname" : str(db_name),
            "user" : str(username),
            "password" : str(password),
            "host" : str(db_host),
            "port" : str(db_port)
        }
        log_writer(file_name = 'DB-Data-Insert', steps = '03', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(file_name = 'DB-Data-Insert', steps = '03', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S03] - {str(error)}', 'row_count' : 0}

    # check if "incident_data" table present:S04
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
                if (not table_exists):
                    log_writer(file_name = 'DB-Data-Insert', steps = '04', status = 'ERROR', message = 'Table "incident_data" Not Present')
                    return {'status' : 'ERROR', 'message' : '"incident_data" Table Not Present', 'row_count' : 0}
    except Exception as error:
        log_writer(file_name = 'DB-Data-Insert', steps = '04', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S04] - {str(error)}', 'row_count' : 0}

    # define data upsert SQL query:S05
    try:
        ticket_data_upsert_sql = '''
        WITH v (
            ticket_type, company, sys_id, number, created_by, created_on, opened_by, opened_at,
            configuration_item, category, subcategory, priority, impact, urgency, severity, state,
            incident_state, assignment_group, assigned_to, parent_incident, business_process, vendor,
            environment, availability_group, short_description, description, resolved_by, resolved_at,
            close_code, close_notes, work_notes
        ) AS (
            VALUES %s
        )
        INSERT INTO incident_data (
            ticket_type, company, sys_id, number, created_by, created_on, opened_by, opened_at,
            configuration_item, category, subcategory, priority, impact, urgency, severity, state,
            incident_state, assignment_group, assigned_to, parent_incident, business_process, vendor,
            environment, availability_group, short_description, description, resolved_by, resolved_at,
            close_code, close_notes, work_notes
        )
        SELECT
            ticket_type, company, sys_id, number, created_by, created_on, opened_by, opened_at,
            configuration_item, category, subcategory, priority, impact, urgency, severity, state,
            incident_state, assignment_group, assigned_to, parent_incident, business_process, vendor,
            environment, availability_group, short_description, description, resolved_by, resolved_at,
            close_code, close_notes, work_notes
        FROM v
        WHERE sys_id IS NOT NULL AND btrim(sys_id) <> ''
        ON CONFLICT (sys_id) DO UPDATE SET
            ticket_type = EXCLUDED.ticket_type,
            company = EXCLUDED.company,
            number = EXCLUDED.number,
            created_by = EXCLUDED.created_by,
            created_on = EXCLUDED.created_on,
            opened_by = EXCLUDED.opened_by,
            opened_at = EXCLUDED.opened_at,
            configuration_item = EXCLUDED.configuration_item,
            category = EXCLUDED.category,
            subcategory = EXCLUDED.subcategory,
            priority = EXCLUDED.priority,
            impact = EXCLUDED.impact,
            urgency = EXCLUDED.urgency,
            severity = EXCLUDED.severity,
            state = EXCLUDED.state,
            incident_state = EXCLUDED.incident_state,
            assignment_group = EXCLUDED.assignment_group,
            assigned_to = EXCLUDED.assigned_to,
            parent_incident = EXCLUDED.parent_incident,
            business_process = EXCLUDED.business_process,
            vendor = EXCLUDED.vendor,
            environment = EXCLUDED.environment,
            availability_group = EXCLUDED.availability_group,
            short_description = EXCLUDED.short_description,
            description = EXCLUDED.description,
            resolved_by = EXCLUDED.resolved_by,
            resolved_at = EXCLUDED.resolved_at,
            close_code = EXCLUDED.close_code,
            close_notes = EXCLUDED.close_notes,
            work_notes = EXCLUDED.work_notes;'''
        log_writer(file_name = 'DB-Data-Insert', steps = '05', status = 'SUCCESS', message = 'Data Upsert SQL Query Defined')
    except Exception as error:
        log_writer(file_name = 'DB-Data-Insert', steps = '05', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S05] - {str(error)}', 'row_count' : 0}

    # insert batch ticket data into table:S06
    try:
        with psycopg2.connect(**db_connection_parameter) as database_connection:  # type: ignore
            with database_connection.cursor() as database_cursor:
                execute_values(database_cursor, ticket_data_upsert_sql, batch_ticket_data)
    except psycopg2.Error as db_error:
        log_writer(file_name = 'DB-Data-Insert', steps = '06', status = 'ERROR', message = str(db_error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S06] - {str(db_error)}', 'row_count' : 0}
    except Exception as error:
        log_writer(file_name = 'DB-Data-Insert', steps = '06', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S06] - {str(error)}', 'row_count' : 0}

    # fetch inserted row count:S07
    try:
        with psycopg2.connect(**db_connection_parameter) as database_connection:  # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute('SELECT COUNT(*) FROM incident_data;')
                inserted_ticket_count = int(database_cursor.fetchone()[0])
                log_writer(file_name = 'DB-Data-Insert', steps = '07', status = 'SUCCESS', message = f'Total {int(inserted_ticket_count)} Incident Ticket Details Upserted')
                return {'status' : 'SUCCESS', 'message' : 'Ticket Data Upserted', 'row_count' : int(inserted_ticket_count)}
    except Exception as error:
        log_writer(file_name = 'DB-Data-Insert', steps = '07', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S07] - {str(error)}', 'row_count' : 0}