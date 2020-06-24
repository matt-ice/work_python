import pandas as pd
import re
import os
import datetime


def pandas_processing(source_directory, file_name, output_directory):
    df = pd.concat(pd.read_excel(os.path.join(source_directory, file_name), sheet_name=None, skiprows=5),
                   ignore_index=True)
    # drop first column as it's empty
    df.drop(df.columns[0], axis=1, inplace=True)
    # drop all rows that contain Totals and are empty
    total_indexes = df[df["Site Name"] == "Total"].index
    empty_indexes = df[df["Site Name"].isnull()].index
    df.drop(total_indexes, inplace=True)
    df.drop(empty_indexes, inplace=True)
    df.columns = ['site_name', 'location_description', 'careteam', 'contract_ref', 'service_code', 'visit_id',
                  'careplan_id', 'client_id', 'client_ss_id', 'client_forename', 'client_surname', 'visit_start_date',
                  'visit_end_date', 'template_start_time', 'template_duration', 'planned_start_time',
                  'planned_duration', 'actual_start_time', 'actual_duration', 'actual_end_time', 'invoice_status',
                  'time_ciritcal_flag', 'variation_datetime', 'variation_reason', 'variation_user',
                  'multilink_reference', 'time_ciritcal_flag_1', 'week_start_date', 'billable_duration_calculated',
                  'billable_value_calculated', 'calculated_available', 'last_calculation', 'bill_status', 'bill_rule',
                  'billable_start', 'billable_end', 'calculated_payable_duration', 'calculated_payable_value',
                  'pay_status', 'payroll_status', 'pay_rule', 'payable_start', 'payable_end', 'payroll_run_date']
    # getting rid of empty columns
    empty_cols = [col for col in df.columns if df[col].isnull().all()]
    # Drop these columns from the dataframe
    df.drop(empty_cols,
            axis=1,
            inplace=True)
    df.to_csv(os.path.join(output_directory, file_name[:-5] + '.csv'), index=False)


def get_date_string(filename):
    # getting date string out of file - eg abcd30062020.xslx becomes 30062020 or None if there is no such string
    try:
        matched = re.search('([0-9]{8})', filename)  # search for 8 digit date code
        return matched.group(1)
    except:
        return None


def convert_string_to_date(date_string):
    # convert date string to date so 30062020 becomes 30/06/2020
    return datetime.date(int(date_string[4:]), int(date_string[2:4]), int(date_string[:2]))


def find_last_file(directory, date_compare, go_to_end):
    '''
    loop through all files in the folder and find the one with the latest date

    go_to_end is used so that files get processed in order, so if 3 new files get uploaded, it takes the file that has
    the first later date (go_to_end == False) than the file in sync with the latest date (go_to_end == True)
    '''
    directory = os.fsencode(directory)
    last_date = date_compare
    last_file = None
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        date_string = get_date_string(filename)
        if date_string is not None:
            file_date = convert_string_to_date(date_string)
            if file_date > last_date and go_to_end == False:
                return filename
            elif file_date > last_date and go_to_end:
                last_date = file_date
                last_file = filename
    if last_file is None:
        return '01012000.csv'  # random output to have the main loop run if there are no files in sync folder
    else:
        return last_file


def get_number_of_files(directory):
    # does what it says on the tin
    return len(next(os.walk(directory))[2])


def main_loop(upload_dir, sync_dir):
    upload_folder = upload_dir
    sync_folder = sync_dir

    # getting the last file synced
    last_sync = find_last_file(sync_folder, datetime.date(2000, 1, 1), True)
    last_upload = find_last_file(upload_folder, convert_string_to_date(get_date_string(last_sync)), False)
    print("processing {}".format(last_upload))
    if last_upload[:-5] != last_sync[:-4]:
        pandas_processing(upload_folder, last_upload, sync_folder)
        return True  # return True if the loop ran
    else:
        return False  # return False if loop didn't run


upload = # source folder
sync =   # output folder
upload_files = get_number_of_files(upload)
sync_files = get_number_of_files(sync)
iterations = upload_files - sync_files
for i in range(iterations):
    result = main_loop(upload, sync)
    if result == False:
        exit(0)
