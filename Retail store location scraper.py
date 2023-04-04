import requests
from bs4 import BeautifulSoup
import csv
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_application")

def extract_store_details(city):
    url = f"https://shop.adidas.co.in/store-locator?city={city}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    stores = soup.find_all('div', {'class': 'store-name'})

    store_details = []

    for store in stores:
        name = store.find('h3').text.strip()
        address = store.find('p', {'class': 'address'}).text.strip()
        timings = store.find('p', {'class': 'timings'}).text.strip()
        phone = store.find('p', {'class': 'phone'}).text.strip()

        
        location = geolocator.geocode(address)
        if location is None:
            latitude = ''
            longitude = ''
        else:
            latitude = location.latitude
            longitude = location.longitude

        store_details.append([name, address, timings, phone, latitude, longitude])

    return store_details


cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur']


all_store_details = []
for city in cities:
    store_details = extract_store_details(city)
    all_store_details.extend(store_details)
    time.sleep(5) 


with open('adidas_stores_india.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Store Name', 'Address', 'Timings', 'Phone', 'Latitude', 'Longitude'])
    for store_detail in all_store_details:
        writer.writerow(store_detail)

