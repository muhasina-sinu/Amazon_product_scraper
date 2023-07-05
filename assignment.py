import requests
from bs4 import BeautifulSoup

site = requests.get('https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2 C283&ref=sr_pg_1')

soup = BeautifulSoup(site.text, 'html.parser')

products = soup.find_all('div',{"data-component-type":"s-search-result"})
scraped_data = []

for product in products:
    product_data = {}
    
    link = product.find('a',{"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"},href=True)
    if link:
        product_data['url'] = 'https://www.amazon.in' + link['href']
        
        
    name = product.find('span',{"class":"a-size-medium a-color-base a-text-normal"})
    if name:
        product_data['name'] = name.text
        
    price = product.find('span',{"class":"a-price-whole"})
    if price:
        product_data['price'] = price.text  
         
        
    rating = product.find('span',{"class":"a-icon-alt"})
    if rating:
        product_data['rating'] = rating.text
        
    reviews = product.find('span',{"class":"a-size-base s-underline-text"})
    if reviews:
        product_data['reviews'] = reviews.text
       
        
    scraped_data.append(product_data)
    
print(scraped_data)
    

    

        
 
      
        
        