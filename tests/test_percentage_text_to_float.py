import pandas as pd
import pytest
from data_cleaner import percentage_text_to_float

def test_percentage_text_to_float_when_text_format_should_convert_to_float():
    # Arrange
    df = pd.DataFrame({'percentage': ['98.7%', '50.0%', '2.3%']})
    expected_df = pd.DataFrame({'percentage': [98.7, 50.0, 2.3]})
    # Act
    result_df = percentage_text_to_float(df, 'percentage')
    # Assert
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_percentage_text_to_float_when_column_is_already_numeric():
    # Arrange
    df = pd.DataFrame({'percentage': [98.7, 50.0, 2.3]})
    # Act
    result_df = percentage_text_to_float(df, 'percentage')
    # Assert
    pd.testing.assert_frame_equal(result_df, df)


