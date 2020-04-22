import datetime
from flask import Flask,render_template,request
app=Flask(__name__)

from db import insertOrder,gettingAllData,gettingDataOrderid


#Rutas
@app.route('/')
def inicio():
    datos=gettingAllData()
    return render_template("index.html",datos=datos)

@app.route('/saveorder',methods=['POST'])
def saveOrder():
    now=datetime.datetime.now().strftime("%Y%m%d%f")
    typeliving=request.form["typeliving"]
    lookingfor=request.form["lookingfor"]
    transaction=request.form["Transanction"]
    minresult=int(request.form["minresult"])

    #Limit the orders
    if minresult>50:
        minresult=50

    insertOrder(now,typeliving,lookingfor,transaction,minresult)
    print("Correcto!!")
    return render_template("index.html",orderid=now)

@app.route('/getorder',methods=['POST'])
def getorder():
    orderid=request.form["orderid"]
    datos=gettingDataOrderid(orderid)
    return render_template("index.html",datos=datos)