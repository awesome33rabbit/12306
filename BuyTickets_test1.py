from splinter.browser import Browser
from time import sleep


'''
实现自动抢火车票(基于Python3.6+splinter)
Created on 2019年1月15日
@author: pumingzheng
'''


# 实现自动购票的类
class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends):
        self.username = username
        self.passwd = passwd
        # 车次，0代表所有车次，依次从上到下，1代表所有车次，依次类推
        self.order = order
        # 乘客名
        self.passengers = passengers
        # 起始地和终点
        self.starts = starts
        self.ends = ends
        # 日期
        self.dtime = dtime
        # self.xb = xb
        # self.pz = pz
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        self.initMy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
        self.executable_path = 'D:\Python36\Scripts\chromedriver.exe'

    # 登录功能实现
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name', self.username)
        # sleep(1)
        self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('请输入验证码...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name)
        # 窗口大小的操作
        self.driver.driver.set_window_size(700, 500)
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始购票...')
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        self.driver.find_by_text('预订')[self.order - 1].click()
                        # a = self.driver.find_by_text('预订')
                        # print(a, len(a))
                        sleep(1.5)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        for i in self.driver.find_by_text('预订'):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            print('开始预订...')
            sleep(10)
            print('开始选择用户...')
            for p in self.passengers:
                self.driver.find_by_text(p).last.click()
                sleep(0.5)
                if p[-1] == ')':
                    self.driver.find_by_id('dialog_xsertcj_ok').click()
            print('提交订单...')
            # sleep(1)
            # self.driver.find_by_text(self.pz).click()
            # sleep(1)
            # self.driver.find_by_text(self.xb).click()
            # sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            sleep(2)
            print('确认选座...')
            self.driver.find_by_id('qr_submit_id').click()
            print('预订成功...')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # 用户名
    username = '**********'
    # 密码
    password = '**********'
    # 车次选择，0代表所有车次
    order = 29
    # 乘客名，比如passengers = ['XXX', 'XXX']
    # 学生票需注明，注明方式为：passengers = ['XXX(学生)', 'XXX']
    passengers = ['XXX']
    # 日期，格式为：'2018-02-10'
    dtime = '2019-02-10'
    dtime = '2019-01-24'
    # 出发地(需填写cookie值)
    starts = u'%u6F5C%u6C5F%2CQJN'  # 潜江
    # starts = u'%u5E7F%u5DDE%2CGZQ'  # 广州
    # 目的地(需填写cookie值)
    ends = u'%u6B66%u6C49%2CWHN'  # 广州 %u6B66%u6C49%2CWHN
    # ends = u'%u6DF1%u5733%2CSZQ'  # 北京 %u6B66%u6C49%2CWHN

    # xb =['硬座座']
    # pz=['成人票']

    Buy_Tickets(username, password, order, passengers, dtime, starts, ends).start_buy()

    sleep(20)
