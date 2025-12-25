DATASET
-------
This project uses the Book Recommendation Dataset from Kaggle.

Download the dataset from:
https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset

After downloading, place the following files into the data/ directory:

data/
- Book-Ratings.csv
- Books.csv


INSTALLATION
------------
Clone the repository:

git clone https://github.com/daniel-demian/book-recommedation.git
cd book-recommender

Create a virtual environment:

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt


RUN APPLICATION
---------------
Start the Streamlit app:

streamlit run app.py

Then open your browser at:

http://localhost:8501
