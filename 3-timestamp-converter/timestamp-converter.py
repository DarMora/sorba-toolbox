import pandas as pd


def main():
    # Read csv
    pdf = pd.read_csv("C:\\Users\\cmolina.ITG.000\\Downloads\\ITG\\REF.csv", delimiter=',')

    # Transform timestamp to datetime64[ns] data type
    pdf['time'] = pd.to_datetime(pdf['time'], infer_datetime_format=True)

    # Convert timestamp column (datatype: datetime64[ns]) to format: 2017-08-22 13:25:28.875 (datatype: str object)
    pdf['time'] = pdf['time'].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    # truncate number of microseconds (6 digits) to milliseconds (3 digits)
    pdf['time'] = pdf['time'].str[:-3]

    # Check printed timestamp and write to csv to check as well, in both cases it should follow the stand format: 2017-08-22 13:25:28.875
    pdf.to_csv("C:\\Users\\cmolina.ITG.000\\Downloads\\ITG\\REF-formatted.csv", sep=',', encoding='utf-8', index=False)

# jajjaja modifique la cosaaaa
if __name__ == '__main__':
    with open("C:\\Users\\cmolina.ITG.000\\Downloads\\ITG\\REF-formatted.csv") as f:
        print(f.readline())
        print(f.readline())

    main()
