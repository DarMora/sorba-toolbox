import pandas as pd
import re


def check_dt_consistency(date_time: str):
    # search for a pattern match
    _match = re.search("(\d+.\d+.\d+)( \d+)?(:\d+)?(:\d+)?", date_time)
    #             GROUP:      1         2      3      4
    if _match.group(2) and _match.group(3) and _match.group(4):
        return date_time
    elif _match.group(2) and _match.group(3):
        return _match.group(1)+_match.group(2)+_match.group(3) + ":00"
    elif _match.group(2):
        return _match.group(1)+_match.group(2)+":00:00"
    else:
        return _match.group(1) + " 00:00:00"


def check_data_consistency(file_name: str):
    # print file name being processed
    print(file_name)

    # read csv into a dataframe
    file_name = pd.read_csv(file_name)

    # fill empty values forward and backward
    file_name.fillna(method='ffill', inplace=True)
    file_name.fillna(method='bfill', inplace=True)

    # write dataframe to csv
    file_name.to_csv(file_name)


def fmt_narrow_to_wide_s7_hmi_to_sdc(file_name: str, dst_dir_name: str):
    """
    this function reformats narrow-formatted data that come from Siemens HMI logs
    into wide-formatted data compatible with SDE Simulation channel

    implemented by using pandas dataframe pivot function (very efficient)

    :param file_name:
    :param dst_dir_name:
    :return:
    """

    # read csv into a dataframe
    df_src = pd.read_csv(file_name, delimiter=';', skipfooter=1, engine='python')

    # check consistency
    df_src.dropna(axis=0, inplace=True)
    df_src = df_src[df_src['Validity'] > 0]
    df_src['TimeString'] = df_src['TimeString'].map(lambda x: check_dt_consistency(x))

    # convert source time format to desired time format
    # source: 07.11.2019 19:23:35
    # destination: 11/07/2019 19:23:35
    df_src['TimeString'] = pd.to_datetime(df_src['TimeString'],
                                          format='%d.%m.%Y %H:%M:%S')  # infer_datetime_format=True
    df_src['TimeString'] = df_src['TimeString'].dt.strftime('%m/%d/%Y %H:%M:%S')

    # rename time column name
    df_src.rename({'TimeString': 'Time'}, axis='columns', inplace=True)

    # cast value column to float
    df_src['VarValue'] = df_src['VarValue'].map(lambda x: float(x.replace(',', '.')))

    # create the result empty dataframe
    df_dst = df_src.pivot_table(index='Time', columns='VarName', values='VarValue')

    # remove $RT_OFF$ column if exists
    if '$RT_OFF$' in df_dst.columns:
        df_dst.drop(columns=['$RT_OFF$'], inplace=True)

    # check dataframe consistency
    df_dst.fillna(method='ffill', inplace=True)
    df_dst.fillna(method='bfill', inplace=True)

    # write dataframe into csv file
    df_dst.to_csv(dst_dir_name)
