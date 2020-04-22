import time,os,requests,sys,csv,subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#Import importants functions support files
from db import gettingOrders,inserturl,gettingurls_order,updating_orderstatus,initialverifications,insertarError

#Options
options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  #gpu windows only
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

#Init Chrome Driver
navegador=webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe",chrome_options=options)
navegador=webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe")
navegador.maximize_window()


#Init Scrapper_sleve
subprocess.call(" python scrapper_sleve.py 1",shell=True)

#----------------------------------------------------------------------------------------------------------
                                        #Function Support
def waitByID(ElementID,time_wait,navegador=navegador):
    """ This Function is used to wait a element with an ID=ElementID. 
        It will wait for the element during the time=time_wait
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.ID,ElementID))
                )
                return navegador.find_element_by_id(ElementID)
            except:
                print("The element with ID:  "+ElementID+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

def waitByXpath(ElementXpath,time_wait,navegador=navegador):
    """ This Function is used to wait a element with an Xpath=ElementXpath.
        It will wait for the element during the time=time_wait.
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.XPATH,ElementXpath))
                )
                return navegador.find_element_by_xpath(ElementXpath)
            except:
                print("The element with Xpath:  "+ElementXpath+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

def waitElementsBycssSelector(cssSelector,time_wait,navegador=navegador):
    """ This Function is used to wait for elements with a cssSelector=cssSelector.
        It will wait for the elements during the time=time_wait.
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,cssSelector))
                )
                return navegador.find_elements_by_css_selector(cssSelector)
            except:
                print("The elements with cssSelector:  "+cssSelector+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

def waitElementsByTagName(tagName,time_wait,navegador=navegador):
    """ This Function is used to wait for elements with a html tag=tagName
        It will wait for the elements during the time=time_wait.
    """
    while True:
        try:
            try:
                WebDriverWait(navegador,time_wait).until(
                    EC.presence_of_element_located((By.TAG_NAME,tagName))
                )
                return navegador.find_elements_by_tag_name(tagName)
            except:
                print("Elements with tag: "+tagName+" does not appeared within "+str(time_wait))
                return "Element not found"
        except:
            print("Waiting for element...")

#Bucle of the global process
while True:
    try:
    
        #Verification in Database
        initialverifications()
        print("Data Base starts!")
        
        #----------------------------------------------------------------------------------------------------------
        #Initiate the navigator
        #Go tu url
        navegador.get("https://www.fincaraiz.com.co/")

        #----------------------------------------------------------------------------------------------------------
                                                #Getting Scrapping Orders
        orders=gettingOrders()

        #If there are not ordres, will sleep for a hour and then will retreive for new orders in the database
        if len(orders)<=0:
            time.sleep(360)
            continue
        
        #Getting all urls already in db
        urls_db=gettingurls_order(orders["OrderID"])
        #----------------------------------------------------------------------------------------------------------
                                                #Parameters
        typelivingplace=orders["typeLivingPlace"]
        whatlookingfor=orders["whatLookingFor"]
        typetransaction=orders["transactionType"]

        parameters_id={
            "Proyectos Nuevos":"ProyectoNuevo",
            "Vivienda":"linkVivienda",
            "Comerciales":"linkInmueblesComerciales"
        }
        #----------------------------------------------------------------------------------------------------------
                                                #Setting Filters
        #Wating for btn search availability
        btn_search=waitByID("btnSearchAdvert",30)

        #1- Type of living 
        btn_typeliving=waitByID(parameters_id[typelivingplace],20).click()

        #2- What are you lookingfor
        container_categories=waitByID("divContainerCategories",20)
        container_categories.click()
        categories=waitByID("ddlCategories"+typelivingplace,20,container_categories)
        labelselements=waitElementsByTagName("li",20,categories)
        for label in labelselements:
            #print(label.text)
            if whatlookingfor in label.text:
                label.click()
                break
        del(labelselements,container_categories,categories)

        #3- Type of transanction: Selling or rent
        container_transactions=waitByID("divContainerTransaction",20)
        container_transactions.click()
        time.sleep(1)
        container_transactions.click()
        transactions=waitByID("ddlTransactionType",20,container_transactions)
        labelselements=waitElementsByTagName("li",20,transactions)
        for label in labelselements:
            #print(label.text)
            if typetransaction in label.text:
                label.click()
                break
        del(labelselements,container_transactions,transactions)

        #Click Search
        btn_search.click()
        #-------------------------------------------------------------------------------------
        urls=[]
        globalactions=[]
        #-------------------------------------------------------------------------------------
        #Bucle of the sub-process of getting urls
        while True:
            startagain=False #This variable reflects the run for a page
            nextpage=0

            #--------------------------------------------------------
                                #GLOBAL EVALUATIONS
            #Evaluationg global actions
            if "nextorder" in globalactions:
                break
            #--------------------------------------------------------
            #Wait for page load
            principal_container=waitByID("divAdverts",10)

            #Getting all advertisements
            advertisements=waitElementsByTagName("ul",10,principal_container)

            #Iterating Advertisements
            counter=0
            for add in advertisements:
                #-------------------------------------------------------
                                #STOP PROCESS EVALUATION
                """ In this section will be evaluated if the order meet with minimal numbers of urls
                """
                if counter>5:
                    urls_db=gettingurls_order(orders["OrderID"])
                    if len(urls_db)>=orders["minResults"]:
                        globalactions.append("nextorder")
                        updating_orderstatus(orders["OrderID"])
                        break
                    else:
                        counter=0
                else:
                    counter+=1
                #-------------------------------------------------------
                #Getting link of the advertisements
                links=waitElementsByTagName("a",20,add)

                #Control flow: if elements is not found, will continue with the next
                if links=="Element not found":
                    continue

                #Getting links for each advertisements and insert to database
                for a in links:
                    url=a.get_attribute("href")
                    if ("https://www.fincaraiz.com.co" in url) and (url not in urls_db):
                        inserturl(orders["OrderID"],url)
                        urls.append(url)
                    else:
                        if nextpage>5:
                            break
                        nextpage+=1
                
                #Verify if there are not more adds
                if nextpage>5:

                    #Go next page
                    link_buttons=waitElementsByTagName("a",20)
                    for button in link_buttons:
                        if "Ir a la pagina Siguiente" in button.get_attribute("title"):
                            button.click()
                            startagain=True
                            break
                if startagain:
                    break
    except Exception as e:
        #Saving Error
        insertarError("Error in the General loop in Scrapper",str(e))

        #Delete and destroy navagador
        navegador.close()
        del(navegador)
        time.sleep(10)

        #Create new navegador
        navegador=webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe",chrome_options=options)