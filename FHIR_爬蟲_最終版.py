#!/usr/bin/env python
# coding: utf-8

# In[22]:


get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install requests')
get_ipython().system('pip install selenium')

get_ipython().system('pip install pyodbc')


# In[112]:


"""## **爬所有種類**"""

from selenium import webdriver
from bs4 import BeautifulSoup,NavigableString,Tag
import requests
import pyodbc

res=requests.get("https://fhir-ru.github.io/resourcelist.html")
soup=BeautifulSoup(res.text)

temp_links=[]
sult_links=[]

for k in soup.find('div',{'id':'tabs'}).find_all('a'):
    try:
        temp_links.append("https://fhir-ru.github.io/" +  k['href'])
    except:
        print("")

for x in temp_links:                  #部分含#的連結非Resource,排除
    if "#" not in x:
        sult_links.append(x)
        sult_links2=sult_links[0:146]



# sult_links2 = ['https://fhir-ru.github.io/patient.html', 'https://fhir-ru.github.io/observation.html', 'https://fhir-ru.github.io/encounter.html', 'https://fhir-ru.github.io/procedure.html', 'https://fhir-ru.github.io/medicationrequest.html', 'https://fhir-ru.github.io/composition.html', 'https://fhir-ru.github.io/condition.html']
print(sult_links2)
print(len(sult_links2))


# In[ ]:


"""## **爬版本是否穩定**"""

i=-1
for abc in sult_links2:
    i=i+1
    if i>146: #共145個 Resource表格(>146全爬)
        break
    else:
        res=requests.get(sult_links2[i])
        soup=BeautifulSoup(res.text)
#------------------------------------------Resource_Title------------------------------------------------------#
        title_list=[]
        for g in soup.find('h1',{'class':'self-link-parent'}):
            title_list.append(g)
        str_title=str(title_list[1])
        re_str_title=str_title.replace(" Resource ","").replace(" - Content ","")
        print(re_str_title)
#----------------------------------------------Status----------------------------------------------------------#
        redtable_list=[]
        redtable_list2=[]
        if soup.find('table',{'class':'colsn'}):
            for h in soup.find('table',{'class':'colsn'}):
                redtable_list.append(h.text)
                for td in h.find_all('td'):
                    redtable_list2.append(td.text)
        if soup.find('table',{'class':'colstu'}):
            for h in soup.find('table',{'class':'colstu'}):
                redtable_list.append(h.text)
                for td in h.find_all('td'):
                    redtable_list2.append(td.text)
        if soup.find('table',{'class':'colsd'}):
            for h in soup.find('table',{'class':'colsd'}):
                redtable_list.append(h.text)
                for td in h.find_all('td'):
                    redtable_list2.append(td.text)
        redtable_list2.insert(0, re_str_title)
        print(redtable_list2)
#----------------------------------------------InsetSQL----------------------------------------------------------#

#         try:
#             conn = pyodbc.connect('Driver={SQL Server};'
#                               'Server=DESKTOP-CJJPB5V\SQLEXPRESS;'
#                               'Database=FHIR_cr;'
#                               'Trusted_Connection=yes;'
# #                               'autocommit=True'
#                              )
#             cursor=conn.cursor()

#             cursor.execute("INSERT INTO [FHIR_cr].[dbo].[Resource_Location](Resource,Work_Group,Maturity_Level,Version,Security_Category,Compartments)VALUES('"+ redtable_list2[0] + "', '"+ redtable_list2[1] + "','"+ redtable_list2[2] + "','"+ redtable_list2[3] + "','"+ redtable_list2[4] + "','"+ redtable_list2[5] + "')")
#             cursor.commit()
#         except:
#             print('warnings:', re_str_title)


# In[34]:


#總數量
print(len(sult_links))
print(len(sult_links2))


# In[88]:


#移除例外
sult_links2_remove =["https://fhir-ru.github.io/structuremap.html",
                     "https://fhir-ru.github.io/parameters.html",
                     "https://fhir-ru.github.io/task.html"]
sult_links2 = [link for link in sult_links2 if link not in sult_links2_remove]
print(len(sult_links2))


# In[89]:


