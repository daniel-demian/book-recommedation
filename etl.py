import pandas as pd

def extract_ratings(path: str) -> pd.DataFrame:
    """Extract ratings CSV into DataFrame"""
    dtype = {"User-ID": int, "ISBN": str, "Book-Rating": int}
    df = pd.read_csv(path, sep=',', encoding='cp1251', dtype=dtype, on_bad_lines='skip', low_memory=False)
    return df

def extract_books(path: str) -> pd.DataFrame:
    """Extract books CSV into DataFrame"""
    dtype = {"ISBN": str, "Book-Title": str, "Book-Author": str, 
             "Year-Of-Publication": str, "Publisher": str}
    df = pd.read_csv(path, sep=',', encoding='cp1251', dtype=dtype, on_bad_lines='skip', low_memory=False)
    return df

def transform_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only rated books (Book-Rating > 0)"""
    return df[df['Book-Rating'] > 0]

def transform_books(df: pd.DataFrame) -> pd.DataFrame:
    """Clean book info: lowercase text columns, drop missing ISBN/title"""
    text_cols = ['Book-Title', 'Book-Author', 'Publisher']
    for col in text_cols:
        df[col] = df[col].str.lower().str.strip()
    df = df.dropna(subset=['ISBN', 'Book-Title'])
    return df

def load_data(ratings_path: str, books_path: str) -> pd.DataFrame:
    """Full ETL pipeline: extract, transform, and merge datasets"""
    ratings = transform_ratings(extract_ratings(ratings_path))
    books = transform_books(extract_books(books_path))
    dataset = pd.merge(ratings, books, on='ISBN')
    return dataset
