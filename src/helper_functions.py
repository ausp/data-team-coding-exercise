import pandas as pd


def load_file_from_dataframe(file_location: str, file_format: str):
    if file_format == "json":
        return pd.read_json(file_location, lines=True)
    elif file_format == "csv":
        return pd.read_csv(file_location, delimiter=",", header=0)
    else:
        raise Exception(f"File format {file_format} is not recognised")


def write_dataframe_to_file(
    df: pd.DataFrame, file_location: str, file_format: str = "csv", header=True, mode: str = "x", sep=","
):
    if file_format == "json":
        df.to_json(file_location, mode=mode)
    elif file_format == "csv":
        df.to_csv(file_location, mode=mode, header=header, index=False, sep=sep)
    else:
        raise Exception(f"File format {file_format} is not recognised")


def extract_day_from_dataframe(df: pd.DataFrame, day: str, col: str) -> pd.DataFrame:
    return df[df[col].dt.date == pd.to_datetime(day).date()]
