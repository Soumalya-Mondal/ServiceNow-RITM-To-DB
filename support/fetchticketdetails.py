# define "fetch_ticket_details" function
def fetch_ticket_details(snow_url: str, username: str, password: str, fetch_offset: int):
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        import urllib3
        import requests
        from datetime import datetime, timezone
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S01] - {str(error)}', 'ticket_details' : []}

    # importing "log_writer" function:S02
    try:
        sys.path.append(str(Path.cwd()))
        from support.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S02] - {str(error)}', 'ticket_details' : []}

    # define ServiceNow parameter:S03
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # define empty "batch_ticket_records" list
        batch_ticket_records = []
        snow_credential = (username, password)
        snow_headers = {
            'Accept': 'Application/json',
            'Content-Type': 'Application/json'
        }
        snow_params = {
            'sysparm_display_value': 'all',
            'sysparm_query': 'ORDERBYsys_created_on',
            'sysparm_exclude_reference_link' : 'true',
            'sysparm_fields': 'assigned_to,assignment_group,close_code,close_notes,requested_for,company,description,impact,price,recurring_price,number,opened_at,opened_by,made_sla,priority,closed_at,closed_by,quantity,short_description,state,sys_class_name,sys_created_by,sys_created_on,sys_id,escalation,approval,cat_item,u_tenant_category,u_tenant_subcategory,billable,urgency,work_notes',
            'sysparm_limit' : '10000',
            'sysparm_offset' : str(fetch_offset)
        }
        snow_api_url = f'{snow_url}/api/now/table/sc_req_item'
        log_writer(file_name = 'Fetch-Ticket-Details', steps = '03', status = 'SUCCESS', message = 'ServiceNow Parameter Defined')
    except Exception as error:
        log_writer(file_name = 'Fetch-Ticket-Details', steps = '03', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S03] - {str(error)}', 'ticket_details' : []}

    # define "parse_snow_datetime" function:S04
    def parse_snow_datetime(value):
        EPOCH_UTC = datetime(1970, 1, 1, tzinfo = timezone.utc)
        s = (value or '').strip()
        if (not s):
            return EPOCH_UTC
        # try common ServiceNow Date-Time formats
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
            try:
                return datetime.strptime(s, fmt).replace(tzinfo = timezone.utc)
            except ValueError:
                pass
        # try ISO-8601
        try:
            return datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(timezone.utc)
        except ValueError:
            return EPOCH_UTC

    # define "get_display_value" function
    def get_display_value(item, field):
        return item.get(field, {}).get("display_value") or "N/A"

    # define "sanitize_value" function
    def sanitize_value(value):
        if isinstance(value, str):
            return value.replace('\x00', '')  # remove NUL characters
        return value

    # calling ServiceNow API:S05
    try:
        ritm_ticket_data_response = requests.get(snow_api_url, auth = snow_credential, headers = snow_headers, params = snow_params, verify = False)
        # check the response status code
        if (int(ritm_ticket_data_response.status_code) == 200):
            ritm_ticket_result = ritm_ticket_data_response.json().get('result', [])
            # if there is no result
            if (ritm_ticket_result):
                # loop through all the ticket details
                for ticket_item in ritm_ticket_result:
                    ticket_record = (
                        sanitize_value(get_display_value(ticket_item, 'sys_class_name')), # ticket_type
                        sanitize_value(get_display_value(ticket_item, 'company')), # company
                        sanitize_value(get_display_value(ticket_item, 'sys_id')), # sys_id
                        sanitize_value(get_display_value(ticket_item, 'number')), # number
                        sanitize_value(get_display_value(ticket_item, 'sys_created_by')), # created_by
                        parse_snow_datetime(ticket_item.get('sys_created_on', {}).get('value')), #created_on
                        sanitize_value(get_display_value(ticket_item, 'opened_by')), # opened_by
                        parse_snow_datetime(ticket_item.get('opened_at', {}).get('value')), #opened_at
                        sanitize_value(get_display_value(ticket_item, 'requested_for')), # requested_for
                        sanitize_value(get_display_value(ticket_item, 'u_tenant_category')), # category
                        sanitize_value(get_display_value(ticket_item, 'u_tenant_subcategory')), # subcategory
                        sanitize_value(get_display_value(ticket_item, 'priority')), # priority
                        sanitize_value(get_display_value(ticket_item, 'impact')), # impact
                        sanitize_value(get_display_value(ticket_item, 'urgency')), # urgency
                        sanitize_value(get_display_value(ticket_item, 'quantity')), # quatity
                        sanitize_value(get_display_value(ticket_item, 'state')), # state
                        sanitize_value(get_display_value(ticket_item, 'price')), # price
                        sanitize_value(get_display_value(ticket_item, 'recurring_price')), # recurring_price
                        sanitize_value(get_display_value(ticket_item, 'assignment_group')), # assignment_group
                        sanitize_value(get_display_value(ticket_item, 'assigned_to')), # assigned_to
                        sanitize_value(get_display_value(ticket_item, 'made_sla')), # made_sla
                        sanitize_value(get_display_value(ticket_item, 'approval')), # approval
                        sanitize_value(get_display_value(ticket_item, 'billable')), # billable
                        sanitize_value(get_display_value(ticket_item, 'cat_item')), # catalog_item
                        sanitize_value(get_display_value(ticket_item, 'escalation')), # escalation
                        sanitize_value(get_display_value(ticket_item, 'short_description')), # short_description
                        sanitize_value(get_display_value(ticket_item, 'description')), # description
                        sanitize_value(get_display_value(ticket_item, 'closed_by')), # closed_by
                        parse_snow_datetime(ticket_item.get('closed_at', {}).get('value')), # closed_at
                        sanitize_value(get_display_value(ticket_item, 'close_notes')), # close_notes
                        sanitize_value(get_display_value(ticket_item, 'work_notes')) # work_notes
                    )
                    # check if "sys_id" and "number" are non-empty
                    if all([ticket_record[2] and ticket_record[2].strip(), ticket_record[3] and ticket_record[3].strip()]):
                        batch_ticket_records.append(ticket_record)
                log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'SUCCESS', message = f'Total: {len(batch_ticket_records)} RITM Ticket Details Fetched')
                return {'status' : 'SUCCESS', 'message' : 'Ticket Details Fetched', 'ticket_details' : batch_ticket_records}
            else:
                log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'INFO', message = 'No New RITM Ticket Found In ServiceNow')
                return {'status' : 'INFO', 'message' : 'No More Ticket Details Found In ServiceNow', 'ticket_details' : []}
        else:
            log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'ERROR', message = str(ritm_ticket_data_response.text))
            return {'status' : 'ERROR', 'message' : str(ritm_ticket_data_response.text), 'ticket_details' : []}
    except Exception as error:
        log_writer(file_name = 'Fetch-Ticket-Details', steps = '05', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'message' : f'[Fetch-Ticket-Details:S05] - {str(error)}', 'ticket_details' : []}