# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import modules.scraper as scr

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="A+R Store Product Information Scraper",
        page_icon="🛋️",
    )

    st.write("# A+R Store Product Information Scraper! 🛋️")

    st.markdown(
        """
        To utilize this tool, kindly click the "Scrape" button. Please be patient for a few seconds, and subsequently, you will be able to download the CSV file containing the scraped data. Additionally, the tool will include general statistics regarding the collected information about the products in the A+R Store.
    """
    )
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
      st.write("#### Start scraping")
      st.button("Scrape", on_click = scr.extract_data)
    with col2:
      st.write("#### Download data")
      if 'final_dataframe' not in st.session_state:
        st.info("Waiting for scraped data", icon = "😶‍🌫️")
      else:
        st.download_button(
            label="Download data as CSV",
            data=st.session_state.final_dataframe,
            file_name='aplusrstore_products.csv'
        )

    st.write("---")
    st.write("#### Data statistics")
    if 'final_dataframe' not in st.session_state:
      st.info("Waiting for scraped data", icon = "😶‍🌫️")
    else:
      col1, col2, col3 = st.columns(3)
      col1.metric(label="Total pages scraped", value = st.session_state.total_pages)
      col2.metric(label="Total products scraped", value = st.session_state.total_products)
      col3.metric(label="Total variants scraped", value = st.session_state.total_variants)
      col1.metric(label="% Variants with SKU info", value = st.session_state.percentage_sku_non_null)
      col2.metric(label="% Variants with price info", value = st.session_state.percentage_price_non_null)
      col3.metric(label="% Variants with weight info", value = st.session_state.percentage_grams_non_null)


if __name__ == "__main__":
    run()