"""## **內容(Structure + Turule_name)**"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import itertools
from selenium.webdriver.common.by import By
import re
import requests
import pyodbc
#----------------------------------------------Table data----------------------------------------------------------#
result_list=[]
i=-1
p_row_list2_temp = []  # 建立暫存清單

for abc in sult_links2:
    i=i+1
    if i>146: #共145個 Resource表格(>146全爬)
        break
    else:
        res=requests.get(sult_links2[i])
        soup=BeautifulSoup(res.text)
        row_list=[]
        row_list2=[]
        for k in soup.find('div',{'id':'tabs'}).find_all('tr'): #以橫為單位全找
            row_list.append(k.text)
            for td in k.find_all('td'):                         #再以縱格分割開
                row_list2.append(td.text)
    # print("Resource表格內容:",i) #第幾個 Resourlen(p_row_list2)ce表格
    p=row_list2.index(' Documentation for this format')#結尾處位置
    p_row_list2=row_list2[:p]
    # print("look",p_row_list2)
    
    #------------------------------------------split list for insert(Structure)-----------------------------------------------#
    try:
        b=[]
        num=0
        num_list=len(p_row_list2)/5
        for abc in range(0,len(p_row_list2),5):
            b.append(p_row_list2[abc:abc+5])

        for cde in p_row_list2:
            num=num+1
            if num > num_list-1:
                break
            else:
                p_row_list2=(b[num][0:5]) #抓取二維中第個[]資料的五個元素
                p_row_list2.insert(0, b[0][0])
                # p_row_list2.insert(1, b[0][0]+'.'+b[num][0])
                p_row_list2[0]=p_row_list2[0].strip()
                p_row_list2[1]=p_row_list2[1].strip()
                p_row_list2[2]=p_row_list2[2].strip()
                p_row_list2[3]=p_row_list2[3].strip()
                p_row_list2[4]=p_row_list2[4].strip()
                p_row_list2[5]=p_row_list2[5].strip().replace("'", "''")
                p_row_list2_temp.append(p_row_list2.copy())  # 將 p_row_list2 的資料存儲在暫存清單中
    #             print("0",p_row_list2)
    #-------------------------------------------p_row_list2第二欄替換(Turtle)--------------------------------------------------#
        driver = webdriver.Chrome()                                                    #開啟chrome模擬器
        driver.implicitly_wait(5)                                                      #time out
        driver.get(sult_links2[i])
        driver.find_element(By.CSS_SELECTOR, "#ui-id-5").click()   #Submit
        time.sleep(5)
        layer_list=[]
        div_element = driver.find_element(By.CSS_SELECTOR, "div#ttl")  # 定位id为"ttl"的div元素
        for layer in div_element.find_elements(By.XPATH, ".//a[@class='dict']"):  # 在该div元素下寻找链接
            text = layer.get_attribute('text')
            layer_list.append(text)
            for layer_remove in layer_list:
                if '.' not in layer_remove:
                    layer_list.remove(layer_remove)  # 去除不是tuetle的中間沒有.的元素(可以從text去看)

        n = 0
        for index, item in enumerate(layer_list):
            n += 1
            # 刪掉第一個點以前的資料(刪掉ResourceType)
            if '.' in item:
                item = item.split('.', 1)[1]
            else:
                item = item
            p_row_list2_copy = p_row_list2_temp[index].copy()  # 從暫存清單中取出對應的 p_row_list2 資料
            p_row_list2_copy[1] = item   # 更改第二欄位成turtle的
            result_list.append(p_row_list2_copy.copy())  # 將更新後的 p_row_list2_copy 加入 result_list
            print(p_row_list2_copy)
            print(n)
        
            # 在插入数据时使用参数化查询
            sql_query = "INSERT INTO resourceinfo(ResourceType, Name, Flags, Card, Type, Description) VALUES (?, ?, ?, ?, ?, ?)"
            try:
                conn = pyodbc.connect('DRIVER={MySQL ODBC 8.0 Unicode Driver};'
                                      'Server=10.40.8.35;'
                                      'Database=fhir;'
                                      'User=lab;'
                                      'Password=1qaz2wsx3EDC;')
                cursor = conn.cursor()

                # 参数化查询执行插入操作
                cursor.execute(sql_query, p_row_list2_copy)
                cursor.commit()
            except Exception as e:
                print('Error occurred:', e)
                
        p_row_list2_temp = []
        driver.quit()
        
    except Exception as e:  #如果有對不上欄位的狀況就跳出不加進資料庫並顯示錯的種類
        print("Error in", p_row_list2[0])  
        p_row_list2_temp = []
        layer_list = []
        continue

#----------------------------------------------InsetSQL----------------------------------------------------------#

        


# In[92]:


"""## **Turtle_Name對不起來的例外處理(StructureMap、Parameters、Task)**"""
sult_links3 =["https://fhir-ru.github.io/parameters.html"]#https://fhir-ru.github.io/structuremap.html,"https://fhir-ru.github.io/parameters.html","https://fhir-ru.github.io/task.html"]

