import pandas as pd
import pytest
from data_cleaner import clean_numeric_data

def test_clean_numeric_data_when_columns_with_dots_should_clean():
    # Create a sample DataFrame with numeric columns
    df = pd.DataFrame({
        'A': ['10,000', '20,000', '30,000'],
        'B': ['40,000', '50,000', '60,000']
    })

    cleaned_df = clean_numeric_data(df, ['A', 'B'])

    # Check if commas are removed and columns are converted to float
    assert cleaned_df['A'].equals(pd.Series([10000.0, 20000.0, 30000.0]))
    assert cleaned_df['B'].equals(pd.Series([40000.0, 50000.0, 60000.0]))

def test_clean_numeric_data_when_columns_without_dots_should_return_the_same():
    # Create a sample DataFrame with numeric columns
    df = pd.DataFrame({
        'A': ['10000.0', '20000.0', '30000.0'],
        'B': ['40000.0', '50000,0', '60000.0']
    })

    cleaned_df = clean_numeric_data(df, ['A', 'B'])

    assert cleaned_df['A'].equals(df['A'])
    assert cleaned_df['B'].equals(df['B'])

def test_clean_numeric_data_when_no_numeric_columns_should_return_the_same():
    # Create a sample DataFrame with numeric columns
    df = pd.DataFrame({
        'A': ['Apple', 'Banana', 'Carrot'],
        'B': ['Dog', 'Cat', 'Panda']
    })

    cleaned_df = clean_numeric_data(df, [])

    assert df.equals(cleaned_df)
