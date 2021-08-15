import shutil
from tempfile import mkdtemp

import pytest
import pandas as pd


@pytest.fixture(scope="function")
def tmp_dir():
    output_dir = mkdtemp()
    yield output_dir
    shutil.rmtree(output_dir)


@pytest.fixture(scope="function")
def df_with_dates():
    df = pd.DataFrame(
        {
            "datetime_col": [
                "2021-06-02T21:09:52Z",
                "2021-06-02T21:10:06Z",
                "2021-06-03T21:12:52Z",
                "2021-06-03T21:16:12Z",
                "2021-06-02T21:19:21Z",
                "2021-06-02T21:34:02Z",
                "2021-06-04T21:36:51Z",
                "2021-06-03T21:39:12Z",
                "2021-06-04T21:46:51Z",
                "2021-06-02T21:50:10Z",
                "2021-06-04T21:51:50Z",
                "2021-06-04T21:53:51Z",
            ]
        }
    )
    df["datetime_col"] = pd.to_datetime(df["datetime_col"])
    return df
