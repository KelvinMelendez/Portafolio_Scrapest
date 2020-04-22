import mysql.connector
import json,datetime


#Reading db settings
settings=json.loads(open("db_settings.json").read())


def initialverifications():
    """ This function is used for making initial verifications such as:
    1- Check if connection is correct: database exists, table exists and so on.
    2- If database or table is not created. It will be created
    """
    errors=[]

    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"]
    )

    #Check if database exists
    cursor=connection.cursor()
    cursor.execute("SHOW DATABASES")
    for database in cursor:
        print(database)
        if settings["database_name"] in database:
            errors.append("Database exists! :)")
            break
    
    #Creating Database in case does not exists
    if "Database exists! :)" in errors:
        connection = mysql.connector.connect(
            host=settings["ip"],
            user=settings["user"],
            passwd=settings["password"],
            database=settings["database_name"]
        )
    else:
        cursor.execute("CREATE DATABASE "+settings["database_name"])
        connection = mysql.connector.connect(
            host=settings["ip"],
            user=settings["user"],
            passwd=settings["password"],
            database=settings["database_name"]
        )

    #Checking if table exists
    cursor=connection.cursor()
    cursor.execute("SHOW TABLES")
    for table in cursor:
        if "scrapping_orders" in table:
            errors.append("table orders exists")

        if "scrapping_urls" in table:
            errors.append("table urls exists")

        if "data_offers" in table:
            errors.append("table data offers exists")
    
    #Creating Tables if they dont exists
    if "table orders exists" not in errors:
        cursor.execute(
            """CREATE TABLE scrapping_orders (
                OrderID VARCHAR(20),
                estatusOrder INTEGER,
                dateOrder DATE,
                typeLivingPlace VARCHAR(40),
                whatLookingFor VARCHAR(40),
                transactionType VARCHAR(50),
                minResults INTEGER,
                observations VARCHAR(200));"""
        )
    
    if "table urls exists" not in errors:
        cursor.execute(
            """CREATE TABLE scrapping_urls (
                OrderID VARCHAR(20),
                urlItem VARCHAR(300),
                statusUrl VARCHAR(20)
            );"""
        )

    if "table data offers exists" not in errors:
        cursor.execute(
            """CREATE TABLE data_offers(
                Ordenid VARCHAR(50),
                urlitem VARCHAR(300),
                total_area VARCHAR(30),
                const_area VARCHAR(30),
                rooms VARCHAR(30),
                bath_room VARCHAR(30),
                clima VARCHAR(30),
                sector VARCHAR(30),
                precio VARCHAR(30)
            );"""
        )

#-----------------------------------------------------------
                #Orders Methods

def insertOrder(orderid,typeliving,whatlooking,transaction,minresult):
    """This function is used for insert orders from web
    """

    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )
  
    #Cursor
    cursor=connection.cursor()

    sqlstring="INSERT INTO scrapping_orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    values=(orderid,0,datetime.datetime.now(),typeliving,whatlooking,transaction,minresult,"no observation")

    #Inserting values
    cursor.execute(sqlstring,values)
    connection.commit()


def gettingOrders():
    """ This function is used for getting all scarpping orders regitered in the database by the GUI.
    This oders will activate the scrapper for getting the information from the web page
    """

    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )
  
    #Creating Cursor for retreive information
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM scrapping_orders WHERE estatusOrder=0;")
    resultados=cursor.fetchone()

    if resultados!= None:
        return {
            "OrderID":resultados[0],
            "estatusOrder":resultados[1],
            "dateOrder":resultados[2],
            "typeLivingPlace":resultados[3],
            "whatLookingFor":resultados[4],
            "transactionType":resultados[5],
            "minResults":resultados[6],
            "observations":resultados[7]
        }
    else:
        return []

def inserturl(orderid,url):
    """This function is used for insert urls in the table scrapping_urls. These urls will be used for sleve scrapper.
    """
    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )

    #Cursor
    cursor=connection.cursor()

    sqlstring="INSERT INTO scrapping_urls VALUES (%s,%s,%s)"
    values=(orderid,url,"not completed")

    #Inserting values
    cursor.execute(sqlstring,values)
    connection.commit()

def gettingurls_order(orderid):
    """ This function is used for getting the numbers of urls inserted for a order.
    """

    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )

    #Cursor
    cursor=connection.cursor()

    #Getting Values
    cursor.execute("SELECT urlItem FROM scrapping_urls WHERE OrderID='"+orderid+"';")
    resultados=cursor.fetchall()
    resultados=[url[0] for url in resultados]

    return resultados

def updating_orderstatus(orderid):
    """This function is used for updating status of the order once the urls are scrapped
    """

    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )

    #Cursor
    cursor=connection.cursor()

    #Getting Values
    cursor.execute("UPDATE scrapping_orders SET estatusOrder=1 WHERE OrderID='"+orderid+"';")
    connection.commit()

#-----------------------------------------------------------
                #URLs Methods
def gettingUrls():
    """This function is used for getting all urls not completed from de database.
    """
    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )
  
    #Creating Cursor for retreive information
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM scrapping_urls WHERE statusUrl='not completed';")
    resultados=cursor.fetchall()
    return resultados

def updating_urlstatus(orderid,url):
    """This function is used for updating status of the url.
    """

    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )

    #Cursor
    cursor=connection.cursor()

    #Getting Values
    cursor.execute("UPDATE scrapping_urls SET statusUrl='Completed' WHERE OrderID='"+orderid+"'  AND urlitem='"+url+"';")
    connection.commit()

def insertdataoffer(orderid,url,data_dict):
    """This function is used for inserting final data to database
    """
    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )

    #Cursor
    cursor=connection.cursor()

    sqlstring="INSERT INTO data_offers VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=(orderid,url,data_dict["Área privada"],data_dict["Área Const"],data_dict["Hab"],data_dict["Baños"],data_dict["Clima"],data_dict["Sector"],data_dict["Precio"])

    #Inserting values
    cursor.execute(sqlstring,values)
    connection.commit()
#-----------------------------------------------------------
                #ERRORES
def insertarError(itemrelated,error):
    """This function is used for inserting final data to database
    """
    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )

    #Cursor
    cursor=connection.cursor()

    sqlstring="INSERT INTO errors_process VALUES (%s,%s)"
    values=(itemrelated,error)

    #Inserting values
    cursor.execute(sqlstring,values)
    connection.commit()

#-----------------------------------------------------------
                #Function of the servers
def gettingAllData():
    """This function is used for getting all urls not completed from de database.
    """
    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )
  
    #Creating Cursor for retreive information
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM data_offers")
    resultados=cursor.fetchall()
    return resultados

def gettingDataOrderid(orderID):
    """This function is used for getting all urls not completed from de database.
    """
    #Connect to the database
    connection = mysql.connector.connect(
        host=settings["ip"],
        user=settings["user"],
        passwd=settings["password"],
        database=settings["database_name"]
    )
  
    #Creating Cursor for retreive information
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM data_offers WHERE Ordenid='"+orderID+"';")
    resultados=cursor.fetchall()

    if len(resultados)>1:
        return resultados
    else:
        return None