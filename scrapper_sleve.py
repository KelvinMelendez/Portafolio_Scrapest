from bs4 import BeautifulSoup
import time,requests,datetime

from db import gettingUrls,updating_urlstatus,insertdataoffer,insertarError

def gettingInformation(orderid,url):
    """This function is used fot getting the important information from the webpage.
        Variables such as: Location, price, # rooms, # bathrooms, weather will be scrapped
    """
    #Defining Dict Results
    fields=["Área privada","Área Const","Clima","Sector","Precio"]
    results={
        "Precio":"na",
        "Sector":"na",
        "Clima":"na",
        "Área Const":"na",
        "Área privada":"na",
        "Hab":"na",
        "Baños":"na"

    }

    #Making request
    r=requests.get(url)
    html=r.text
    del(r)

    #Making soap

    #This loop looks for fields: weather and site
    html=BeautifulSoup(html,'html.parser')
    info=html.find_all("li")
    for elements in info:
        textElement=elements.get_text()
        #print(textElement)
        for field in fields:
            if field in textElement:
                results[field]=textElement.replace("$","").replace("/","").replace("m²","").replace(":","").replace(field,"").replace("\r","").replace("\n","").replace("'","").replace(" ","")
                if len(results[field])<30: #Only remove when size of string is less than 30. This means continue looking for
                    fields.remove(field)
                break
        if len(fields)<1:
            break

    #This loop looks for fields: Inmueble , Hab y Baños
    tableContainer=html.find_all(id="typology")
    columns=[]
    rows=[]
    for element in tableContainer:
        table=element.find("table")
        for element2 in table.thead.tr.find_all("td"):
            columns.append(element2.get_text()) #adding columns of the table
        
    #Looping Rows of the table
    tableContainer=html.find_all(id="typology")
    for element in tableContainer:
        table=element.find("table")
        for element2 in table.tbody.tr.find_all("td"):
            #print(element2.get_text())
            rows.append(element2.get_text().replace("$","").replace("\r","").replace("\n","").replace(" ",""))
    
    #Creating dictionary of the table
    counter=0
    for column in columns:
        results[column]=rows[counter]
        counter+=1

    #------ Second Try looking for rooms and baths---------------
    rooms=html.find_all("span",class_="advertRooms")
    for room in rooms:
        value_room=room.get_text().replace("Habitaciones:","").replace("$","").replace("\n","").replace("\r","").replace(" ","")

    bath_rooms=html.find_all("span",class_="advertBaths")
    for bath in bath_rooms:
        value_bath=bath.get_text().replace("Baños:","").replace("$","").replace("\n","").replace("\r","").replace(" ","")

    if value_room!=None:
        results["Hab"]=value_room
    if value_bath!=None:
        results["Baños"]=value_bath
    #------------------------------------------------------------

    #Adding information to mongodb
    insertdataoffer(orderid,url,results)

    #Udating url
    updating_urlstatus(orderid,url)


#Bucle principal del proceso
while True:
    url="notdefined"
    try:
        #Getting urls not completed
        urls=gettingUrls()
        if len(urls)>0:
            for tuple_url in urls:
                url=tuple_url[1]
                orderid=tuple_url[0]
                gettingInformation(orderid,url)
                print("URL Completed")
        else:
            print("Waiting 1 hour to start over")
            time.sleep(10)
    except Exception as e:
        print(str(e))
        insertarError(url,str(e))
