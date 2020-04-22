# DESCRIPTION

#**OBJECTIVES**

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

### ** Scrapper_sleve**
This is an auxilary worker that helps **Scrapper** to performed better. This is responsable to send final information to the database to be used for enduser.

# **USAGE**
