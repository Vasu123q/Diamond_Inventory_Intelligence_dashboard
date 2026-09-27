import pandas as pd

def clean_text(series: pd.Series) -> pd.Series:
    """
    Removes hidden Excel characters and normalizes text.
    Fixes:
    - Non-breaking space (\xa0)
    - Tabs
    - Newlines
    - Extra spaces
    - Mixed casing
    """
    return (
        series.astype(str)
        .str.replace('\xa0', ' ', regex=False)   # MOST IMPORTANT
        .str.replace('\t', ' ', regex=False)
        .str.replace('\r', ' ', regex=False)
        .str.replace('\n', ' ', regex=False)
        .str.strip()
    )


def apply_hidden_space_removal(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Applies cleaning to multiple columns in a dataframe.
    """
    for col in columns:
        if col in df.columns:
            df[col] = clean_text(df[col])
    return df