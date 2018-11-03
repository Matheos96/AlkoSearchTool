# -*- coding: utf-8 -*-

'''
Alko Search Tool 0.1
Made by Matheos Mattsson 2018

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

#defaults
get_url = 'https://www.alko.fi/tuotteet?SearchTerm='
sorting = 'name-asc' #By name, ascending

def set_sorting():
	print("\n**************Select sorting method**************\n"+
	"1. Alphabetical Order A-Ö (default)\n"+
	"2. Alphabetical Order Ö-A"+
	"\n3. By Price, lowest first\n"+
	"4. By Price, highest first\n")
	option = input("Select an option: ")
	global sorting
	if option=='1':
		sorting = 'name-asc'
	elif option=='2':
		sorting = 'name-desc'
	elif option=='3':
		sorting = 'priceWithPant-asc'
	elif option=='4':
		sorting = 'priceWithPant-desc'

def printProducts(uri, searchTerm, nr_of_pages):
	product_no = 1
	for nr in range(nr_of_pages):	
		url = uri + '&PageNumber='+str(nr)
		page = client.get(url)
		parsed = BeautifulSoup(page.content, 'lxml')
		products_html_list = parsed.findAll('div', attrs={'role': 'listitem'})
		print("\n**************Search term: '"+searchTerm+"' Page number: "+str(nr+1)+"/"+str(nr_of_pages)+"**************\n")
		for p in products_html_list:
			print(str(product_no)+". "+str(p.find('h4', attrs={'class': 'product-name-aria'}).text.strip()) + " " +
			str(p.find('div', attrs={'class': 'product-volume'}).text.strip())+"  "+
			str(p.find('span', attrs={'class': 'price price-wrapper module-price'}).get('content'))+"€")
			print("-------------------------------------------------------------")
			product_no+=1
		
	return 


def search():
	searchTerm = str(input("Enter search term: "))
	url = get_url+searchTerm
	page = client.get(url) 
	parsed = BeautifulSoup(page.content, 'lxml')
	search_url = str(parsed.find('form', attrs={'name': 'paginating'}).get('action'))
	searchParameter = str(parsed.find('input', attrs={'name': 'SearchParameter'}).get('value'))
	nr_of_pages = int(int(parsed.find('span', attrs={'class': 'color-primary'}).text.strip())/12)+1 # Paging starts at 0
	search_url+='&SearchTerm='+searchTerm+'&PageSize=12&SearchParameter='+searchParameter+'&SortingAttribute='+sorting
	printProducts(search_url,searchTerm, nr_of_pages)

 
print("---------------------- Welcome to Alko Search Tool 0.1 ----------------------\n")
while True:
	try:
		print("\n**************Select action**************\n"+
		"1. Search\n"+
		"2. Set sorting method\n"+
		"Type 'exit' to quit")
		response = input("Select an option (default: 1): ")
		if response=="":
			response = '1'
		
		if response=='1':
			search()
		elif response=='2':
			set_sorting()
		elif response=='exit':
			break
		else:
			print("Not a valid option!")
	except Exception as e:
		print(e)
		pass
		

