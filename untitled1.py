import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
URL="https://www.flipkart.com/search?q=android+mobile&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_0_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_0_3_na_na_na&as-pos=0&as-type=HISTORY&suggestionId=android+mobile%7CMobiles&requestId=a1b8c37f-9c49-4b65-b083-35469f0e4d4e&page=1"
#for i in range(1,51):
URL = URL.rstrip(URL[-1])
URL=[URL+str(i) for i in range(5)]
#    URL[-1]=i
#print(URL)
page=[]
for j in URL:
    pag=requests.get(j).text
    page.append(pag)
#print(page)
data=[]
item=[]
price=[]
rating=[]
for i in page:
    soup=bs4(i,'html.parser')
#print(soup.prettify())
    data.append(soup.find_all("div", {"class":"_1UoZlX"}))
    item.append([item.find_all(class_="_3wU53n").get_text() for item in data])
#print(item)
    price.append([price.find_all(class_="_1vC4OE _2rQ-NK").get_text() for price in data])
#print(price)
    rating.append([rate.find_all(class_="hGSR34").get_text() for rate in data])
#print(rating)
dict={"ITEM":item,"PRICE":price,"RATING":rating}
df=pd.DataFrame(dict)
df.to_csv(r"C:\Users\Mani\Desktop\flipkart.csv",index=False)
print(df)
#print(product_name.text)
#ttl=data.find(class_="_3wU53n")
#print(data)
#product_name = []
#for item in data:
#    name = item.find_all("div",{"class":"col col-7-12"})
#    product_name.append(name.get("title"))
#print(data)