import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import csv
import os
from time import sleep

# Require "todays" time to print
today = date.today()

# Require it in the format MM/DD, year is not needed
todays_date = today.strftime("%d %b")

# Delete previous CSV file if they contain the same name.
filename = 'Rental_Properties_'+ todays_date+'.csv'

if os.path.exists(filename):
    os.remove(filename)

# Create the file with proper Headings
headerList = ["Location","Address","Weekly Rent","Bedrooms","Bathrooms","Furnishing","Date Available","Extra","Listed Date","Link"]
with open(filename,'a',newline='') as file:
    writer = csv.DictWriter(file,delimiter=',',fieldnames=headerList)
    writer.writeheader()

# Only scrapes data off the first page of trade me. i.e 22 listings
url = "https://www.trademe.co.nz/a/property/residential/rent/auckland/auckland-city"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

listings= soup.find_all('a', href=re.compile('/a/property/residential/rent/auckland/auckland-city/'))
room = []
a = 0
for link in listings:
    print("%.2f%%" % (100*(a/len(listings))))
    # Skip the first listing as it is just shows recommended listings which may lead to a double up
    if url == "https://www.trademe.co.nz/a/property/residential/rent/auckland/auckland-city" and a == 0: 
        a += 1
        continue
    # print only 9 listing FOR TESTING PURPOSES dont want to keep requesting to site
    # elif a == 10:
    #    break
    specific_url = "https://www.trademe.co.nz" + link.get('href') 
    page = requests.get(specific_url)
    soup_1 = BeautifulSoup(page.content, "html.parser")


    name_data = soup_1.find(class_="tm-property-listing-body__title p-h1")
    name = re.findall("^[^,]*", name_data.text.strip())[0]
    
    listed_date = soup_1.find(class_="tm-property-listing-body__date")
    # Differentitate between properties listed today and elsewise, need to check if listed string contains the word "Today"
    substring_for_today = "Today"
    if substring_for_today in listed_date.text.strip():
        listed_date = todays_date
    else:
        listed_date = listed_date.text.strip()
        listed_date = listed_date[13:]

    address_raw = soup_1.find("h1")
    address = re.findall("^[^,]*", address_raw.text.strip())[0]

    
    if name == address:
        address = "No specific address given"
    
    price_raw = soup_1.find(class_="tm-property-listing-body__price")
    price = price_raw.text.strip()

    for data in soup_1.find_all(class_="tm-property-listing-attribute-tag__tag--content"):
        room.append(data.text.strip())

    beds = room[0].split()[0]
    bath = room[1].split()[0]
    extra_details = room[2:]
    extra_details = ', '.join(extra_details)


    table_raw = soup_1.find(class_="o-table")
    table_fixed = table_raw.text

    table_avail = table_fixed[0:60]

    avail = re.search('Available(.*)20', table_avail)
    avail = avail.group(1).strip()

    table_furnishing = table_fixed[30:200]
    furnishing_substring = ["Furnished","Fully furnished","Fridge","Yes","yes"]
    nofurnishing_substring = ["No","N","Unfurnished"]
    if any(x in table_furnishing for x in furnishing_substring):
        furnishing = "Furnished"
    elif any(x in table_furnishing for x in nofurnishing_substring):
        furnishing = "Unfurnished"
    else:
        furnishing ='Unknown'




    all_data = [name,address,price.split(" ",1)[0],beds,bath,furnishing,avail,extra_details,listed_date,specific_url]
    
    
    room = []

    with open(filename,'a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(all_data)

    

    

 
        

    
    
    

    #REMOVE LATER FOR TESTING PURPOSES
    a += 1
file.close()
print("DONE in "+str(a)+"  iterations")