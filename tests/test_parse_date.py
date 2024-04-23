import pandas as pd
import pytest
from data_cleaner import parse_date

def test_parse_date_when_proper_format_should_return_datetime():
    # Arrange
    df = pd.DataFrame({'Date': ['May 21, 2021', 'May 22, 2021', 'May 23, 2021']})
    # Act
    result_df = parse_date(df, 'Date')
    # Assert
    assert result_df['Date'].dtype == 'datetime64[ns]'
    assert not result_df['Date'].isnull().any()

def test_parse_date_when_column_already_datetime_should_return_same_column():
    # Arrange
    df = pd.DataFrame({'Date': pd.to_datetime(['2021-05-21', '2021-05-22', '2021-05-23'])})
    # Act
    result_df = parse_date(df, 'Date')
    # Assert
    assert result_df['Date'].dtype == 'datetime64[ns]'
    assert df['Date'].equals(result_df['Date'])