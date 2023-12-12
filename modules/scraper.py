import requests
import pandas as pd
import streamlit as st

from bs4 import BeautifulSoup

def extract_info(html: str) -> tuple:
    """
    Extracts information from HTML using BeautifulSoup.

    Args:
        html (str): The HTML content to parse.

    Returns:
        tuple: A tuple containing description, size, and material information.

    Raises:
        None

    Example:
        >>> html_content = "<html>...</html>"
        >>> extract_info(html_content)
        ('Product description', 'Large', 'Cotton')
    """
    # Check if html is None, and return default values if it is
    if html is None:
        return None, None, None
        
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract description
    try:
        description = soup.find('h2', string='Description').find_next('p').text.strip()
    except AttributeError:
        description = None

    # Extract size
    try:
        size = soup.find('h4', string='Size').find_next('span').text.strip()
    except AttributeError:
        size = None

    # Extract material
    try:
        material = soup.find('h4', string='Material').find_next('p').text.strip()
    except AttributeError:
        material = None

    # Return the extracted information as a tuple
    return description, size, material




def extract_data():
    """
    Extracts data from the A+R Store API, processes and normalizes it, and exports the final DataFrame to a CSV file.

    Returns:
        None

    Raises:
        Exception: If there is an error fetching data from the API.

    Example:
        extract_data()
    """

    url_template = "https://aplusrstore.com/products.json?page={}&limit=250"
    total_products = 0
    current_page = 1

    # List to store all DataFrames
    all_dataframes = []

    while True:
        # Showing page info
        st.toast(f"Scrapping page: {current_page}")

        # Make an HTTP GET request
        response = requests.get(url_template.format(current_page))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data
            json_data = response.json()

            # Get the total number of products on the current page
            products_on_page = len(json_data)
            total_products += products_on_page

            # Check if there are more pages
            if products_on_page == 0:
                break

            # Extract product data
            for item in json_data['products']:
                description, size, material = extract_info(item['body_html'])
                first_product_image = next((image['src'] for image in item['images'] if not image['variant_ids']), None)

                item.update({
                    'description': description,
                    'size': size,
                    'material': material,
                    'first_product_image': first_product_image
                })
                del item['body_html']
                del item['images']

            # Normalize the JSON data and extract variants
            normalized_df = pd.json_normalize(json_data["products"], 'variants',
                                               ['id', 'title', 'handle', 'published_at', 'created_at', 'vendor',
                                                'product_type', 'tags', 'description', 'size', 'material',
                                                'first_product_image'], record_prefix="variant_")

            # Append the DataFrame to the list
            all_dataframes.append(normalized_df[['id', 'title', 'handle', 'published_at',
                                                 'created_at', 'vendor', 'product_type', 'tags', 'description', 'size',
                                                 'material', 'first_product_image', 'variant_id', 'variant_title', 'variant_option1',
                                                 'variant_sku', 'variant_requires_shipping', 'variant_taxable',
                                                 'variant_available', 'variant_price', 'variant_grams',
                                                 'variant_created_at', 'variant_featured_image.src']])

            # Move to the next page
            current_page += 1
            break
        else:
            raise Exception(f"Error: Unable to fetch data. Status code: {response.status_code}")

    # Concatenate all DataFrames into one
    final_dataframe = pd.concat(all_dataframes, ignore_index=True)

    # Specify the limit per page
    limit_per_page = 250

    # Calculate the total number of pages
    total_pages = (total_products + limit_per_page - 1) // limit_per_page

    # Calculate completitude metrics
    percentage_sku_non_null = (final_dataframe['variant_sku'].notnull().sum() / len(final_dataframe)) * 100
    percentage_price_non_null = (final_dataframe['variant_price'].notnull().sum() / len(final_dataframe)) * 100
    percentage_grams_non_null = (final_dataframe['variant_grams'].notnull().sum() / len(final_dataframe)) * 100
    
    # Saving metrics as session state
    st.session_state.total_pages = total_pages
    st.session_state.total_products = total_products
    st.session_state.total_variants = len(final_dataframe)
    st.session_state.percentage_sku_non_null = percentage_sku_non_null
    st.session_state.percentage_price_non_null = percentage_price_non_null
    st.session_state.percentage_grams_non_null = percentage_grams_non_null

    # Save df as session state
    st.session_state.final_dataframe = final_dataframe.to_csv(index=False).encode("utf-8")

    
