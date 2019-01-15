import requests
import bs4
import xml
import mysql.connector

mydb = mysql.connector.connect(                                                        #DB Setup
    host = "",
    user = "",
    passwd = "",
    database= "")

mycursor = mydb.cursor()

url = "https://boardgamer.ie/best-sales"                                               
pageReq = requests.get(url)                                                            #Get source
soup = bs4.BeautifulSoup(pageReq.text, 'xml')                                          #create object of bs4
data = soup.findAll('div', {'class':['product-container']})                            #get rid of useless HTML
listOfTitles = []                                                                      #3 list[] instead of
listOfDescriptions = []                                                                # 1 list[][], for read-
listofPrices = []                                                                      # abllity and example 
idx = 0                                                                                # matters

for i in data:
    tempTitle = i.findAll('a', title=True)                         #find all 'a' tags that contain title atribute
    listOfTitles.append(tempTitle[0]['title'])                     # and populate the list
    tempDescription = i.findAll('p', {'class': ['product-desc']})  #find all 'p' tags in a 'product-des' class
    listOfDescriptions.append(tempDescription[0].text)
    tempPrice = i.findAll('span')                                  #find all 'span' tags 
    listofPrices.append(tempPrice[0].text.split(' ')[2])           #split the return value at space to remove the
                                                                   #currentcy sing, and unnecessary characters
i = 1
for l in listOfTitles:
    sql = "INSERT INTO BoardGames (Position, Name, Description, Price, Source) VALUES (%s, %s, %s, %s, %s)"
    val = (i, listOfTitles[i], listOfDescriptions[i], listofPrices[i], url)            #standard SQL statements
    mycursor.execute(sql, val)
    mydb.commit()
    i += 1
