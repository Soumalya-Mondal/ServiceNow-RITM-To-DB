# define "log_writer" function
def log_writer(file_name: str, steps: str, status: str, message: str):
    # importing python module:S01
    try:
        from pathlib import Path
        from datetime import datetime
    except Exception as error:
        print(f'ERROR - [Log-Writer:S01] - {str(error)}')

    # define file path:S02
    try:
        parent_folder_path = Path.cwd()
        activity_log_file_path = Path(parent_folder_path) / 'activity.log'
    except Exception as error:
        print(f'ERROR - [Log-Writer:S02] - {str(error)}')

    # define log time:S03
    try:
        log_date_time = datetime.now().strftime('%d-%b-%Y - %I:%M:%S %p')
    except Exception as error:
        print(f'ERROR - [Log-Writer:S03] - {str(error)}')

    # write message to log file:S04
    try:
        with open(activity_log_file_path, 'a') as log_file:
            log_file.write(f'{str(log_date_time)} - {str(file_name).ljust(20)} - {str(steps)} - {str(status).ljust(7)} - {str(message)}\n')
    except Exception as error:
        print(f'ERROR - [Log-Writer:S04] - {str(error)}')