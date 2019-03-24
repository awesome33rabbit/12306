#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Pu MingZheng
@license: Apache Licence 
@file: selenium_12306.py
@time: 2019/3/21 13:27
"""

from selenium import webdriver
from time import sleep
from urllib.request import quote


class GetTicket():
    def __init__(self):
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.search_url ='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={},QJN&ts={},WHN&date=2019-{}&flag=N,N,Y'
        self.driver = webdriver.Chrome()

    def login(self, username, password):
        self.driver.get(self.login_url)
        sleep(2)
        self.driver.find_element_by_class_name('login-hd-account').click()
        sleep(2)

        self.driver.find_element_by_id('J-userName').send_keys(username)
        sleep(2)
        self.driver.find_element_by_id('J-password').send_keys(password)
        print('等待输入验证码')
        sleep(10)
        try:
            name = self.driver.find_element_by_class_name('txt-primary')
            print(name.text)
            print('登陆成功')
        except:
            print('登陆失败')

    def search_buy(self, fromStation, toStation, fromDate):
        fromStation = quote(fromStation, encoding='utf-8')
        toStation = quote(toStation, encoding='utf-8')
        search_url = self.search_url.format(fromStation, toStation, fromDate)
        self.driver.get(search_url)
        sleep(2)
        Reserve = self.driver.find_elements_by_link_text('预定')
        print(len(Reserve))




if __name__ == '__main__':
    username = '******'
    password = '******'
    ticket = GetTicket()
    ticket.login(username, password)
    fromStation = input('输入出发地：')
    toStation = input('输入目的地：')
    fromDate = input('输入出发日期（例：03-24）：')
    ticket.search_buy(fromStation, toStation, fromDate)
