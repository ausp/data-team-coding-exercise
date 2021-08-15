import pandas as pd
from pandas import json_normalize
import argparse

from . import helper_functions as hf


def run_pipeline(
    components_location: str,
    orders_location: str,
    output_location: str,
):

    df_components = hf.load_file_from_dataframe(components_location, file_format="csv")
    df_components = df_components[["componentId", "colour"]]  # Discard non-required columns to speed solution

    df_orders = hf.load_file_from_dataframe(orders_location, "json")
    df_orders = df_orders[["timestamp", "units"]]  # Discard non-required columns to speed solution

    # Filter required data and drop timestamp column, which is no longer required
    df_orders_single_day = hf.extract_day_from_dataframe(df_orders, "2021-06-03", "timestamp")[["units"]]

    # Normalise the 'units' column to split apart the kv pairs
    df_orders_normalised = pd.json_normalize(df_orders_single_day["units"])

    # Sum the parts ordered and convert output to ints
    df_orders_counted = df_orders_normalised.sum(axis=0).to_frame()
    df_orders_counted[0] = df_orders_counted[0].astype("int")

    # Join dataframes to obtain the colours of each componentId
    df_joined = df_orders_counted.join(df_components.set_index("componentId"))[["colour", 0]]

    # Write output to file at provided location.
    hf.write_dataframe_to_file(
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