i=-1
for abc in sult_links3:
    i=i+1
    if i>1: #共145個 Resource表格(>146全爬)
        break
    else:
        res=requests.get(sult_links3[i])
        soup=BeautifulSoup(res.text)
        row_list=[]
        row_list2=[]
        for k in soup.find('div',{'id':'tabs'}).find_all('tr'): #以橫為單位全找
            row_list.append(k.text)
            for td in k.find_all('td'):                         #再以縱格分割開
                row_list2.append(td.text)
    # print("Resource表格內容:",i) #第幾個 Resourlen(p_row_list2)ce表格
    p=row_list2.index(' Documentation for this format')#結尾處位置
    p_row_list2=row_list2[:p]
    # print("look",p_row_list2)
#--------------------------------------------split list for insert-----------------------------------------------------#
    b=[]
    num=0
    num_list=len(p_row_list2)/5
#     print(num_list)
    
    for abc in range(0,len(p_row_list2),5):
        b.append(p_row_list2[abc:abc+5])
    for cde in p_row_list2:
        num=num+1
        if num > num_list-1:
            break
        else:
            p_row_list2=(b[num][0:5]) #抓取二維中第個[]資料的五個元素
            p_row_list2.insert(0, b[0][0])
            p_row_list2[0]=p_row_list2[0].strip()
            p_row_list2[1]=p_row_list2[1].strip()
            p_row_list2[2]=p_row_list2[2].strip()
            p_row_list2[3]=p_row_list2[3].strip()
            p_row_list2[4]=p_row_list2[4].strip()
            p_row_list2[5]=p_row_list2[5].strip().replace("'", "''")
            print(p_row_list2)
#             print("res:",result_list)
            print(num)

#----------------------------------------------InsetSQL----------------------------------------------------------#
#         try:
#             conn = pyodbc.connect('DRIVER={MySQL ODBC 8.0 Unicode Driver};'
#                       'Server=10.40.8.35;'
#                       'Database=fhir;'  
#                       'User=lab;' 
#                       'Password=1qaz2wsx3EDC;') 
#             cursor=conn.cursor()

#             cursor.execute("INSERT INTO resourceinfo(ResourceType,Name,Flags,Card,Type,Description)VALUES('"+ p_row_list2[0] + "', '"+ p_row_list2[1] + "','"+ p_row_list2[2] + "','"+ p_row_list2[3] + "','"+ p_row_list2[4] + "','"+ p_row_list2[5] + "')")
#             cursor.commit()
#         except Exception as e:
#             print('Error occurred:', e)
#             print('warnings:', repr(p_row_list2))


# In[110]:


