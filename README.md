# Amazon Product Scraper

## Overview

This Python script is designed to scrape product information from Amazon. It utilizes the `BeautifulSoup` library for HTML parsing and `csv` for exporting the data to a CSV file. The primary purpose of the script is to scrape multiple pages of Amazon search results for a specific product category and extract detailed information about the products.

## Prerequisites

Before using the script, ensure that you have the following libraries installed:

- `requests`
- `BeautifulSoup`
- `csv`

## Usage

The scrape function extracts product information from a provided Amazon search page URL and returns a list of dictionaries containing product data.

The scrape_product function is responsible for scraping additional product details from a product's detail page. It is called by the scrape function for each product found on the search page.

Set the base URL for the Amazon search results page you intend to scrape.

Initialize an empty list called data to store the scraped product data.

Loop through multiple pages of search results, calling the scrape function for each page and appending the results to the data list.

Determine the filename for the CSV file where you want to export the scraped data (e.g., 'product_data.csv').

Open the CSV file in write mode and use csv.DictWriter to write the header row and the scraped data to the file.

Print a success message indicating that the data has been successfully exported.
