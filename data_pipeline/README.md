# Data Pipeline

Builds a complete data pipeline using web scraping, data cleaning, data transformation, SQLite database storage, SQL queries, and Pandas operations.

## Project Steps

1. Scrape book data from Books to Scrape website.
2. Randomly select 7 book categories and collect book details.
3. Store the scraped data in a Pandas DataFrame.
4. Clean and transform the data:
   - Convert price from GBP to numeric format.
   - Convert star ratings from words to numbers.
   - Create an in-stock indicator.
   - Convert GBP prices to INR.
5. Create a SQLite database with `books` and `categories` tables.
6. Insert the processed book data into the database.
7. Perform SQL queries using:
   - SELECT and WHERE
   - ORDER BY
   - LIMIT
   - DISTINCT
   - BETWEEN
   - JOIN
8. Perform the same JOIN operation using `pandas.merge()`.
9. Compare the SQL JOIN result with the Pandas merge result.

## Technologies Used

Python, Pandas, BeautifulSoup, Requests, SQLite, SQL

## Database

The SQLite database is stored as `books.db`.

The `books` table contains book details such as title, price, rating, availability, GBP price, stock status, INR price, and category ID.

The `categories` table stores the category ID and category name.
