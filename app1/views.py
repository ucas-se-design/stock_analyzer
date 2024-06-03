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
    'password': '001015wq.',
    'host': '127.0.0.1',
    'database': 'user_and_password',
    'charset': 'utf8mb4',
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

def home_page(request):
    return render(request,'initial.html')

def login(request):
    return render(request,'pages-login.html')

def register(request):
    return render(request,'pages-register.html')

def message(request):
    return render(request,'message.html')

def recoverpw(request):
    return render(request,'pages-recoverpw.html')

def start_login(request):
    web_message = request.GET
    temp_username = web_message.get('username')
    temp_password = web_message.get('password')

    try:
        connection = pymysql.connect(**config)
        print("Successfully connected to MySQL!")
        with connection.cursor() as cursor:
            # 创建命令
            query_sql = "SELECT * FROM users;"
            # 执行命令
            cursor.execute(query_sql)
            # 获得命令结果
            result = cursor.fetchall()
            # result是一个字典列表，每个元素是一个字典，键为列名，值为元素
            for dict_item in result:
                if dict_item['username'] != temp_username:
                    continue
                else:
                    if dict_item['password'] != temp_password:
                        return render(request,'pwerror.html')
                    else:
                        print("Successfully login!")
                        return index1(request)
            return render(request,'user_not_exist.html')

    except pymysql.Error as e:
        print(f"Error:{e}")
        ############
        #需要写一个页面mysql_error.html来表示连接数据库失败或其他错误
        ############
        return render(request,'mysql_error.html')
    finally:
        if 'connection' in locals():
            connection.close()

def start_register(request):
    web_message = request.GET
    temp_username = web_message.get('username')
    temp_password1 = web_message.get('password1')
    temp_password2 = web_message.get('password2')
    temp_email = web_message.get('email')
    '''
    一些已经做好的页面
        |——'username_is_too_long.html'
        |——'password_is_too_short.html'
        |——'password_is_too_long.html'
        |——'please_input_right_email.html'
        |——'password_is_not_same.html'
        |——'username_is_repeated.html'
        |——'register_is_succeed.html'
    '''
    #################
    #根据用户输入的用户名、密码、重复密码和邮箱来注册用户
    #仿照start_login函数，使用上述页面实现用户注册业务
    #################
    return

    
def recover(request):
    web_message = request.GET
    temp_username = web_message.get('username')
    temp_email = web_message.get('email')
    temp_password = web_message.get('password')
    '''
    一些做好的页面：
        |——'register_user_not_exist.html'
        |——'email_is_not_right.html'
        |——'password_is_changed.html'
    '''
    #################
    #根据用户输入的用户名、邮箱和密码来修改用户修改密码
    #仿照start_login函数，使用上述页面实现用户修改密码业务
    #################
    
    pass

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
    #打开js文件，准备对配置项进行修改
    kline_data = []
    
    with open('C:\\Users\\sun\\Desktop\\testmd\\my_site\\static\\js\\test.js',"w") as f:
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
    
    with open('C:\\Users\\sun\\Desktop\\testmd\\my_site\\static\\js\\result.js',"w") as result_file:
        data = get_result()
        result = ''
        for i in data:
            result += i
        result_file.writelines("data_to_show = " + result) 
        
    return main_page1(request)
    
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
        with open(filename) as file_obj:
            dataList[name] = json.load(file_obj)
    return render(request, 'index1.html',
                  {
                      'stockCode': json.dumps(stockCode),
                      'dateList': json.dumps(dateList),
                      'dataList': json.dumps(dataList),
                  })
   # return render(request,'index1.html')

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

