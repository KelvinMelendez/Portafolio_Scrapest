# **SCRAPPER_FINCARAIZ**

*Scrapper_Fincaraiz* is a web scrapper for the web page https://www.fincaraiz.com.co/. This webpage publishes livingplaces for sell.

# DESCRIPTION

*Scrapper_Fincaraiz* can help you to scrapp information from https://www.fincaraiz.com.co/ specifying some filters or parameters for a better fitting of the results. 

# **OBJECTIVES**

1. Get information of living place from Argentina
2. Develope a Tool (GUI) where it can be created orders of scrappings with specifics parameters
3. Create awareness of what can be done with the used tecniques during this project

# **CONSIDERATIONS**

All posible feactures were not implemented in order to protect integration of the information for the webpage.

# **INTRODUCTION OF THE PROCESS**

We can divide this projects into three entities:

1. Server: This  is the entity that ser the GUI for end users. The server was code using python (FLASK)
2. Scraper: This is entity contains all the code/script needed for getting the information from the webpage
3. scrapper_sleve: This is a second code/script needed for getting the information from the webpage. This works as a auxiliary worker.

# **DEVELOPMENT OF ENTITIES**

### **Server**

The server was coded using the library python named FLASK. FLASK is really good for small applications where you want to deploy fast. This entity serve the GUI template to be used by the end users. Here the user can define search criteria by creating a order scrap. This order travels to the database to be taken by the **Scrapper**

### **Scrapper**

This is the main Script during the scrapping process. In this script we apply filters and criteria defined by the user in the GUI to the webpage https://www.fincaraiz.com.co/. Then it will iterate thru all adds published in the web scrapping the information defined in the script.

### **Scrapper_sleeve**
This is an auxilary worker that helps **Scrapper** to performed better. This is responsable to send final information to the database to be used for enduser.

# **INSTALATION**

First, install python libraries bellow:

```bash
pip install flask
pip install requests
pip install BeautifulSoup
pip install selenium
pip install mysql-connector
```

In order deploy the entire ecosystem. Make the following steps:

1. Clone de repository
2. Enter to the clonned repository folder
3. Modify the file *db_settings.json* with the credentials of the database you want to use
4. Run the *scrapper_sleve.py* script by using the command in cmd: **python scrapper_sleve.py**
5. Run the *Scrapper.py* script by using the commandin cmd: **python Scrapper.py**
6. Start the Server by run following commands (WINDOWS ONLY)
    ```bash
    set FLASK_APP=server.py
    python -m flask run --host=0.0.0.0 -p 80
    ```
7. Start the Server by run following commands (LINUX ONLY):
    ```bash
    export FLASK_APP=server.py
    flask run --host=0.0.0.0 -p 80
    ```

Once previous steps are done, you can get the GUI by going to your navigator and go to url: http://localhost:5000


# **USAGE**

Once everything is installed and working on, you can do several things  thru the GUI

1. Create a Order Scrapping: Here create a order with specific filters and parameters to be used by the *Scrapper* for getting the information in the web
2. All information are saved in the database, if you want to retreive the total information no matter the order, the GUI has a data table where you can do that
3. You can retreive information for a specific order.

# SUPPORT

In case of any question, please contact me on kmelendezdipre@outlook.com