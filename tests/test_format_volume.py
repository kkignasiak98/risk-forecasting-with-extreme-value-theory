import pandas as pd
import pytest
from data_cleaner import format_volume

def test_format_volume_when_column_is_already_numeric():
    # Arrange
    df = pd.DataFrame({'Volume': [98.7, 50.0, 2.3]})
    # Act
    result_df = format_volume(df, 'Volume')
    # Assert
    assert result_df['Volume_new'].equals(df['Volume'])

def test_format_volume_when_text_format_should_convert_to_float():
    # Arrange
    df = pd.DataFrame({'Volume': ['98.7M', '50.0M', '2.3B']})
    expected_df = pd.DataFrame({'Volume': [98700000.0, 50000000.0, 2300000000.0]})
    # Act
    result_df = format_volume(df, 'Volume')
    # Assert
    assert result_df['Volume_new'].equals(expected_df['Volume'])

def test_format_volume_when_column_has_no_suffix():
    # Arrange
    df = pd.DataFrame({'Volume': ['98.7', '50.0', '2.3']})
    expected_df = pd.DataFrame({'Volume': [98.7, 50.0, 2.3]},dtype=float)
    # Act
    result_df = format_volume(df, 'Volume')
    # Assert
    assert result_df['Volume_new'].equals(expected_df['Volume'])
