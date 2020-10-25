import pandas as pd
import datetime as dt
import time
import os

def display_settings(max_rows=500, max_columns=20, display_width=1000):
    """
    :param max_rows: row option
    :param max_columns: column option
    :param display_width: display width option
    :return: adjusted display options
    """
    pd.set_option('display.max_rows', max_rows)
    pd.set_option('display.max_columns', max_columns)
    pd.set_option('display.width', display_width)


def time_checkpoint(checkpoint_message, start_time):
    """
    :param checkpoint_message: check point message to be printed
    :param start_time: start time in float. this should be at the start of the portion you are testing
    :return: message with current time minus start time
    """
    seconds = int(round(time.time() - start_time))
    stopwatch = dt.timedelta(seconds=seconds)
    print(checkpoint_message, " ", stopwatch)


def custom_round(series, round_list):
    """
    :param series: int series to be rounded
    :param round_list: list of numbers you want to round to. ex [15, 30, 60, 120]
    :return: series with argument series rounded to given int list
    """
    boundaries = pd.Series(round_list)
    rounded_series = series.map(lambda pt: boundaries[(boundaries - pt).abs().argmin()])
    return rounded_series


def combine_workbooks_to_df(folder_location, skip_rows=0):
    """
    :param skip_rows: how many rows to skip
    :param folder_location: location of .CSV or .XLSX file to be combined
    :return: df with merged files
    """
    file_list = os.listdir(folder_location)
    save_loc_list = []

    for File in file_list:
        save_loc = folder_location + r'/' + File
        save_loc_list.append(save_loc)

    main_df = pd.DataFrame()

    for file in save_loc_list:
        file_ext = os.path.splitext(file)[-1]
        if file_ext == '.xlsx':
            temp_df = pd.read_excel(io=file, header=0, skiprows=skip_rows)
        elif file_ext == '.csv':
            temp_df = pd.read_csv(filepath_or_buffer=file, header=0, skiprows=skip_rows)
        else:
            print(file + ' is not a .CSV or .XLSX file type')

        temp_df.dropna(how='all', inplace=True)
        main_df = pd.concat(objs=[main_df, temp_df], ignore_index=True)

    return main_df


def save_df_to_excel(df, save_path, df_date_header=None, overwrite=False):
    """
    :param df: df to save
    :param save_path: location to save df
    :param df_date_header:
    :param overwrite: option to overwrite existing file or name as next version number
    :return: .XSLX file saved to given location
    """
    if df_date_header is not None:
        df[df_date_header] = pd.to_datetime(df[df_date_header])
        min_date = df[df_date_header].min().strftime('%m.%d.%Y')
        max_date = df[df_date_header].max().strftime('%m.%d.%Y')
        save_path = save_path + '_' + min_date + '-' + max_date

    if overwrite:
        df.to_excel(excel_writer=save_path + '.xlsx', index=False)
    else:
        i, save_path_alt = 0, save_path
        while os.path.isfile(save_path_alt + '.xlsx'):
            version_num = 'V' + str(i + 2)
            save_path_alt = save_path + '_' + version_num
            i += 1
        df.to_excel(excel_writer=save_path_alt + '.xlsx', index=False)


def uid_creator(df, list_of_id, insert_loc_index=0):
    """
    :param df:
    :param list_of_id: headers to combine into UID
    :return: df with UID column
    """
    uid_df = df[list_of_id]
    uid_series = uid_df[uid_df.columns].apply(
        lambda x: ','.join(x.dropna().astype(str)), axis=1)
    df.insert(loc=insert_loc_index, column="UID", value=uid_series)

    return df


def clean_header(df):
    df.columns = df.columns.str.replace(' ', '_').str.lower()
