import pandas as pd
from pandas import json_normalize
import argparse


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


def run_pipeline(
    components_location: str,
    orders_location: str,
    output_location: str,
):
    print(components_location, orders_location, output_location)

    # pd.read_json(orders_location).show()

    df_components = load_file_from_dataframe(components_location, file_format="csv")
    print(df_components)
    df_components = df_components[["componentId", "colour"]]

    df_orders = load_file_from_dataframe(orders_location, "json")
    print(df_orders)
    df_orders = df_orders[["timestamp", "units"]]

    df_orders_single_day = extract_day_from_dataframe(df_orders, "2021-06-03", "timestamp")[["units"]]
    print(df_orders_single_day)

    # df_orders_single_day.drop("timestamp", axis=1, inplace=True)
    # print(df_orders_single_day)

    df_orders_normalised = pd.json_normalize(df_orders_single_day["units"])
    print(df_orders_normalised)

    component_id_list = df_components["componentId"].tolist()
    print(component_id_list)

    df_orders_counted = df_orders_normalised.count(axis=0).to_frame()
    print(df_orders_counted)

    df_joined = df_orders_counted.join(df_components.set_index("componentId"))[["colour", 0]]
    print(df_joined)

    write_dataframe_to_file(
        df_joined, file_location=output_location, file_format="csv", header=False, mode="w", sep=":"
    )


def main():

    parser = argparse.ArgumentParser(description="DataJob")

    parser.add_argument(
        "--components_location",
        action="store",
        required=False,
        type=str,
        default="./data/input/components.csv",
    )

    parser.add_argument(
        "--orders_location",
        action="store",
        required=False,
        type=str,
        default="./data/input/orders.json.txt",
    )

    parser.add_argument(
        "--output_location",
        action="store",
        required=False,
        type=str,
        default="./data/output/order_volume.txt",
    )

    args = vars(parser.parse_args())

    run_pipeline(
        components_location=args["components_location"],
        orders_location=args["orders_location"],
        output_location=args["output_location"],
    )


if __name__ == "__main__":
    main()
