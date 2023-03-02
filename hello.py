import requests
from bs4 import BeautifulSoup

URL = "https://www.trademe.co.nz/a/property/residential/rent/auckland/auckland-city"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

job_elements = soup.find_all(class_="tm-property-premium-listing-card__link")

for job_element in job_elements:
    # name_element = job_element.find(class_="")
    bed_element = job_element.find(class_="tm-property-search-card-attribute-icons__metric-value")
    # print(name_element)
    print(bed_element.text)
