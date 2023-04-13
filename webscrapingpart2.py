from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


def get_brand(soup):
    try:

        brand = soup.find("tr", attrs={"class": "a-spacing-small po-brand"}).text.strip()

        brand_value = brand.split()

        brand_string = brand_value[1:]

    except AttributeError:
        brand_string = ""

    return brand_string


def get_typename(soup):
    try:

        typename = soup.find("tr", attrs={"class": "a-spacing-small po-model_name"}).text.strip()

        typename_value = typename.split()

        typename_string = typename_value[1:]

    except AttributeError:
        typename_string = ""

    return typename_string


def get_inches(soup):
    try:

        inches = soup.find("tr", attrs={"class": "a-spacing-small po-display.size"}).text.strip()

        inches_value = inches.split()

        inches_string = inches_value[2:]

    except AttributeError:
        inches_string = ""

    return inches_string


def get_cpu(soup):
    try:

        cpu = soup.find("tr", attrs={"class": "a-spacing-small po-cpu_model.family"}).text.strip()

        cpu_value = cpu.split()

        cpu_string = cpu_value[2:]

    except AttributeError:
        cpu_string = ""

    return cpu_string


def get_ram(soup):
    try:

        ram = soup.find("tr", attrs={"class": "a-spacing-small po-ram_memory.installed_size"}).text.strip()

        ram_value = ram.split()

        ram_string = ram_value[4:]

    except AttributeError:
        ram_string = ""

    return ram_string


def get_harddisksize(soup):
    try:

        harddisksize = soup.find("tr", attrs={"class": "a-spacing-small po-hard_disk.size"}).text.strip()

        harddisksize_value = harddisksize.split()

        harddisksize_string = harddisksize_value[3:]

    except AttributeError:
        harddisksize_string = ""

    return harddisksize_string


def get_gpu(soup):
    try:

        gpu = soup.find("tr", attrs={"class": "a-spacing-small po-graphics_coprocessor"}).text.strip()

        gpu_value = gpu.split()

        gpu_string = gpu_value[2:]

    except AttributeError:
        gpu_string = ""

    return gpu_string


def get_operatingsys(soup):
    try:

        operatingsys = soup.find("tr", attrs={"class": "a-spacing-small po-operating_system"}).text.strip()

        operatingsys_value = operatingsys.split()

        operatingsys_string = operatingsys_value[2:]

    except AttributeError:
        operatingsys_string = ""

    return operatingsys_string


def get_price(soup):
    try:

        price = soup.find("span", attrs={'class': 'a-price-whole'})

        price_value = price.text

        price_string = price_value.strip()

    except AttributeError:
        price_string = ""

    return price_string


if __name__ == '__main__':

    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})

    # Initialize the dataframe
    d = {"Brand": [], "typename": [], "inches": [], "cpu": [], "ram": [], "harddisksize": [], "gpu": [],
         "operatingsys": [], "price": []}
    amazon_df = pd.DataFrame.from_dict(d)

    # Loop through multiple pages
    for i in range(1, ):  # loop through first 5 pages
        # The webpage URL
        URL = f"https://www.amazon.in/s?i=computers&rh=n%3A1375424031&fs=true&page={i}&qid=1678285862&ref=sr_pg_{i}"

        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        # Store the links
        links_list = []

        # Loop for extracting links from Tag Objects
        for link in links:
            links_list.append(link.get('href'))

        # Loop for extracting product details from each link
        for link in links_list:
            new_webpage = requests.get("https://www.amazon.in/" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            d['Brand'].append(get_brand(new_soup))
            d['typename'].append(get_typename(new_soup))
            d['inches'].append(get_inches(new_soup))
            d['cpu'].append(get_cpu(new_soup))
            d['ram'].append(get_ram(new_soup))
            d['harddisksize'].append(get_harddisksize(new_soup))
            d['gpu'].append(get_gpu(new_soup))
            d['operatingsys'].append(get_operatingsys(new_soup))
            d['price'].append(get_price(new_soup))

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['Brand'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Brand'])
    amazon_df.to_csv("amazon_data1.csv", header=True, index=False)
amazon_df
