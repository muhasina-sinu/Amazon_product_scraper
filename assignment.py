# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import csv

# Define the function to scrape product information from a search page URL
def scrape(page_url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    # Send a GET request to the Amazon search page
    site = requests.get(page_url, headers=headers)
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(site.text, 'html.parser')
    # Find all product containers on the page
    products = soup.find_all('div',{"data-component-type":"s-search-result"})
    scraped_data = []

    # Iterate through each product container
    for product in products:
        product_data = {}

        # Extract product URL
        link = product.find('a',{"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"},href=True)
        if link:
            product_data['url'] = 'https://www.amazon.in' + link['href']
            
        # Extract product name   
        name = product.find('span',{"class":"a-size-medium a-color-base a-text-normal"})
        if name:
            product_data['name'] = name.text

        # Extract product price
        price = product.find('span',{"class":"a-price-whole"})
        if price:
            product_data['price'] = price.text  
            
        # Extract product rating    
        rating = product.find('span',{"class":"a-icon-alt"})
        if rating:
            product_data['rating'] = rating.text

        # Extract product reviews
        reviews = product.find('span',{"class":"a-size-base s-underline-text"})
        if reviews:
            product_data['reviews'] = reviews.text   

        # Call the scrape_product function to extract additional product details
        product_data = scrape_product(product_data)
        
        scraped_data.append(product_data)
    
    return scraped_data
    
# Define the function to scrape additional product information from a product detail page
def scrape_product(product_data):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Send a GET request to the product detail page
    site = requests.get(product_data['url'], headers=headers)
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(site.text, 'html.parser')

    # Extract product description
    description = soup.find('div',{"id":"feature-bullets"})
    if description:
        product_data['description'] = description.text

    # Extract product information (ASIN and manufacturer)
    information = soup.find('div',{"id":"productDetails_db_sections"})
    if information:
        result = information.find('th',string="ASIN")
        manufacturer = information.find('th',string="manufacturer")
        if result:
            product_data['asin'] = result.find_next_sibling('td').text
            product_data['manufacturer'] = manufacturer.find_next_sibling('td').text
    else:    
        other = soup.find('div',{"id":"detailBullets_feature_div"})
        if other:
            asin = other.find('span',string='ASIN') 
            manufacturer = other.find('span',string="manufacturer")
            if asin and manufacturer:
                product_data['asin'] = asin.find_next_sibling('span').text
                product_data['manufacturer'] = manufacturer.find_next_sibling('span').text

    # Extract product proDescription
    pro_description = soup.find('div',{"id":"productDescription"})
    if pro_description:
        product_data['proDescription'] = pro_description.text
        
    return product_data  
    
    
# Define the base URL for Amazon search results
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"


data = []

# Loop through multiple pages of search results
for page in range(1,21):
    page_url = base_url + '&page=' + str(page)
    page_data = scrape(page_url)
    data.extend(page_data)

# Define the filename for the CSV file
filename = 'product_data.csv'

# Open the CSV file and write data
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[ 'URL', 'Name', 'Price', 'Rating', 'Reviews','description', 'ASIN', 'product Description', 'manufacturer'])
    writer.writeheader()
    
    for product in data:
        url = product.get('url', 'N/A')
        name = product.get('name', 'N/A')
        price = product.get('price', 'N/A')
        rating = product.get('rating', 'N/A')
        reviews = product.get('reviews', 'N/A')
        description = product.get('description','N/A')
        asin = product.get('asin','N/A')
        proDescription = product.get('proDescription','N/A')
        manufacturer = product.get('manufacturer','N/A')
        
        writer.writerow({'URL': url, 'Name': name, 'Price': price, 'Rating': rating, 'Reviews': reviews,'description': description, 'ASIN': asin, 'product Description': proDescription,
                         'manufacturer': manufacturer})
    
print('Data exported successfully to', filename)   


    

    
    
    

    

    
 
      
        
        
