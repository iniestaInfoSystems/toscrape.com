import pandas as pd
import os

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', 20)        



chrome_exe = os.getcwd()+"\\chrome.exe"
chrome_driver_exe = os.getcwd()+"\\chromedriver.exe"


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = chrome_exe
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_argument("--remote-debugging-port=9515") 


driver = webdriver.Chrome(options=options, executable_path=chrome_driver_exe)

driver.get("https://google.com")

driver.get("https://books.toscrape.com/")



book_names = []
prices = []
availabilitys = []
star_ratings = []
landing_urls = []


page_no = 1

while page_no <= 50:
    lnth = driver.execute_script("return document.getElementsByTagName('h3').length")
    for x in range(0, lnth):
       book_name = driver.execute_script("return document.getElementsByTagName('h3')["+str(x)+"].innerText")
       price = driver.execute_script("return document.getElementsByClassName('price_color')["+str(x)+"].innerText")
       availibility = driver.execute_script("return document.getElementsByClassName('instock availability')["+str(x)+"].innerText")
       star_rating = driver.execute_script("return document.getElementsByClassName('star-rating')["+str(x)+"].classList[1]")
       landing_url = driver.execute_script("return document.getElementsByTagName('h3')["+str(x)+"].children[0].href")
       
       book_names.append(book_name)
       prices.append(price)
       availabilitys.append(availibility)
       star_ratings.append(star_rating)
       landing_urls.append(landing_url) 
       
    
    if (driver.execute_script("return document.getElementsByClassName('next').length")>0):
        driver.execute_script("document.getElementsByClassName('next')[0].children[0].click()")    
    page_no = page_no+1
        
data = {
        'Book Name':book_names,
        'Price' : prices,
        'Availability' : availabilitys,
        'Star Ratings' : star_ratings,
        'Landing Page URL' : landing_urls
         }

df =  pd.DataFrame(data)
df.to_csv(os.getcwd()+"\\file.csv", index=None)