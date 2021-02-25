import pandas as pd 
from bs4 import BeautifulSoup
from urllib.request import urlopen 
path = 'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm'
price_list = []
header_list = []
page = urlopen(path)
soup = BeautifulSoup(page,'html.parser') 
table = soup.find(text="Week Of").find_parent("table")

print(table)



