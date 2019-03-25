#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Pu MingZheng
@license: Apache Licence 
@file: selenium_12306.py
@time: 2019/3/24 23:27
"""
import requests

from selenium import webdriver
from time import sleep
from urllib.request import quote

from selenium.webdriver.common.keys import Keys


class GetTicket():
    def __init__(self):
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        # self.search_url ='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={},QJN&ts={},WHN&date=2019-{}&flag=N,N,Y'
        self.search_url = 'https://www.12306.cn/index/index.html'
        # self.search_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver = webdriver.Chrome()

    def login(self, username, password):
        self.driver.get(self.login_url)
        c_url = self.driver.current_url
        sleep(2)
        self.driver.find_element_by_class_name('login-hd-account').click()
        sleep(2)

        self.driver.find_element_by_id('J-userName').send_keys(username)
        sleep(2)
        self.driver.find_element_by_id('J-password').send_keys(password)
        print('等待输入验证码')
        sleep(5)
        self.driver.find_element_by_id('J-login').click()
        try:
            name = self.driver.find_element_by_class_name('txt-primary')
            print(name.text)
        except:
            print('。。。。。')

        sleep(2)
        if self.driver.current_url != c_url:
            print('登陆成功')
        else:
            print('登陆失败')

    def search_buy(self, fromStation, toStation, fromDate, names):
        # fromStation = quote(fromStation, encoding='utf-8')
        # toStation = quote(toStation, encoding='utf-8')
        # search_url = self.search_url.format(fromStation, toStation, fromDate)
        self.driver.get(self.search_url)
        self.driver.implicitly_wait(10)
        sleep(1)
        self.driver.find_element_by_id('fromStationText').click()
        sleep(0.5)
        self.driver.find_element_by_id('fromStationText').send_keys(fromStation)  # 出发地
        sleep(0.5)
        self.driver.find_element_by_id('fromStationText').send_keys(Keys.ENTER)
        sleep(0.5)
        self.driver.find_element_by_id('toStationText').send_keys(toStation)  # 到达地
        sleep(0.5)
        self.driver.find_element_by_id('toStationText').send_keys(Keys.ENTER)
        sleep(0.5)

        js = 'document.getElementById("train_date").removeAttribute("readonly");'
        js_value = "document.getElementById('train_date').value='%s'" % (fromDate)  # 出发日期
        self.driver.execute_script(js)
        self.driver.execute_script(js_value)
        self.driver.find_element_by_id('search_one').click()

        sleep(5)
        self.driver.switch_to_window(self.driver.window_handles[1])  # 跳转页面
        c_url = self.driver.current_url
        button = self.driver.find_elements_by_xpath('//*[@id="queryLeftTable"]/tr/td[13]')  # 获取所有的 ‘预订’ 按钮
        print(len(button))

        count = 0
        while self.driver.current_url == c_url:
            self.driver.find_element_by_id('query_ticket').click()
            sleep(0.5)
            button = self.driver.find_elements_by_xpath('//*[@id="queryLeftTable"]/tr/td[13]')  # 循环点击查询
            print(len(button), '*')
            count += 1
            print('循环点击查询...  第 {} 次'.format(count))
            sleep(1)
            button[1].click()  # 购票
            sleep(0.5)
            if self.driver.current_url != c_url:
                print('预订成功')
                break
            else:
                print('预订失败')
        sleep(5)
        print(self.driver.current_url)

        name_list = self.driver.find_elements_by_xpath('//*[@id="normal_passenger_id"]/li/label')  # 获取乘客信息列表
        print(len(name_list))
        new_list = []
        for i in name_list:
            print(i.text)
            new_list.append(i.text)

        normalPassenger_ = []
        for i in names:
            if i in new_list:
                normalPassenger_.append(new_list.index(i))

        # 添加购票乘客
        for i in normalPassenger_:
            normalPassenger = 'normalPassenger_{}'.format(i)
            self.driver.find_element_by_id(normalPassenger).click()
        sleep(0.5)

        # 提交订单
        self.driver.find_element_by_id('submitOrder_id').click()
        sleep(0.5)
        self.driver.find_element_by_id('qr_submit_id').click()


if __name__ == '__main__':
    username = '********'
    password = '********'
    names = ['name1', 'name2']
    ticket = GetTicket()
    ticket.login(username, password)
    sleep(5)
    fromStation = '武汉'
    toStation = '南京'
    fromDate = '2019-03-28'
    ticket.search_buy(fromStation, toStation, fromDate, names)