sult_links3 =["https://fhir-ru.github.io/task.html"]
i=-1
for abc in sult_links3:
    i=i+1
    if i>1: #共145個 Resource表格(>146全爬)
        break
    else:
        res=requests.get(sult_links3[i])
        soup=BeautifulSoup(res.text)
        row_list=[]
        row_list2=[]
        for k in soup.find('div',{'id':'tabs'}).find_all('tr'): #以橫為單位全找
            row_list.append(k.text)
            for td in k.find_all('td'):                         #再以縱格分割開
                row_list2.append(td.text)
    # print("Resource表格內容:",i) #第幾個 Resourlen(p_row_list2)ce表格
    p=row_list2.index(' Documentation for this format')#結尾處位置
    p_row_list2=row_list2[:p]
    # print("look",p_row_list2)
    
    #------------------------------------------split list for insert(Structure)-----------------------------------------------#
    try:
        b=[]
        num=0
        num_list=len(p_row_list2)/5
        for abc in range(0,len(p_row_list2),5):
            b.append(p_row_list2[abc:abc+5])

        for cde in p_row_list2:
            num=num+1
            if num > num_list-1:
                break
            else:
                p_row_list2=(b[num][0:5]) #抓取二維中第個[]資料的五個元素
                p_row_list2.insert(0, b[0][0])
                # p_row_list2.insert(1, b[0][0]+'.'+b[num][0])
                p_row_list2[0]=p_row_list2[0].strip()
                p_row_list2[1]=p_row_list2[1].strip()
                p_row_list2[2]=p_row_list2[2].strip()
                p_row_list2[3]=p_row_list2[3].strip()
                p_row_list2[4]=p_row_list2[4].strip()
                p_row_list2[5]=p_row_list2[5].strip().replace("'", "''")
                p_row_list2_temp.append(p_row_list2.copy())  # 將 p_row_list2 的資料存儲在暫存清單中
    #             print("0",p_row_list2)
    #-------------------------------------------p_row_list2第二欄替換(Turtle)--------------------------------------------------#
        driver = webdriver.Chrome()                                                    #開啟chrome模擬器
        driver.implicitly_wait(5)                                                      #time out
        driver.get(sult_links3[i])
        driver.find_element(By.CSS_SELECTOR, "#ui-id-5").click()   #Submit
        time.sleep(5)
        layer_list=[]
        div_element = driver.find_element(By.CSS_SELECTOR, "div#ttl")  # 定位id为"ttl"的div元素
        for layer in div_element.find_elements(By.XPATH, ".//a[@class='dict']"):  # 在该div元素下寻找链接
            text = layer.get_attribute('text')
            layer_list.append(text)
            for layer_remove in layer_list:
                if '.' not in layer_remove:
                    layer_list.remove(layer_remove)  # 去除不是tuetle的中間沒有.的元素(可以從text去看)

        n = 0
        for index, item in enumerate(layer_list):
            n += 1
            # 刪掉第一個點以前的資料(刪掉ResourceType)
            if '.' in item:
                item = item.split('.', 1)[1]
            else:
                item = item
            p_row_list2_copy = p_row_list2_temp[index].copy()  # 從暫存清單中取出對應的 p_row_list2 資料
            p_row_list2_copy[1] = item   # 更改第二欄位成turtle的
            result_list.append(p_row_list2_copy.copy())  # 將更新後的 p_row_list2_copy 加入 result_list
            print(p_row_list2_copy)
            print(n)
        
            # 在插入数据时使用参数化查询
            sql_query = "INSERT INTO resourceinfo(ResourceType, Name, Flags, Card, Type, Description) VALUES (?, ?, ?, ?, ?, ?)"
            try:
                conn = pyodbc.connect('DRIVER={MySQL ODBC 8.0 Unicode Driver};'
                                      'Server=10.40.8.35;'
                                      'Database=fhir;'
                                      'User=lab;'
                                      'Password=1qaz2wsx3EDC;')
                cursor = conn.cursor()

                # 参数化查询执行插入操作
                cursor.execute(sql_query, p_row_list2_copy)
                cursor.commit()
            except Exception as e:
                print('Error occurred:', e)
                
        driver.quit()
        
    except Exception as e:  #如果有對不上欄位的狀況就跳出不加進資料庫並顯示錯的種類
        print("Error in", p_row_list2[0])  
        p_row_list2_temp = []
        layer_list = []
        continue


# In[111]:


"""## **格式 (Reference要例外處理)*"""
from selenium import webdriver
from bs4 import BeautifulSoup,NavigableString,Tag
import requests
import pyodbc

id_list=['tabs-Attachment-struc','tabs-Coding-struc','tabs-CodeableConcept-struc','tabs-Quantity-struc','tabs-Money-struc','tabs-Range-struc','tabs-Ratio-struc'
         ,'tabs-Period-struc','tabs-SampledData-struc','tabs-Identifier-struc','tabs-HumanName-struc','tabs-Address-struc','tabs-ContactPoint-struc'
         ,'tabs-Timing-struc','tabs-Signature-struc','tabs-Annotation-struc']

for id in id_list:
    res=requests.get("https://hl7.org/fhir/R4/datatypes.html#code")
    soup=BeautifulSoup(res.text)
    type_list=[]
    div_element = soup.find("div", id=id)  # 定位id为"..."的div元素
    for k in div_element.find('div',{'id':'tbl-inner'}).find_all('tr'): #以橫為單位全找
        type_list2 = []  # 重置為新的空列表
        for td in k.find_all('td'):                         #再以縱格分割開
            type_list2.append(td.text.strip())
        if type_list2:  # 检查数据是否为空列表
            type_list.append(type_list2)
            
    datatype=type_list[0][0]
    if 'Documentation for this format' in type_list[-1]:
#         print(type_list[0])
        type_list = type_list[1:-1]

    for i, row in enumerate(type_list):
        type_list[i] = [datatype] + row

    for row in type_list:
        row[5] = row[5].strip().replace("'","''")
        print(row)

