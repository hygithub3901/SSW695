from math import remainder
from unittest import result
from flask import Flask,make_response,json,render_template,request,redirect,url_for
import json
import csv

from datetime import datetime

import get_food_nutrient

import flask_db_operate

# with open('back_end/apikey.txt', mode='r') as api:
#     API_KEY = api.read()
API_KEY = 'aa'
todaytime = '2022-4-1'


app = Flask(__name__)

@app.route('/input_food',methods=['GET','POST'])
def input_food():
    reader=list()
    with open('back_end\\USER_INFO\\USER_FOOD_LOGS.CSV', mode='r') as inp:
        readers = csv.reader(inp) 
        reader=[row for row in readers]


    meal_id=food_id=str(len(reader))
    user_name='GW'
    date='2022-03-24'
    food_name=request.form.get('food_name')
    Type=request.form.get('Type')
    weight=request.form.get('weight')
    calorie_rate=request.form.get('calorie_rate')
    carbohydrate=request.form.get('carbohydrate')
    protein=request.form.get('protein')
    fat=request.form.get('fat')

    try:
        calorie_cost=float(calorie_rate)*float(weight)/100
        calorie_cost=str(calorie_cost)
        reader.append([meal_id,food_id,food_name,user_name,date,Type,weight,calorie_rate,carbohydrate,protein,fat,calorie_cost])
        
        with open('back_end\\USER_INFO\\USER_FOOD_LOGS.CSV', 'w') as f:
            s=''
            for key in reader:
                s+=(",".join(key)+'\n')
            f.write(s)
        return redirect('/today/'+ "GW")
    except:
        calorie_cost=0
    return render_template('input_food.html')


@app.route('/yoursituation/<username>', methods =['GET','POST'])
def getinfo(username):
    userId = username
    userName = request.form.get('Name')
    gender = request.form.get('gender')
    height = request.form.get('height')
    weight = request.form.get('weight')
    age = request.form.get('age')
    fatRate = request.form.get('fatRate')
    BMR = request.form.get('BMR')
    infoDate = datetime.now()
    submit = request.form.get('Submit')
    userInfoDict = {
        'userId':userId,
        'userName':userName,
        'gender':gender,
        'height':height,
        'weight':weight,
        'age':age,
        'fatRate':fatRate,
        'BMR':BMR,
        'infoDate':infoDate
    }
    if submit == 'Submit':
        canRecord = flask_db_operate.insertUserInfo(userInfoDict)
        if canRecord:
            return redirect('/home/'+username)
    return render_template('user_info.html')



@app.route('/register',methods=['GET','POST'])
def register():
    
    login=request.form.get('login')
    if login=="login":
         return redirect('/login')
    username=request.form.get('username')
    password=request.form.get('password')
    register=request.form.get('Register')

    userInfo = {
        'userId': username,
        'userPassword': password,
    }
    if(register == 'Register'):
        canreg = flask_db_operate.insertLogin(userInfo)
        if canreg:
            return redirect('/yoursituation/' + username)
    return render_template('register.html',result=False)

@app.route('/')
def inddex():
    return redirect('/login')

# @app.route('/login',methods=['GET','POST'])
@app.route('/verifyLogin', methods = ['GET','POST'])
def login():
    # username=request.form.get('username')
    # password=request.form.get('password')
    # Login = request.form.get('Login')
    # Register=request.form.get('Register')
    data = json.loads(request.get_data()) 
    userInfo = {
        'userId': data['username'],
        'userPassword': data['password'],
    }
    cannotlogin = flask_db_operate.findIfInTable('login', 'userId', userInfo['userId'])

    res_json = {
        "isSuccess": cannotlogin,
    }
    # if Login == 'Login':
    #     if(cannotlogin):
    #         return redirect('/home/'+username)
    # if Register=="Register":
    #     return redirect('/register')
    # return render_template('login.html',result=False)
    return res_json
    

@app.route('/home/<username>',methods=['GET','POST'])
def homepage(username):
    username = username
    userinfo = request.form.get('Check')
    today = request.form.get('today')
    if userinfo == 'Check':
        return redirect('/user_info/'+ username)
    search = request.form.get('Search')
    if search == 'Search':
        return redirect('/searchFood')
    
    if today == 'today':
        return redirect('/today/'+username)
    
    userinfo = flask_db_operate.findInTable('userInfo_logs', 'userId', username)
    # if len(userinfo) == 1:
    userinfores = userinfo[0]
    print(userinfores)
    total = 2300
    
    mealres = flask_db_operate.findInTable('mealRecord', 'mealDate', todaytime)
    totalenergy = 0.0
    for i in mealres:
        canfind = flask_db_operate.findIfInTable('foodInfo', 'foodName', i[3])
        if canfind:
            foodenergy = flask_db_operate.findInTable('foodInfo', 'foodName', i[3])
            totalenergy = totalenergy + foodenergy[0][6]
        else:
            ans = get_food_nutrient.call_API(i[3], API_KEY)
            foodenergy = get_food_nutrient.obtain_energy(ans['foods'][0]['foodNutrients'])
            totalenergy += foodenergy
    
    remaind = total - totalenergy

    if remaind>=0:
        advice="You can still enjoy foods today"
    else:
        advice="You ate too much today, need to do exercise."
    return render_template('homepage.html', total = total, remaind = remaind, advice = advice)

@app.route('/today/<username>',methods=['GET','POST'])
def userfoodInfo(username):
    userId = username
    mealDate = request.form.get('mealDate')
    # mealDate = datetime.now()
    mealType = request.form.get('mealType')
    foodName = request.form.get('foodName')
    res_data = flask_db_operate.findInTable('mealRecord', 'mealDate', todaytime)

    mealData = {
        'userId':userId,
        'mealDate':mealDate,
        'mealType':mealType,
        'foodName':foodName,
    }
    
    Inputinfo = request.form.get('Inputinfo')
    if Inputinfo == 'Inputinfo':
        caninput = flask_db_operate.insertMealRecord(mealData)
        if caninput:
            return redirect('/today/' + userId)
    
    ReturnHome = request.form.get('Home')
    if ReturnHome == 'Home':
        return redirect('/home/' + userId)

    return render_template('today.html', rows = res_data)

@app.route('/user_info/<username>',methods=['GET','POST'])
def userInfo(username):
    userId = username
    info_res = flask_db_operate.findInTable('userInfo_logs', 'userId', userId)
    userinfo_dict = {
        'userId': username,
        'infomation': info_res,
    }
    return userinfo_dict

@app.route('/searchFood',methods=['GET','POST'])
def searchFood():
    Input= request.form.get('Input')
    foodName = request.form.get('foodname')
    search = request.form.get('Search')
    if Input == 'Input':
        return redirect('/input_food')
    if search == 'Search':
        return redirect('/foodNutrient/' + foodName)
    return render_template('search_food.html')


@app.route('/foodNutrient/<foodname>')
def foodNutrient(foodname):
    ans = get_food_nutrient.call_API(foodname, API_KEY)

    data = list()

    for i in range(len(ans['foods'])):
        fdcId = ans['foods'][i]['fdcId']
        foodCategory = ans['foods'][i]['foodCategory']
        foodDetailInfo = ans['foods'][i]['foodNutrients']
        fooddata = get_food_nutrient.format_food(fdcId, foodname, foodCategory, foodDetailInfo)
        data.append(fooddata)
        # break after 10 result
        if i >= 10:
            break
    
    # insert first one
    insert = flask_db_operate.insertFood(data[0])
    if insert:
        print("insert successful")
    else:
        print("insert fail")
    return make_response(data[0])


if __name__ == '__main__':
    app.run()