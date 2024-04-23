import pandas as pd
import arrow

def clean_numeric_data(df:pd.DataFrame, numeric_columns:list)-> pd.DataFrame:
    """
    Cleans the numeric data in a pandas DataFrame by replacing commas with empty strings and casting the specified columns to float.

    Args:
        df (pd.DataFrame): The DataFrame containing the numeric data.
        numeric_columns (list): A list of column names to be cleaned.

    Returns:
        pd.DataFrame: The DataFrame with the cleaned numeric data.
    """
    df[numeric_columns] = df[numeric_columns].replace(',','',regex = True) # From "103,00.00" -> "10300.00"
    # Cast the specified columns to float
    df[numeric_columns] = df[numeric_columns].astype(float)

    return(df)

def format_volume(df:pd.DataFrame,column_name:str)-> pd.DataFrame:
    """
    A function to format volume data in a DataFrame by converting the specified column from the string representation with M or B suffixes representing millions or billions, respectively, to a float.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column containing the volume data.

    Returns:
        pd.DataFrame: The DataFrame with formatted volume data, including a new column with the calculated volume.
    """
    new_column = f"{column_name}_new"
    # Check if the column can be casted to numeric
    try:
        df[new_column] = df[column_name].astype(float)
        return(df)
    except:
        pass
    df['Vol_amount'] = df[column_name]
    df['Vol_magnitude'] = df[column_name]

    regex_million = r'(\d+\.\d+)M'
    regex_billion = r'(\d+\.\d+)B'
    df['Vol_amount'] = df['Vol_amount'].replace({regex_million: r'\1',regex_billion: r'\1' },regex = True)
    df['Vol_magnitude'] = df['Vol_magnitude'].replace({regex_million: r'1000000',regex_billion: r'1000000000' },regex = True)

    df[['Vol_amount','Vol_magnitude']] = df[['Vol_amount','Vol_magnitude']].astype(float)
    df[new_column] = df['Vol_amount'] * df['Vol_magnitude']
    df = df.drop(['Vol_amount', 'Vol_magnitude'], axis=1)

    return(df)

def percentage_text_to_float(df:pd.DataFrame,column_name:str)-> pd.DataFrame:
    """
    Converts a column of percentage values in a DataFrame from text format to float format.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the column to be converted.
        column_name (str): The name of the column to be converted.

    Returns:
        pd.DataFrame: The DataFrame with the converted column.

    Example:
        >>> df = pd.DataFrame({'percentage': ['98.7%', '50.0%', '2.3%']})
        >>> percentage_text_to_float(df, 'percentage')
           percentage
        0       98.70
        1       50.00
        2        2.30
    """
    df[column_name] = df[column_name].replace('[\%,]', '', regex=True).astype(float)
    return(df)

def parse_date(df:pd.DataFrame, column:str)->pd.DataFrame:
    """
    Parses the given column of a DataFrame using the arrow library and returns the modified DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be modified.
        column (str): The name of the column to be parsed.

    Returns:
        pd.DataFrame: The modified DataFrame with the parsed column.
    """
    if df[column].dtype == 'datetime64[ns]':
        return df
    df[column] = df[column].apply(lambda x: arrow.get(x, "MMM DD, YYYY"))
    df[column] = df[column].apply(lambda x: pd.to_datetime(f"{x.year}--{x.month}--{x.day}"))
    df[column] = df[column].astype('datetime64[ns]')
    return(df)