#--------------------------------------------split list for insert-----------------------------------------------------#
        try:
            conn = pyodbc.connect('DRIVER={MySQL ODBC 8.0 Unicode Driver};'
                      'Server=10.40.8.35;'
                      'Database=fhir;'  # 添加数据库名称
                      'User=lab;'  # 修改为您的MySQL用户名
                      'Password=1qaz2wsx3EDC;')  # 修改为您的MySQL密码
            cursor=conn.cursor()

            cursor.execute("INSERT INTO datatypes(DataType,Name,Flags,Card,Type,Description)VALUES('"+ row[0] + "', '"+ row[1] + "','"+ row[2] + "','"+ row[3] + "','"+ row[4] + "','"+ row[5] + "')")
            cursor.commit()
        except Exception as e:
            print('Error occurred:', e)
            print('warnings:', repr(row))


# In[26]:


"""## **整理Turtle_Name欄位**"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import itertools
from selenium.webdriver.common.by import By
import re

i=-1
for cde in sult_links2:
    i=i+1
    if i>1: #設定跑到哪
        break
    else:
        driver = webdriver.Chrome()                                                    #開啟chrome模擬器
        driver.implicitly_wait(5)                                                      #time out
        driver.get(sult_links2[i])
        driver.find_element(By.CSS_SELECTOR, "#ui-id-5").click()   #Submit
        time.sleep(5)
        layer_list=[]
        div_element = driver.find_element(By.CSS_SELECTOR, "div#ttl")  # 定位id为"ttl"的div元素
        for layer in div_element.find_elements(By.XPATH, ".//a[@class='dict']"):  # 在该div元素下寻找链接
            text = layer.get_attribute('text')
            layer_list.append(text)
            for layer_remove in layer_list:
                if '.' not in layer_remove:
                    layer_list.remove(layer_remove)  # 去除不是tuetle的中間沒有.的元素(可以從text去看)

        num = 0
        for item in layer_list:
            num += 1
            # 判断是否存在点，并提取点之后的部分
            if '.' in item:
                item = item.split('.', 1)[1]
            else:
                item = item
            print([item])
            print("第幾個", num)

        driver.quit()


# In[36]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import itertools

i=-1
for cde in sult_links2:
    i=i+1
    if i>1: #共145個 Resource表格(>146全爬)
        break
    else:
        driver = webdriver.Chrome()  
        driver.implicitly_wait(5)  
        driver.get(sult_links2[i])
        driver.find_element_by_css_selector("#ui-id-5").click()
        time.sleep(5)
        layer_list=[]
        for layer in driver.find_elements_by_xpath("//a[@class='dict']"):
            text = layer.get_attribute('text')
            layer_list.append(text)
            for layer_remove in layer_list:
                if '.' not in layer_remove:layer_list.remove(layer_remove)
        layer_list.insert(0,sult_links2[i].replace('http://hl7.org/fhir/','').replace('.html',''))
#         print(layer_list)
        driver.quit()
        
        layer_list_num=[]
        for layer_num in layer_list:
            stage_num=1+layer_num.count(".")
            layer_list_num.append(stage_num)
#         print(layer_list_num)
        
        layer_list_combine=list(itertools.chain.from_iterable(zip(layer_list,layer_list_num)))
#         print(layer_list_combine)
#--------------------------------------------split list for insert-----------------------------------------------------#
    b=[]
    num=-1
    num_list=len(layer_list_combine)/2
    print(num_list)
    for abc in range(0,len(layer_list_combine),2):
        b.append(layer_list_combine[abc:abc+2])
    for cde in layer_list_combine:
        num=num+1
        if num > num_list-1:
            break
        else:
            layer_list_combine=(b[num][0:2])
            print(layer_list_combine)
            print(num)
#----------------------------------------------InsetSQL----------------------------------------------------------#
#         try:
#             conn = pyodbc.connect('Driver={SQL Server};'
#                               'Server=DESKTOP-CJJPB5V\SQLEXPRESS;'
#                               'Database=FHIR_cr;'
#                               'Trusted_Connection=yes;'
# #                               'autocommit=True'
#                              )
#             cursor=conn.cursor()
#             cursor.execute("INSERT INTO [FHIR_cr].[dbo].[Resource_Layer](Resource_Layer,Num_Layer)VALUES('"+ layer_list_combine[0] + "', '"+ str(layer_list_combine[1]) + "')")

#             cursor.commit()
#         except:
#              print('warnings:', layer_list_combine[0])


# In[ ]:




