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

    # check if "ritm_data" table present:S04
    try:
        with psycopg2.connect(**db_connection_parameter) as database_connection:  # type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute('''
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'ritm_data'
                );''')
                table_exists = database_cursor.fetchone()[0]
                # check if "ritm_data" table present
                if (not table_exists):
                    log_writer(file_name = 'DB-Data-Insert', steps = '04', status = 'ERROR', message = 'Table "ritm_data" Not Present')
                    return {'status' : 'ERROR', 'message' : '"ritm_data" Table Not Present', 'row_count' : 0}
    except Exception as error:
        log_writer(file_name = 'DB-Data-Insert', steps = '04', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S04] - {str(error)}', 'row_count' : 0}

    # define data upsert SQL query:S05
    try:
        ticket_data_upsert_sql = '''
        WITH v (
            ticket_type, company, sys_id, number, created_by, created_on, opened_by, opened_at,
            requested_for, category, subcategory, priority, impact, urgency, quantity, state,
            price, recurring_price, assignment_group, assigned_to, made_sla, approval, billable,
            catalog_item, escalation, short_description, description, closed_by, closed_at,
            close_notes, work_notes
        ) AS (
            VALUES %s
        )
        INSERT INTO ritm_data (
            ticket_type, company, sys_id, number, created_by, created_on, opened_by, opened_at,
            requested_for, category, subcategory, priority, impact, urgency, quantity, state,
            price, recurring_price, assignment_group, assigned_to, made_sla, approval, billable,
            catalog_item, escalation, short_description, description, closed_by, closed_at,
            close_notes, work_notes
        )
        SELECT
            ticket_type, company, sys_id, number, created_by, created_on, opened_by, opened_at,
            requested_for, category, subcategory, priority, impact, urgency, quantity, state,
            price, recurring_price, assignment_group, assigned_to, made_sla, approval, billable,
            catalog_item, escalation, short_description, description, closed_by, closed_at,
            close_notes, work_notes
        FROM v
        WHERE sys_id IS NOT NULL AND btrim(sys_id) <> ''
        ON CONFLICT (sys_id) DO UPDATE SET
            ticket_type       = EXCLUDED.ticket_type,
            company           = EXCLUDED.company,
            number            = EXCLUDED.number,
            created_by        = EXCLUDED.created_by,
            created_on        = EXCLUDED.created_on,
            opened_by         = EXCLUDED.opened_by,
            opened_at         = EXCLUDED.opened_at,
            requested_for     = EXCLUDED.requested_for,
            category          = EXCLUDED.category,
            subcategory       = EXCLUDED.subcategory,
            priority          = EXCLUDED.priority,
            impact            = EXCLUDED.impact,
            urgency           = EXCLUDED.urgency,
            quantity          = EXCLUDED.quantity,
            state             = EXCLUDED.state,
            price             = EXCLUDED.price,
            recurring_price   = EXCLUDED.recurring_price,
            assignment_group  = EXCLUDED.assignment_group,
            assigned_to       = EXCLUDED.assigned_to,
            made_sla          = EXCLUDED.made_sla,
            approval          = EXCLUDED.approval,
            billable          = EXCLUDED.billable,
            catalog_item      = EXCLUDED.catalog_item,
            escalation        = EXCLUDED.escalation,
            short_description = EXCLUDED.short_description,
            description       = EXCLUDED.description,
            closed_by         = EXCLUDED.closed_by,
            closed_at         = EXCLUDED.closed_at,
            close_notes       = EXCLUDED.close_notes,
            work_notes        = EXCLUDED.work_notes;'''
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
                database_cursor.execute('SELECT COUNT(*) FROM ritm_data;')
                inserted_ticket_count = int(database_cursor.fetchone()[0])
                log_writer(file_name = 'DB-Data-Insert', steps = '07', status = 'SUCCESS', message = f'Total {int(inserted_ticket_count)} RITM Ticket Details Upserted')
                return {'status' : 'SUCCESS', 'message' : 'Ticket Data Upserted', 'row_count' : int(inserted_ticket_count)}
    except Exception as error:
        log_writer(file_name = 'DB-Data-Insert', steps = '07', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[DB-Data-Insert:S07] - {str(error)}', 'row_count' : 0}