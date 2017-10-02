#CoreTM
# -*- coding: utf-8 -*-
import telebot
import random
from telebot import types
from telebot import util
from random import randint
import redis
import json
import logging
import urllib
import urllib2
import time
import logging
import subprocess
import math
import requests
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sudo = 438573461
token = "466072424:AAHKR-wy9alETrHGjTbHXh6klKzVdfp8los" #TOKEN
bot = telebot.TeleBot(token)
R = redis.StrictRedis(host='localhost', port=6379, db=0)

@bot.message_handler(commands=['start'])
def rate(m):
      markup = types.InlineKeyboardMarkup()
      rate = types.InlineKeyboardButton('منو راهنما', callback_data='help')
      markup.add(rate)
      s = types.InlineKeyboardButton('تنظیمات', callback_data='setting')
      markup.add(s)
      bot.send_message(m.chat.id,'*سلام خوش آمدی\nChannel @MrCruel\nDev @Mr_Cruel\n\nتوجه قبل از شروع کاربا ربات لطفا از منو تنظیمات قالب خود را تنظیم کنید',reply_markup=markup)
@bot.message_handler(commands=['sendall'])
def sendall(m):
    if m.chat.id == sudo :
        text = m.text.replace('/sendall ','')
        ids = R.smembers("our:users")
        for id in ids:
            try:
                bot.send_message(id,text)
            except:
                R.srem("our:users",id)
@bot.message_handler(commands=['fwdtoall'])
def fwdall(m):
    if m.chat.id == sudo :
        if m.reply_to_message:
            mid = m.reply_to_message.message_id
            ids = R.smembers("our:users")
            for id in ids:
                try:
                    bot.forward_message(id,m.chat.id,mid)
                except:
                    R.srem("our:users",id)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try :
        if call.data == "ah":
            R.set("type:{}".format(call.message.chat.id),"circlepro")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=" قالب فایل شما به دایره تنظیم شد ")
        if call.data == "help":
            markup = types.InlineKeyboardMarkup()
            s3 = types.InlineKeyboardButton('بازگشت', callback_data='start')
            markup.add(s3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" این ربات میتواند با متن دلخواه شما فایل مخصوصی برای ساخت پک استیکر در ربات @stickers بسازد\nشما میتوانید در بخش تنظیمات قابل فایل خود را انتخاب کنی", reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="به منو راهنما خوش آمدید")
        elif call.data == "setting":
            markup = types.InlineKeyboardMarkup()
            bye = types.InlineKeyboardButton('مربع', callback_data='sqr')
            n = types.InlineKeyboardButton('بیضی', callback_data='ovl')
            b = types.InlineKeyboardButton('دایره', callback_data='ah')
            l = types.InlineKeyboardButton('بازگشت', callback_data='start')
            markup.add(bye)
            markup.add(n)
            markup.add(b)
            markup.add(l)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="لطفا قالب فایل خود را انتخاب کنید!", reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="به منو تنظیمات خوش آمدید")
        elif call.data == "start":
            markup = types.InlineKeyboardMarkup()
            bye = types.InlineKeyboardButton('منو راهنما', callback_data='help')
            n = types.InlineKeyboardButton('تنظیمات', callback_data='setting')
            markup.add(bye)
            markup.add(n)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="سلام خوش آمدی\nChannel : @MrCruel\nDev : @Mr_Cruel", reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="امیدوارم از من خوشت بیاد :)")
        elif call.data == "sqr":
            R.set("type:{}".format(call.message.chat.id),"squer")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="قالب فایل شما به مربع تنظیم شد")
        elif call.data == "ovl":
            R.set("type:{}".format(call.message.chat.id),"oval")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=" قالب فایل شما به بیضی تنظیم شد" )
    except Exception as e:
        bot.send_message(logchat,e)
@bot.message_handler(func=lambda message: True)
def all(m):
    try:
        if m.text == "/start" :
            R.sadd("our:users",m.chat.id)
        elif m.text == "/help" :
            return None
        elif m.text == "/users" :
            return None
        elif m.text == "/fwdall" :
            return None
        elif re.match(r"/sendall (.*)", m.text):
            return None
        else:
            typ = R.get("type:{}".format(m.chat.id)) or "circlepro"
            text = urllib.urlencode({'txtclr': 'ffffff', 'txt': m.text, 'txtfit': 'max', 'txtsize' : '200', 'txtalign' : 'center,middle', 'txtfont' : 'PT Serif,Bold'})
            text2 = text.replace("+","%20")
            link = "http://iteam.imgix.net/{}.png?{}".format(typ,text2)
            urllib.urlretrieve(link, "SMaker.png")
            file = open('SMaker.png', 'rb')
            bot.send_document(m.chat.id,file)
            bot.send_message(m.chat.id,'@stickers')
    except Exception as e:
        bot.send_message(sudo,e)
bot.polling(True)
#end
