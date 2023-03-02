import requests
from bs4 import BeautifulSoup
import re

# Only scrapes data off the first page of trade me. i.e 22 listings
url = "https://www.trademe.co.nz/a/property/residential/rent/auckland/auckland-city"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls =[]
a = 0
for link in soup.find_all('a', href=re.compile('/a/property/residential/rent/auckland/auckland-city/')):
    # Skip the first listing as it is just shows recommended listings which may lead to a double up
    if a == 0: 
        a += 1
        continue
    #print only 4 listing FOR TESTING PURPOSES dont want to keep requesting to site
    # elif a == 5:
    #     break
    specific_url = "https://www.trademe.co.nz" + link.get('href') 
    page = requests.get(specific_url)
    soup_1 = BeautifulSoup(page.content, "html.parser")


    name_data = soup_1.find(class_="tm-property-listing-body__title p-h1")
    name = re.findall("^[^,]*", name_data.text.strip())[0]
        
    address_raw = soup_1.find("h1")
    address = re.findall("^[^,]*", address_raw.text.strip())[0]

    price_raw = soup_1.find(class_="tm-property-listing-body__price")
    price = price_raw.text.strip()
    
    print('{:<0} {:>12} {:>12}'.format(name, "",price))
    if name == address:
        print("No specific address given")
    else:
        print(address)
    
    for data in soup_1.find_all(class_="tm-property-listing-attribute-tag__tag--content"):
        print(data.text.strip())
    print("--------------------------------------------------")

    # #REMOVE LATER FOR TESTING PURPOSES
    # a += 1
    
