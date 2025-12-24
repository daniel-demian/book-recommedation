import pandas as pd
import numpy as np
from etl import load_data

def recommend_books(dataset: pd.DataFrame, book_title: str, min_ratings: int = 8, top_n: int = 10):
    
    if not book_title:
        print(f"No close match found for '{user_input}'. Please check spelling.")
        return None, None
    
    print(f"Matched book: '{book_title}'")
    
    # Users who read this book
    readers = dataset.loc[dataset['Book-Title'] == book_title, 'User-ID'].unique()
    subset = dataset.loc[dataset['User-ID'].isin(readers)]
    
    # Filter books with enough ratings
    rating_counts = subset.groupby('Book-Title').size()
    books_to_compare = rating_counts[rating_counts >= min_ratings].index.tolist()
    
    if book_title not in books_to_compare:
        print(f"Not enough ratings for '{book_title}' to compute correlations.")
        return None, None
    
    # Pivot table for correlations
    ratings_matrix = subset[subset['Book-Title'].isin(books_to_compare)].pivot_table(
        index='User-ID',
        columns='Book-Title',
        values='Book-Rating',
        aggfunc='mean'
    )
    
    ratings_matrix_other = ratings_matrix.drop(columns=[book_title])
    correlations = ratings_matrix_other.corrwith(ratings_matrix[book_title]).dropna()
    
    # Build recommendations DataFrame
    avg_ratings = subset.groupby('Book-Title')['Book-Rating'].mean()
    recommendations = pd.DataFrame({
        'book': correlations.index,
        'corr': correlations.values,
        'avg_rating': avg_ratings[correlations.index].values
    })
    
    # Merge with full book info
    book_info = dataset.drop_duplicates(subset=['Book-Title']).set_index('Book-Title')
    top_books = recommendations.sort_values(['corr', 'avg_rating'], ascending=False).head(top_n)
    worst_books = recommendations.sort_values(['corr', 'avg_rating'], ascending=True).head(top_n)
    top_books_full = top_books.join(book_info, on='book')
    worst_books_full = worst_books.join(book_info, on='book')

    return top_books_full, worst_books_full

# -------------------------------
# Main Execution
# -------------------------------

if __name__ == "__main__":
    dataset = load_data('./data/BX-Book-Ratings.csv', './data/BX-Books.csv')
    
    #the fellowship of the ring (the lord of the rings, part 1)

    print("Book Recommendation")
    print("Type a book title to get recommendations.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a book title: ").strip().lower()

        if user_input == "exit":
            print("\nGoodbye")
            break

        if not user_input:
            print("Please enter a valid book title.\n")
            continue
        
        top10, worst10 = recommend_books(dataset, user_input)
    
        if top10 is not None:
            print("Top 10 Recommendations:")
            print(top10[['book','ISBN','Book-Author','Publisher','Year-Of-Publication','avg_rating','corr']])
            print("\n10 Worst Recommendations:")
            print(worst10[['book','ISBN','Book-Author','Publisher','Year-Of-Publication','avg_rating','corr']])
        print("\n" + "-" * 80 + "\n")
