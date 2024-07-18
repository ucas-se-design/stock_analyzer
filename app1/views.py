import http
from this import d
from wsgiref.util import request_uri
from django.shortcuts import render,HttpResponse
import openpyxl
import socket
import json
# Create your views here.
import tkinter
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import pymysql
#导入ADO接口模块
from tkinter import messagebox
from tkinter.messagebox import *

# 配置数据库连接参数
config = {
    'user': 'root',
    'password': '123456',
    'host': '127.0.0.1',
    'database': 'stock_forecast',
    # 'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

def exps(request):
    return render(request,'explain.html')

def more1(request):
    return render(request,'tables-responsive1.html')

def more2(request):
    return render(request,'tables-responsive2.html')

def more3(request):
    return render(request,'tables-responsive3.html')

def service_agreement(request):
    return render(request, 'service_agreement.html')
def home_page(request):
    return render(request,'home_page.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def message(request):
    return render(request,'message.html')

def forget_password(request):
    return render(request,'forget_password.html')

def start_login(request):
    web_message = request.GET
    username = web_message.get('username')
    password = web_message.get('password')

    try:
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            query_sql = "SELECT * FROM user;"
            cursor.execute(query_sql)
            result = cursor.fetchall()
            for dict_item in result:
                if dict_item['username'] != username:
                    continue
                else:
                    if dict_item['password'] != password:
                        return render(request,'password_error.html')
                    else:
                        return index1(request)
            return render(request,'user_not_exist.html')

    except pymysql.Error as e:
        return render(request,'mysql_error.html')
    finally:
        if 'connection' in locals():
            connection.close()

def start_register(request):
    web_message = request.GET
    username = web_message.get('username')
    password1 = web_message.get('password1')
    password2 = web_message.get('password2')
    email = web_message.get('email')
    if len(username) >= 10:
        return render(request, 'username_is_too_long.html')
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email) is None:  # 如果不是标准的邮箱格式
        return render(request, 'please_input_right_email.html')
    if password1 == password2:
        pattern = r'^[A-Za-z0-9_\W]*$'
        if re.match(pattern, password1) is None:  # 如果密码格式不合法
            return render(request, 'password_is_illegal.html')
        if len(password1) < 6:
            return render(request, 'password_is_too_short.html')
        if len(password1) > 16:
            return render(request, 'password_is_too_long.html')
    else:
        return render(request, 'password_is_not_same.html')
    connection = pymysql.connect(**config)
    with connection.cursor() as cursor:
        query_sql = "INSERT INTO user(`username`, `password`, `email`) VALUES('" + username + "', '" + password1 + "', '" + email + "');"
        print(query_sql)
        try:
            cursor.execute(query_sql)
            connection.commit()
            connection.close()
        except:
            return render(request, 'username_is_repeated.html')
    return render(request, 'register_is_succeed.html')

    
def recover(request):
    web_message = request.GET
    username = web_message.get('username')
    email = web_message.get('email')
    password = web_message.get('password')
    try:
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            query_sql = "SELECT * FROM user;"
            cursor.execute(query_sql)
            result = cursor.fetchall()
            for dict_item in result:
                if dict_item['username'] != username:
                    continue
                else:
                    if dict_item['email'] != email:
                        return render(request, 'email_is_not_right.html')
                    else:
                        query_sql = "UPDATE user SET `password` = '" + password + "' WHERE (`username` = '" + username + "');"
                        print(query_sql)
                        cursor.execute(query_sql)
                        connection.commit()
                        connection.close()
                        return render(request, 'password_is_changed.html')
            return render(request, 'register_user_not_exist.html')

    except pymysql.Error as e:
        print(e)
        return render(request, 'mysql_error.html')

def get_result():
    serverName = '127.0.0.1'
    serverPort = 2580
    BUFSIZ = 2048
    ADDR = (serverName, serverPort)
    
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(ADDR)
    clientSocket.send("J-S-P_ I am Client".encode('utf-8'))
    returnData = clientSocket.recv(BUFSIZ)
    print('from Server information:%s' % returnData.decode('utf-8'))
    clientSocket.close()
    print("结束")
    return returnData.decode('utf-8')

def main_page(request):
    # 打开js文件，准备对配置项进行修改
    kline_data = []
    
    with open('static\\js\\test.js', "w") as f:
        date = ""
        op = 0
        cp = 0
        hp = 0
        lp = 0
        vol = 0
        sign = 1
        
        wb = openpyxl.load_workbook('D:\\图像数据.xlsx')
        sheet = wb.worksheets[0]
        judgefirstrow = True
        dataitem = []
        for row in sheet.iter_rows():
            if(judgefirstrow == False):
                dataitem = []
                count = 0
                for item in row:
                    count += 1
                    if(count == 1):
                        date = str(item.value)
                    elif(count == 2):
                        op = item.value
                    elif(count == 3):
                        cp = item.value
                    elif(count == 4):
                        hp = item.value
                    elif(count == 5):
                        lp = item.value
                    elif(count == 6):
                        vol = item.value
                        break
                if(op >= cp):
                    sign = 1
                else:
                    sign = -1
                dataitem.append(date)
                dataitem.append(op)
                dataitem.append(hp)
                dataitem.append(lp)
                dataitem.append(cp)
                dataitem.append(vol)
                dataitem.append(sign)
                kline_data.append(dataitem)
            else:
                judgefirstrow = False

        f.writelines("var reset = kline.getOption().dataZoom;\n")
        f.writelines("reset = {\n")
        f.writelines("dataset :{\n")
        f.writelines("source:  ")
        f.writelines(str(kline_data))
        f.writelines('}}\n')
        f.writelines("kline.setOption(reset);")
    
    with open('static\\js\\result.js', "w") as result_file:
        data = get_result()
        result = ''
        for i in data:
            result += i
        result_file.writelines("data_to_show = " + result) 
        
    return render(request,'main_page.html')
    
def main_page1(request):
    return render(request,'main_page.html')
    
def index1(request):
    stockCode = "000004"
    nameList = ['MACD', 'RSI', 'KDJ', 'BOLL', 'DMA', 'BRAR', 'CCI', 'OBV', 'PSY', 'VR']
    dataList = {}
    filename = 'static/json/' + stockCode + '_date.json'
    with open(filename) as file_obj:
        dateList = json.load(file_obj)
    for name in nameList:
        filename = 'static/json/' + stockCode + '_' + name + '.json'
        # print(filename)
        with open(filename) as file_obj:
            # print('Yes')
            dataList[name] = json.load(file_obj)
    return render(request, 'index1.html',
                  {
                      'stockCode': json.dumps(stockCode),
                      'dateList': json.dumps(dateList),
                      'dataList': json.dumps(dataList),
                  })

def index2(request):
    stockCode = "000005"
    nameList = ['MACD', 'RSI', 'KDJ', 'BOLL', 'DMA', 'BRAR', 'CCI', 'OBV', 'PSY', 'VR']
    dataList = {}
    filename = 'static/json/' + stockCode + '_date.json'
    with open(filename) as file_obj:
        dateList = json.load(file_obj)
    for name in nameList:
        filename = 'static/json/' + stockCode + '_' + name + '.json'
        with open(filename) as file_obj:
            dataList[name] = json.load(file_obj)
    return render(request, 'index2.html',
                  {
                      'stockCode': json.dumps(stockCode),
                      'dateList': json.dumps(dateList),
                      'dataList': json.dumps(dataList),
                  })

def index3(request):
    stockCode = "000006"
    nameList = ['MACD', 'RSI', 'KDJ', 'BOLL', 'DMA', 'BRAR', 'CCI', 'OBV', 'PSY', 'VR']
    dataList = {}
    filename = 'static/json/' + stockCode + '_date.json'
    with open(filename) as file_obj:
        dateList = json.load(file_obj)
    for name in nameList:
        filename = 'static/json/' + stockCode + '_' + name + '.json'
        with open(filename) as file_obj:
            dataList[name] = json.load(file_obj)
    return render(request, 'index3.html',
                  {
                      'stockCode': json.dumps(stockCode),
                      'dateList': json.dumps(dateList),
                      'dataList': json.dumps(dataList),
                  })