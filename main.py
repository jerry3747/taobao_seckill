#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import datetime
from tkinter import *
from seckill.seckill_taobao import ChromeDrive



def run_killer(txt, txt2):
    seckill_time = txt.get()
    password = str(txt2.get())
    print(seckill_time, password)
    ChromeDrive(seckill_time = seckill_time, password = password).sec_kill()



def main():
    win = Tk()
    win.title('小熊秒杀助手')
    width = 380
    height = 300
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(alignstr)

    lbl = Label(win, text = "开抢时间：", width = 8, height = 2)
    lbl.grid(column = 0, row = 0)
    start_time = StringVar()
    txt = Entry(win, textvariable = start_time, width = 18)
    txt.grid(column = 1, row = 0)
    start_time.set(str(datetime.datetime.now()))

    lbl2 = Label(win, text = "支付密码：", width = 8, height = 2)
    lbl2.grid(column = 0, row = 1)
    txt2 = Entry(win, width = 18, show = '*')
    txt2.grid(column = 1, row = 1)

    b1 = Button(win, text = '开始', command = lambda: run_killer(txt, txt2))
    b1.config(font = 'Helvetica -10 bold', bg = 'red', relief = 'sunken', width = 8, height = 6)
    b1.place(x=300, y=5)
    win.resizable(width = False, height = False)

    txt0 = Label(win, text = '使用说明:',width = 8, height = 2)
    txt0.grid(column = 0, row = 3)

    txt3 = Label(win, text = '1、安装chrome浏览器以及chromeDriver')
    txt3.config(font = 'Helvetica -10 bold', fg = 'red')
    txt3.place(x = 10, y = 120)

    txt4 = Label(win, text = '2、抢购前要清空购物车，然后把要抢的东西加入购物车')
    txt4.config(font = 'Helvetica -10 bold', fg = 'red')
    txt4.place(x = 10, y = 140)

    txt5 = Label(win, text = '3、开抢时间必须是 %Y-%m-%d %H:%M:%S 形式，如2020-12-29 12:10:15' )
    txt5.config(font = 'Helvetica -10 bold', fg = 'red')
    txt5.place(x=10, y=160)

    txt6 = Label(win, text = '4、输入开抢时间和支付密码后点开始，程序会控制浏览器打开淘宝登陆页')
    txt6.config(font = 'Helvetica -10 bold', fg = 'red')
    txt6.place(x = 10, y = 180)

    txt7 = Label(win, text = '5、扫码登陆后，程序会自动刷新购物车页面，到点会完成抢购动作')
    txt7.config(font = 'Helvetica -10 bold', fg = 'red')
    txt7.place(x = 10, y = 200)

    txt8 = Label(win, text = '6、本项目仅供交流学习使用，请勿用于其它任何商业用途')
    txt8.config(font = 'Helvetica -10 bold', fg = 'red')
    txt8.place(x = 10, y = 220)

    txt9 = Label(win, text = '7、如果想手动付款，输入开抢时间后不用输入支付密码，直接点开始就可以了')
    txt9.config(font = 'Helvetica -10 bold', fg = 'red')
    txt9.place(x = 10, y = 240)
    win.mainloop()


if __name__ == '__main__':
    main()
