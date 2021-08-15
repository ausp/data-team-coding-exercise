from datetime import datetime

import pytest
import pandas as pd

from src.helper_functions import load_file_from_dataframe, write_dataframe_to_file, extract_day_from_dataframe


@pytest.mark.usefixtures("df_with_dates")
def test_extract_day_from_dataframe(df_with_dates):

    expected = pd.DataFrame(
        {
            "datetime_col": [
                "2021-06-03T21:12:52Z",
                "2021-06-03T21:16:12Z",
                "2021-06-03T21:39:12Z",
            ]
        }
    ).sort_values("datetime_col")
    print(expected.dtypes)
    expected["datetime_col"] = pd.to_datetime(expected["datetime_col"])
    print(expected.dtypes)
    actual = extract_day_from_dataframe(df_with_dates, "2021-06-03", "datetime_col").sort_values("datetime_col")
    print(actual.dtypes)

    pd.testing.assert_frame_equal(actual.reset_index(drop=True), expected.reset_index(drop=True))
