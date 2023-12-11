# A+R Store Product Information Scraper 🛋️

## Overview

This tool allows you to scrape product information from the A+R Store and provides general statistics about the collected data. The scraped information includes details about products, variants, and more.

Try here: https://arstoreitem-informationscraper.streamlit.app/

## Installation

To run the scraper, you need to have Python and Streamlit installed. You can install the required dependencies using the following commands:

```bash
pip install streamlit
```
## Usage

1- Clone this repository: 
```bash
git clone https://github.com/elchristog/a-r-store-item-information-scraper
cd your-repository
```

2- Run the Streamlit app:
```bash
streamlit run your_script.py
```

3- Open the provided URL in your browser and use the following steps:
- Click the "Scrape" button to initiate the scraping process.
- Wait for a few seconds for the scraping to complete.
- Once done, you can download the scraped data as a CSV file using the "Download data" button

## Functions

#### extract_info(html: str) -> tuple:
- This function takes an HTML string as input.
- It uses BeautifulSoup to parse the HTML content.
- Tries to find and extract the product description, size, and material from specific HTML tags.
- Returns a tuple containing description, size, and material information.
- If any of the information is not found, it returns None for that particular value.

#### @st.cache_data(ttl=21600, show_spinner=False)
- This is a decorator from the Streamlit library that caches the result of the function to improve performance.
- ttl specifies the time-to-live for the cache in seconds (21600 seconds or 6 hours in this case).
- show_spinner is set to False to hide the spinner while the function is being executed.

#### extract_data():
- This function extracts data from the A+R Store API in a paginated manner.
- It sends HTTP GET requests to the API with a specified template URL and iterates through pages.
- For each page, it retrieves JSON data, extracts information using the extract_info function, and normalizes the data into a Pandas DataFrame.
- Various DataFrame manipulations are performed to structure the data.
- Metrics such as the total number of products, pages, and percentages of non-null values for specific columns are calculated.
- The final DataFrame is saved as a CSV file.
- Metrics and the final DataFrame are saved in Streamlit's session state for further use in the Streamlit app.