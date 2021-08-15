import pandas as pd


def load_file_from_dataframe(file_location: str, file_format: str, fail_on_error=True):
    try:
        if file_format == "json":
            return pd.read_json(file_location, lines=True)
        elif file_format == "csv":
            return pd.read_csv(file_location, delimiter=",", header=0)
        else:
            raise Exception(f"File format {file_format} is not recognised")
    except Exception as e:
        print(e)
        if fail_on_error is True:
            raise e


def write_dataframe_to_file(
    df: pd.DataFrame,
    file_location: str,
    file_format: str = "csv",
    header=True,
    mode: str = "x",
    sep=",",
    fail_on_error=True,
):
    try:
        if file_format == "json":
            df.to_json(file_location, mode=mode)
        elif file_format == "csv":
            df.to_csv(file_location, mode=mode, header=header, index=False, sep=sep)
        else:
            raise Exception(f"File format {file_format} is not recognised")
    except Exception as e:
        print(e)
        if fail_on_error is True:
            raise e


def extract_day_from_dataframe(df: pd.DataFrame, day: str, col: str) -> pd.DataFrame:
    return df[df[col].dt.date == pd.to_datetime(day).date()]


def process_orders(df, col_name):
    # Normalise the 'units' column to split apart the kv pairs
    df_orders_normalised = pd.json_normalize(df[col_name])

    # Sum the parts ordered and convert output to ints
    df_orders_counted = df_orders_normalised.sum(axis=0).to_frame()
    df_orders_counted[0] = df_orders_counted[0].astype("int")
    return df_orders_counted
