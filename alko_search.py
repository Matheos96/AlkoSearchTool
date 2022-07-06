# -*- coding: utf-8 -*-

'''
Alko Search Tool 0.3
Made by Matheos Mattsson 2018
Updated 06/07/2022

PYTHON 3 ONLY

Requirements:
- BeautifulSoup4
- requests
- lxml

Feel free to reuse in any way shape or form you may want!
'''

import requests
from bs4 import BeautifulSoup

client = requests.session()

# defaults
GET_URL = 'https://www.alko.fi/tuotteet?SearchTerm='
SORTING = 'name-asc'  # By name, ascending
SEARCH_URL_DEFAULT = "https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewParametricSearch-" \
                     "ProductPagingRandom?Context=ViewParametricSearch-ProductPagingRandom"


def set_sorting():
    print('\n************** Select sorting method **************\n' \
          '1. Alphabetical Order A-Ö (default)\n' \
          '2. Alphabetical Order Ö-A\n' \
          '3. By Price, lowest first\n' \
          '4. By Price, highest first\n')
    option = input('Select an option: ')
    global SORTING
    if option == '1':
        SORTING = 'name-asc'
    elif option == '2':
        SORTING = 'name-desc'
    elif option == '3':
        SORTING = 'priceWithPant-asc'
    elif option == '4':
        SORTING = 'priceWithPant-desc'


def print_products(uri, search_term, nr_of_pages):
    product_no = 1
    for nr in range(nr_of_pages):
        page = client.get(f'{uri}&PageNumber={nr}')
        parsed = BeautifulSoup(page.content, 'lxml')
        products_html_list = parsed.findAll('div', attrs={'role': 'listitem'})
        print(f'\n************** Search term: \'{search_term}\' Page number: {nr + 1}/{nr_of_pages} **************\n')
        for p in products_html_list:
            print(f'{product_no}. {p.find("h4", attrs={"class": "product-name-aria"}).text.strip()} {p.find("div", attrs={"class": "mc-volume"}).text.strip()}'  \
                f'  {p.find("span", attrs={"itemprop": "price"}).get("content")} €')
            print('---------------------------------------------------------------------------')
            product_no += 1


def search():
    search_term = input('Enter search term: ')
    page = client.get(GET_URL + search_term)
    parsed = BeautifulSoup(page.content, 'lxml')
    search_parameter = parsed.find('input', attrs={'name': 'SearchParameter'}).get('value')
    try: 
        nr_of_pages = int(parsed.find('span', attrs={'class': 'color-primary'}).text.strip()) // 12 + 1  # Paging starts at 0
        search_url = f'{SEARCH_URL_DEFAULT}&SearchTerm={search_term}&PageSize=12&SearchParameter={search_parameter}&SortingAttribute={SORTING}'
        print_products(search_url, search_term, nr_of_pages)
    except:
        print(f'\nNo products matching \'{search_term}\' could be found.\n')


if __name__ == '__main__':
    print("---------------------- Welcome to Alko Search Tool 0.3 ----------------------\n")
    while True:
        try:
            print('\n************** Select action **************\n' \
                '1. Search\n' \
                '2. Set sorting method\n' \
                'Type \'exit\' to quit')
            
            response = input('Select an option (default: 1): ')
            
            if response == '1' or response == '':
                search()
            elif response == '2':
                set_sorting()
            elif response == 'exit':
                break
            else:
                print('Not a valid option!')
        except Exception as e:
            print(e)
            pass
