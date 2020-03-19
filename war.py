import discord
import os.path
import random
import datetime
import os
import sys
import subprocess
import threading
import re
from time import sleep
from twitter import *
import atexit
import schedule
import time
import urllib.request
import urllib.error
import requests
from requests_oauthlib import OAuth1Session
import json
import types
import shutil
import glob
import pya3rt
import logging
import linecache
from gyazo import Api
from PIL import Image, ImageOps
import cv2
import importlib.util
import numpy as np
from twython import Twython, TwythonError
import oauth2
import asyncio
import traceback
from pytz import timezone

#ツイート時間計算機
def TweetId2Time(url):
    id = int(twitterid_url(url))
    epoch = ((id >> 22) + 1288834974657) / 1000.0
    d = datetime.datetime.fromtimestamp(epoch)
    stringTime = d.strftime('%Y-%m-%d %H:%M:%S.%f')
    return stringTime[:-3]

def load_movieodai(count):
    odailist = []
    musicname = linecache.getline('Clientdata/odai/映像大会お題/{0}/settings.txt'.format(count), 1).replace('\n', '')
    janru = linecache.getline('Clientdata/odai/映像大会お題/{0}/settings.txt'.format(count), 2).replace('\n', '')
    bpm = linecache.getline('Clientdata/odai/映像大会お題/{0}/settings.txt'.format(count), 3).replace('\n', '')
    credit1 = linecache.getline('Clientdata/odai/映像大会お題/{0}/settings.txt'.format(count), 4).replace('\n', '')
    credit2 = linecache.getline('Clientdata/odai/映像大会お題/{0}/settings.txt'.format(count), 5).replace('\n', '')
    teian = linecache.getline('Clientdata/odai/映像大会お題/{0}/settings.txt'.format(count), 6).replace('\n', '')
    odailist.append(musicname)
    odailist.append(janru)
    odailist.append(bpm)
    odailist.append(credit1)
    odailist.append(credit2)
    odailist.append(teian)
    return odailist

def tweet_genkai(content):
    consumer_key = "*"
    consumer_secret = "*"
    token = "*"
    token_secret = "*"
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    t.statuses.update(status=content)

def tweet_elodo(content):
    consumer_key = "*"
    consumer_secret = "*"
    token = "*"
    token_secret = "*"
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    t.statuses.update(status=content)

def rt_genkaibot(twitterid):
    consumer_key = "*"
    consumer_secret = "*"
    token = "*"
    token_secret = "*"
    t = Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    t.statuses.retweet(id=twitterid)

def tweet_elodo_image(content, image):
    f = urllib.request.Request(image, headers={'User-Agent': 'Mozilla/5.0'})
    f_open = urllib.request.urlopen(f)
    get_img = f_open.read()
    consumer_key = "*"
    consumer_secret = "*"
    token = "*"
    token_secret = "*"
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    t_upload = Twitter(domain='upload.twitter.com',auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    id_img1 = t_upload.media.upload(media=get_img)["media_id_string"]
    t.statuses.update(status=content, media_ids=",".join([id_img1]))

def load_dic(path):
    with open(path, encoding='utf-8') as open_file:
        raw = open_file.read()
    point = raw.splitlines()
    p_dict = {}
    for line in point:
        name,points_str = line.split(';')
        p_dict[name] = points_str
    print(p_dict)
    return p_dict

def writefile_add(path, content):
    f = open(path, 'a', encoding='utf-8')
    f.write(content)
    f.close()

def ai_talk(message):
    do_dic = load_dic('Clientdata\dic\do.txt')
    thing_dic = load_dic('Clientdata/dic/thing.txt')
    resp_dic = load_dic('Clientdata/dic/response.txt')
    words = ""
    response = ""
    for key in do_dic:
        if key in message:
            if do_dic[key] not in words:
                words += do_dic[key]+','
    print(response)
    for key in thing_dic:
        if key in message:
            if thing_dic[key] not in words:
                words += thing_dic[key]+','
    for key in resp_dic:
        if words == key:
            response = resp_dic[key]
    print(response)
    print(words)
    if response == "":
        response = ":bow: 理解できませんでした・・・\n単語の意味を尋ねる場合は、`〇〇について教えて！`と言ってください。\nまたは、`/wiki`コマンドで検索することもできます！"
        content = '本文：{0}, 単語：{1}\n'.format(message, words)
        writefile_add('Clientdata/dic/study.txt', content)
    content = '本文：{0}, 単語：{1}, 返信：{2}\n'.format(message, words, response)
    writefile_add('Clientdata/dic/result.txt', content)
    return response

def isurl(url, domain):
    if (url.count('/') < 3):
        raise Exception
    url_data = url.split('/')
    if (url_data[2] == domain):
        return True
    else:
        return False

def twitterid_url(url):
    url_data = url.split('/')
    if ('?' in url_data[5]):
        url_data = url_data[5].split('?')
        return url_data[0]
    else:
        return url_data[5]

async def eizo_start():
    count = linecache.getline('Clientdata/odai/映像大会お題/count.txt', 1).replace('\n', '')
    if os.path.exists('Clientdata/odai/映像大会お題/{0}'.format(count)):
        if os.path.exists('Clientdata/odai/映像大会お題/{0}/settings.txt'.format(count)):
            try:
                if odailist[4] == '1':credit3 = 'この音源は本大会のために特別に許諾を頂いたものです。ツイート本文に以下のライセンス情報をコピーペーストしてください。'
                elif odailist[4] == '2':credit3 = 'この音源はCreativeCommonsLicense楽曲です。ツイート本文に以下のライセンス情報をコピーペーストしてください。'
                else:credit3 = odailist[4]
                channel = client.get_channel(498872353971765269)
                await channel.send('@here\n:alarm_clock: 第{0}回限界映像大会 お題発表\n\n曲名: {1}\nジャンル: {2}\n提案者: <@{3}>\n完成した作品は`#限界映像大会`を付けてツイート！'\
                                    '\n参加前に<#523156728741625875>をご一読ください！'.format(count, musicname, janru, teian))
                await channel.send(file=discord.File('Clientdata/odai/映像大会お題/{0}/genkai{0}.wav'.format(count)))
                await channel.send('{0}\n`{1}`\nBPM(測定値): {2}'.format(credit3, credit2, BPM))
                channel = client.get_channel(498872353971765269)
                await channel.send(':pushpin: 第{0}回限界映像大会 お題発表\n\n曲名: {1}\nジャンル: {2}\nお題楽曲は https://discord.gg/6tAqA7s で配布しています。\n完成した作品は`#限界映像大会`をつけてツイート！'.format(count, musicname, janru))
                tweet_genkai('第{0}回限界映像大会 お題発表\n\n曲名: {1}\nジャンル: {2}\nお題楽曲は https://discord.gg/6tAqA7s で配布しています。\n完成した作品は #限界映像大会 をつけてツイート！\n#限界映像大会'.format(count, musicname, janru))
                linecache.clearcache()
                count_next = int(count) + 1
                if os.path.exists('Clientdata/odai/映像大会お題/{0}'.format(str(count_next))):
                    log_client.info('ファイルがすでに存在しました。')
                else:
                    os.mkdir('Clientdata/odai/映像大会お題/{0}'.format(str(count_next)))
                f = open('Clientdata/odai/映像大会お題/count.txt','w')
                f.write('{0}\n'.format(count_next))
                f.close()
            except:
                log_client.warning(traceback.format_exc())
                asyncio.create_task(eizo_backup())
        else:
            asyncio.create_task(eizo_backup())
    else:
        asyncio.create_task(eizo_backup())

async def eizo_backup():
    count = linecache.getline('Clientdata/odai/映像大会お題/count.txt', 1).replace('\n', '')
    musicname = linecache.getline('Clientdata/odai/映像大会お題/0/settings.txt', 1).replace('\n', '')
    janru = linecache.getline('Clientdata/odai/映像大会お題/0/settings.txt', 2).replace('\n', '')
    bpm = linecache.getline('Clientdata/odai/映像大会お題/0/settings.txt', 3).replace('\n', '')
    credit1 = linecache.getline('Clientdata/odai/映像大会お題/0/settings.txt', 4).replace('\n', '')
    credit2 = linecache.getline('Clientdata/odai/映像大会お題/0/settings.txt', 5).replace('\n', '')
    teian = linecache.getline('Clientdata/odai/映像大会お題/0/settings.txt', 6).replace('\n', '')
    if credit1 == '1':credit3 = 'この音源は本大会のために特別に許諾を頂いたものです。ツイート本文に以下のライセンス情報をコピーペーストしてください。'
    elif credit1 == '2':credit3 = 'この音源はCreativeCommonsLicense楽曲です。ツイート本文に以下のライセンス情報をコピーペーストしてください。'
    else:credit3 = credit1
    channel = client.get_channel(523156712149221376)
    await channel.send('@here\n:alarm_clock: 第{0}回限界映像大会 お題発表\n\n曲名: {1}\nジャンル: {2}\n提案者: <@{3}>\n完成した作品は`#限界映像大会`を付けてツイート！'.format(count, musicname, janru, teian))
    await channel.send('参加前に<#523156728741625875>をご一読ください！')
    await channel.send(file=discord.File('Clientdata/odai/映像大会お題/0/genkai.wav'))
    await channel.send('{0}\n`{1}`'.format(credit3, credit2))
    await channel.send('BPM(測定値): {0}'.format(bpm))
    channel = client.get_channel(499236063265685505)
    await channel.send(':pushpin: 第{0}回限界映像大会 お題発表\n\n曲名: {1}\nジャンル: {2}\nお題楽曲は https://discord.gg/6tAqA7s で配布しています。\n完成した作品は`#限界映像大会`をつけてツイート！'.format(count, musicname, janru))
    consumer_key = "*"
    consumer_secret = "*"
    token = "*"
    token_secret = "*"
    t = Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    t.statuses.update(status='第{0}回限界映像大会 お題発表\n\n曲名: {1}\nジャンル: {2}\nお題楽曲は https://discord.gg/6tAqA7s で配布しています。\n完成した作品は #限界映像大会 をつけてツイート！\n#限界映像大会'.format(count, musicname, janru))
    linecache.clearcache()
    count_next = int(count) + 1
    if os.path.exists('Clientdata/odai/映像大会お題/{0}'.format(str(count_next))):
        log_client.info('ファイルがすでに存在しました。')
    else:
        os.mkdir('Clientdata/odai/映像大会お題/{0}'.format(str(count_next)))
    f = open('Clientdata/odai/映像大会お題/count.txt','w')
    f.write('{0}\n'.format(count_next))
    f.close()

async def eizo_end():
    count = linecache.getline('Clientdata/odai/映像大会お題/count.txt', 1).replace('\n', '')
    count = int(count) - 1
    channel = client.get_channel(523156688921165824)
    await channel.send('@here\n:loudspeaker: 第{0}回限界映像大会終了のお知らせ\n\n限界映像大会は終了しました。作品のご投稿ありがとうございました。\nまだ動画を製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。'.format(count))
    consumer_key = "*"
    consumer_secret = "*"
    token = "*"
    token_secret = "*"
    t = Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    t.statuses.update(status='第{0}回限界映像大会終了のお知らせ\n\n限界映像大会は終了しました。作品のご投稿ありがとうございました。\nまだ動画を製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。\n\n#限界映像大会'.format(count))

async def taikai_end():
    count = linecache.getline('Clientdata/odai/限界大会お題/count.txt', 1).replace('\n', '')
    if (count == '1'):
        count_time = linecache.getline('Clientdata/odai/限界大会お題/モデリング大会/count.txt', 1).replace('\n', '')
        channel = client.get_channel(523156688921165824)
        await channel.send('@here\n:loudspeaker: 第{0}回限界モデリング大会終了のお知らせ\n\n限界モデリング大会は終了しました。作品のご投稿ありがとうございました。\nまだ製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。'.format(count_time))
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status='第{0}回限界モデリング大会終了のお知らせ\n\n限界モデリング大会は終了しました。作品のご投稿ありがとうございました。\nまだ製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。\n\n#限界モデリング大会'.format(count_time))
        count_time = int(count_time) + 1
        f = open('Clientdata/odai/限界大会お題/count.txt','w')
        f.write('2\n')
        f.close()
        f = open('Clientdata/odai/限界大会お題/モデリング大会/count.txt','w')
        f.write('{0}\n'.format(count_time))
        f.close()
        linecache.clearcache()
    elif (count == '2'):
        count_time = linecache.getline('Clientdata/odai/限界大会お題/DTM大会/count.txt', 1).replace('\n', '')
        channel = client.get_channel(523156688921165824)
        await channel.send('@here\n:loudspeaker: 第{0}回限界DTM大会終了のお知らせ\n\n限界DTM大会は終了しました。作品のご投稿ありがとうございました。\nまだ製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。'.format(count_time))
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status='第{0}回限界DTM大会終了のお知らせ\n\n限界DTM大会は終了しました。作品のご投稿ありがとうございました。\nまだ製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。\n\n#限界DTM大会'.format(count_time))
        count_time = int(count_time) + 1
        f = open('Clientdata/odai/限界大会お題/count.txt','w')
        f.write('3\n')
        f.close()
        f = open('Clientdata/odai/限界大会お題/DTM大会/count.txt','w')
        f.write('{0}\n'.format(count_time))
        f.close()
        linecache.clearcache()
    elif (count == '3'):
        count_time = linecache.getline('Clientdata/odai/限界大会お題/デザイン大会/count.txt', 1).replace('\n', '')
        channel = client.get_channel(523156688921165824)
        await channel.send('@here\n:loudspeaker: 第{0}回限界デザイン大会終了のお知らせ\n\n限界デザイン大会は終了しました。作品のご投稿ありがとうございました。\nまだ製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。'.format(count_time))
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status='第{0}回限界デザイン大会終了のお知らせ\n\n限界デザイン大会は終了しました。作品のご投稿ありがとうございました。\nまだ製作中の方、後日投稿する方はツイートに遅刻であることを記載してください。\n\n#限界デザイン大会'.format(count_time))
        count_time = int(count_time) + 1
        f = open('Clientdata/odai/限界大会お題/count.txt','w')
        f.write('1\n')
        f.close()
        f = open('Clientdata/odai/限界大会お題/デザイン大会/count.txt','w')
        f.write('{0}\n'.format(count_time))
        f.close()
        linecache.clearcache()

async def taikai_start():
    count = linecache.getline('Clientdata/odai/限界大会お題/count.txt', 1).replace('\n', '')
    if (count == '1'):
        count_time = linecache.getline('Clientdata/odai/限界大会お題/モデリング大会/count.txt', 1).replace('\n', '')
        f = open("Clientdata/odai/限界大会お題/モデリング大会/odai.txt", "r", encoding='UTF-8')
        l = f.readlines()
        s = random.sample(l, 1)
        odai = "".join(s)
        odai = odai.strip()
        f.close()
        with open('Clientdata/odai/限界大会お題/モデリング大会/odai.txt', encoding='UTF-8') as f:
            taikai_data=f.read()
            taikai_data=taikai_data.replace(odai,'')
            content = re.sub(r'^[\r\n]+', '', taikai_data, flags=re.MULTILINE)
            f = open('Clientdata/odai/限界大会お題/モデリング大会/odai.txt', 'w')
            f.write(content)
            f.close()
        channel = client.get_channel(523535822566195201)
        await channel.send('@here\n:alarm_clock: 第{0}回限界モデリング大会 お題発表\n\n今回のお題は `{1}` です。\n完成した作品は `#限界モデリング大会` でツイート！'.format(count_time, odai))
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status='第{0}回限界モデリング大会 お題発表\n\n今回のお題は {1} です。\n完成した作品は #限界モデリング大会 でツイート！\n\n詳しくはこちら\nhttps://apps.m86.work/genkai/\n\n#限界モデリング大会'.format(count_time, odai))
    elif (count == '2'):
        count_time = linecache.getline('Clientdata/odai/限界大会お題/DTM大会/count.txt', 1).replace('\n', '')
        f = open("Clientdata/odai/限界大会お題/DTM大会/odai.txt", "r", encoding='UTF-8')
        l = f.readlines()
        s = random.sample(l, 1)
        odai = "".join(s)
        odai = odai.strip()
        f.close()
        with open('Clientdata/odai/限界大会お題/DTM大会/odai.txt', encoding='UTF-8') as f:
            taikai_data=f.read()
            taikai_data=taikai_data.replace(odai,'')
            content = re.sub(r'^[\r\n]+', '', taikai_data, flags=re.MULTILINE)
            f = open('Clientdata/odai/限界大会お題/DTM大会/odai.txt', 'w')
            f.write(content)
            f.close()
        channel = client.get_channel(523452026236043264)
        await channel.send('@here\n:alarm_clock: 第{0}回限界DTM大会 お題発表\n\n今回のお題は `{1}` です。\n完成した作品は `#限界DTM大会` でツイート！'.format(count_time, odai))
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status='第{0}回限界DTM大会 お題発表\n\n今回のお題は {1} です。\n完成した作品は #限界DTM大会 でツイート！\n\n詳しくはこちら\nhttps://apps.m86.work/genkai/\n\n#限界DTM大会'.format(count_time, odai))
    elif (count == '3'):
        count_time = linecache.getline('Clientdata/odai/限界大会お題/デザイン大会/count.txt', 1).replace('\n', '')
        f = open("Clientdata/odai/限界大会お題/デザイン大会/odai.txt", "r", encoding='UTF-8')
        l = f.readlines()
        s = random.sample(l, 1)
        odai = "".join(s)
        odai = odai.strip()
        f.close()
        with open('Clientdata/odai/限界大会お題/デザイン大会/odai.txt', encoding='UTF-8') as f:
            taikai_data=f.read()
            taikai_data=taikai_data.replace(odai,'')
            content = re.sub(r'^[\r\n]+', '', taikai_data, flags=re.MULTILINE)
            f = open('Clientdata/odai/限界大会お題/デザイン大会/odai.txt', 'w')
            f.write(content)
            f.close()
        channel = client.get_channel(523538442135535636)
        await channel.send('@here\n:alarm_clock: 第{0}回限界デザイン大会 お題発表\n\n今回のお題は `{1}` です。\n完成した作品は `#限界デザイン大会` でツイート！'.format(count_time, odai))
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status='第{0}回限界デザイン大会 お題発表\n\n今回のお題は {1} です。\n完成した作品は #限界デザイン大会 でツイート！\n\n詳しくはこちら\nhttps://apps.m86.work/genkai/\n\n#限界デザイン大会'.format(count_time, odai))

async def taikai_promo():
    count = linecache.getline('Clientdata/odai/限界大会お題/count.txt', 1).replace('\n', '')
    if (count == '1'):
        channel = client.get_channel(523156688921165824)
        await channel.send('@here\n:tada: 本日の大会のお知らせ :tada:\n\n本日は限界モデリング大会です！\nお題発表は本日6時！\n参加前にルールをご一読ください！')
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status="本日の大会のお知らせ\n\n本日は #限界モデリング大会 です。\n参加方法はサイトをチェック!\nhttps://apps.m86.work/genkai/\nお題発表は本日6時!\n#限界モデリング大会")
    elif (count == '2'):
        channel = client.get_channel(523156688921165824)
        await channel.send('@here\n:tada: 本日の大会のお知らせ :tada:\n\n本日は限界DTM大会です！\nお題発表は本日6時！\n参加前にルールをご一読ください！')
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status="本日の大会のお知らせ\n\n本日は #限界DTM大会 です。\n参加方法はサイトをチェック!\nhttps://apps.m86.work/genkai/\nお題発表は本日6時!\n#限界DTM大会")
    elif (count == '3'):
        channel = client.get_channel(523156688921165824)
        await channel.send('@here\n:tada: 本日の大会のお知らせ :tada:\n\n本日は限界デザイン大会です！\nお題発表は本日6時！\n参加前にルールをご一読ください！')
        consumer_key = "*"
        consumer_secret = "*"
        token = "*"
        token_secret = "*"
        t = Twitter(
            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
        t.statuses.update(status="本日の大会のお知らせ\n\n本日は #限界デザイン大会 です。\n参加方法はサイトをチェック!\nhttps://apps.m86.work/genkai/\nお題発表は本日6時!\n#限界デザイン大会")

# 限界大会宣伝
async def eizo_promo():
    consumer_key = "*"
    consumer_secret = "*"
    token = "*"
    token_secret = "*"
    t = Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    t.statuses.update(status="本日の大会のお知らせ\n\n本日は #限界映像大会 です。\n参加方法はサイトをチェック!\nhttps://dev.m86.work/pages/genkai\nお題発表は本日6時!\n#限界映像大会")
    channel = client.get_channel(523156688921165824)
    await channel.send('@here\n:tada: 本日の大会のお知らせ :tada:\n\n本日は限界映像大会です！\nお題発表は本日6時！\n参加前にルールをご一読ください！')

# asyncioのtask作成
def task_eizo_start():
    asyncio.create_task(eizo_start())

def task_eizo_promo():
    asyncio.create_task(eizo_promo())

def task_taikai_end():
    asyncio.create_task(taikai_end())

def task_eizo_end():
    asyncio.create_task(eizo_end())

def task_taikai_start():
    asyncio.create_task(taikai_start())

def task_taikai_promo():
    asyncio.create_task(taikai_promo())

def task_start334():
    asyncio.create_task(start334())

def inputer():
    while True:
        mes = input('>>> ')
        webhook_url = '*'
        payload = {'content': mes}
        requests.post(webhook_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))

#スケジューリング
async def task_timer():
    #映像宣伝
    schedule.every().saturday.at("16:10").do(task_eizo_promo)
    #映像大会投稿
    schedule.every().saturday.at("18:13").do(task_eizo_start)
    #映像大会終了投稿
    schedule.every().sunday.at("00:00").do(task_eizo_end)

    #限界大会宣伝投稿
    schedule.every().sunday.at("12:00").do(task_taikai_promo)
    schedule.every().friday.at("12:00").do(task_taikai_promo)
    #限界大会投稿
    schedule.every().sunday.at("18:00").do(task_taikai_start)
    schedule.every().friday.at("18:08").do(task_taikai_start)
    #限界大会終了投稿
    schedule.every().monday.at("00:00").do(task_taikai_end)
    schedule.every().saturday.at("00:00").do(task_taikai_end)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

#ロガーの設定
logger = logging.getLogger('discord')

logger.setLevel(logging.DEBUG)

output = logging.StreamHandler()
output.setLevel(logging.INFO)
output.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logfile = logging.FileHandler(filename='./Clientdata/log/' + str(datetime.date.today()) + '-warbot.log', encoding='utf-8')
logfile.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logfile_info = logging.FileHandler(filename='./Clientdata/log/' + str(datetime.date.today()) + '-warbot-info.log', encoding='utf-8')
logfile_info.setLevel(logging.INFO)
logfile_info.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(output)
logger.addHandler(logfile)
logger.addHandler(logfile_info)

log_client = logging.getLogger("discord").getChild("warclient")


class MyClient(discord.Client):
    async def on_ready(self): #起動時に実行
        log_client.info('Discordにログインしました。： {0}'.format(self.user))
        log_client.info('起動時処理を開始します。')

        # コマンド入力起動
        log_client.info('スケジューラを起動しました。')
        thread_1 = threading.Thread(target=inputer)
        thread_1.setDaemon(True)
        thread_1.start()

        # 変数の宣言
        global zyoya_count
        zyoya_count = 0
        global pixelsort_process
        pixelsort_process = 0

        # アクティビティアップデート
        await client.change_presence(status=discord.Status.online, activity=discord.Game('WARbot beta4.1.1'))

        # タスク重複の確認
        if len(asyncio.Task.all_tasks()) >= 6:
            log_client.warning('実行タスクが多いので、Discordpyの再起動を行います。')
            loop = asyncio.get_event_loop()
            loop.stop()

        log_client.info('現在の実行タスク数は{0}個です。'.format(len(asyncio.Task.all_tasks())))

        # 定期実行の開始
        asyncio.create_task(task_timer())

    async def on_message(self, message):
        if message.content.startswith('/restart'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if (message.author.id == 227375367990542338 or message.channel.id == 498872353971765269):
                log_client.info('再起動を行います。')
                await message.channel.send(':repeat: 再起動を行います！')
                exit()
            else:
                log_client.warning('権限がありません。')
                await message.channel.send(':warning: おっと、権限をお持ちでないようです！')
            

        if message.content.startswith('/stop'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if (message.author.id == 227375367990542338 or message.channel.id == 498872353971765269):
                log_client.info('動作を停止しています。再開するには何かキーを押してください。')
                await message.channel.send(':warning: サーバーに操作があるまで動作を停止します！')
                input('>>> ')
            else:
                log_client.warning('権限がありません。')
                await message.channel.send(':warning: おっと、権限をお持ちでないようです！')

        if message.content == '/test':
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if (message.author.id == 227375367990542338 or message.channel.id == 498872353971765269):
                log_client.info('テストには何も設定されていません！')
                await message.channel.send(message.author.voice.channel.id)
            else:
                log_client.warning('権限がありません。')
                await message.channel.send(':warning: おっと、権限をお持ちでないようです！')

        if message.content.startswith('/じゃんけん'):
            try:
                janken_command, janken_result = message.content.split()
                janken_resultme = random.randint(1, 3)
                if janken_result == 'グー':
                    if janken_resultme == 1:await message.channel.send(':punch:\nあいこ！')
                    elif janken_resultme == 2:await message.channel.send(':v:\nあなたの勝ち！')
                    elif janken_resultme == 3:await message.channel.send(':hand_splayed:\nあなたの負け！')
                elif janken_result == 'チョキ':
                    if janken_resultme == 1:await message.channel.send(':punch:\nあなたの負け')
                    elif janken_resultme == 2:await message.channel.send(':v:\nあいこ！')
                    elif janken_resultme == 3:await message.channel.send(':hand_splayed:\nあなたの勝ち！')
                elif janken_result == 'パー':
                    if janken_resultme == 1:await message.channel.send(':punch:\nあなたの勝ち！')
                    elif janken_resultme == 2:await message.channel.send(':v:\nあなたの負け！')
                    elif janken_resultme == 3:await message.channel.send(':hand_splayed:\nあいこ！')
                else:
                    await message.channel.send(':no_entry_sign: は？コマンドちげぇし、出直してこいや:punch::boom:')
            except:
                await message.channel.send(':middle_finger: は？コマンドちげぇし、出直してこいや:punch::boom:')

        if message.content.startswith('/about'):
            embed=discord.Embed(title="WARBot", url="https://apps.m86.work/warbot/", description="Version beta 5.0")
            embed.set_author(name="Minato86", url="https://minato86.me", icon_url="https://i.gyazo.com/2c5586d71f838ebee9cbf24932188ed4.jpg")
            embed.set_thumbnail(url="https://i.gyazo.com/dd364ca6df96669cba64638f985ba850.png")
            embed.add_field(name="このBotについて", value="限界創作村に生息するよくわからんBot", inline=True)
            embed.add_field(name="何ができるの？", value="いろいろできます。コマンド一覧はサイトを御覧ください。", inline=False)
            embed.set_footer(text="©2019 Minato86")
            await message.channel.send(embed=embed)

        if message.content.startswith('/wiki'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：'\
                '{0.content}が実行されました。'.format(message))
            commands = message.content.split()
            try:
                await message.channel.send(':mag_right: https://ja.wikipedia.org/wiki/'+commands[1])
            except IndexError:
                print(sys.exc_info())
                await message.channel.send(':mag_right: 質問るにはす、`/wiki [キーワード]`を実行してください。')

        if message.content.startswith('/tweet'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：'\
                '{0.content}が実行されました。'.format(message))
            commands = message.content.split()
            try:
                if (commands[1] == "elodo"):
                    def check(m):
                        return m.author == message.author and m.channel == message.channel
                    await message.channel.send(':pencil: 本文を入力してください')
                    msg = await client.wait_for('message', check=check)
                    tweet_elodo(msg.content)
                    await message.channel.send(':incoming_envelope: 送信しました！')
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：'\
                        '送信先：elodo, 本文:{1} Twitterの投稿に成功しました。'.format(message, msg.content))
                if (commands[1] == "image"):
                    def check(m):
                        return m.author == message.author and m.channel == message.channel
                    await message.channel.send(':speech_balloon: どのアカウントでつぶやきますか？\n'\
                        '```markdown\n# アカウントリスト\nelodo - 限界創作村のマスコット\n```')
                    msg = await client.wait_for('message', check=check)
                    if (msg.content == "elodo"):
                        await message.channel.send(':pencil: 本文を入力してください')
                        text = await client.wait_for('message', check=check)
                        await message.channel.send(':frame_photo: 画像URLを入力してください')
                        image = await client.wait_for('message', check=check)
                        tweet_elodo_image(text.content, image.content)
                        await message.channel.send(':incoming_envelope: 送信しました！')
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：'\
                        '送信先：{1}, 本文:{2}, 画像URL:{3} Twitterの投稿に成功しました。'.format(message, msg.content, text.content, image.content))
            except IndexError:
                print(sys.exc_info())
                await message.channel.send('```markdown\n# tweet系コマンド一覧\n/tweet : tweet系コマンドの一覧を見れます\n'\
                    '/tweet elodo : ELODOにツイートできます。\n'\
                    '/tweet image : 画像付きツイートができます。\n```')
            except TwitterHTTPError:
                print(sys.exc_info())
                await message.channel.send(':no_entry_sign: 送信に失敗しました。すでにツイート済みのツイートではないかご確認ください。')
            except urllib.error.HTTPError:
                print(sys.exc_info())
                await message.channel.send(':no_entry_sign: 画像の取得に失敗しました。URLをご確認ください。')
            except ValueError:
                await message.channel.send(':no_entry_sign: 画像の取得に失敗しました。URLをご確認ください。')
            except:
                await message.channel.send(':no_entry_sign: コマンド実行に失敗しました。送信内容をお確かめください。')
                print(sys.exc_info())

        if message.content.startswith('/talk'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：'\
                '{0.content}が実行されました。'.format(message))
            def check(m):
                return m.author == message.author and m.channel == message.channel
            await message.channel.send(':speech_balloon: なんでも言ってください！')
            msg = await client.wait_for('message', check=check)
            await message.channel.send(ai_talk(msg.content))

        if message.content.startswith('/twitter'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            commands = message.content.split()
            try:
                if (commands[1] == "get"):
                    def check(m):
                        return m.author == message.author and m.channel == message.channel
                    await message.channel.send(':speech_balloon: 何を取得しますか？\n'\
                        '```markdown\n# 取得コマンド一覧'\
                        '\ntweettime - ツイートURLから時間を取得します。\n'\
                        '```')
                    msg = await client.wait_for('message', check=check)
                    if (msg.content == "tweettime"):
                        await message.channel.send(':link: URLを入力してください')
                        url = await client.wait_for('message', check=check)
                        if isurl(url.content, 'twitter.com'):
                            time = TweetId2Time(url.content)
                            await message.channel.send(':alarm_clock: ツイート時間は {0} です！'.format(time))
                        else:
                            await message.channel.send(':no_entry_sign: TwitterのURLを入力してください。')
                    if (msg.content == "tweetid"):
                        await message.channel.send(':link: URLを入力してください')
                        url = await client.wait_for('message', check=check)
                        if isurl(url.content, 'twitter.com'):
                            id = twitterid_url(url.content)
                            await message.channel.send(':paperclip: ツイートIDは {0} です！'.format(id))
                        else:
                            await message.channel.send(':no_entry_sign: TwitterのURLを入力してください。')
            except IndexError:
                print(sys.exc_info())
                await message.channel.send('```markdown\n# twitter系コマンド一覧\n/twitter get : いろいろ取得できます。\n'\
                    '```')
            except Exception:
                print(sys.exc_info())
                await message.channel.send(':no_entry_sign: エラーが発生しました。URL等を確認してください。')

        '''
        if message.content.startswith('https'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}のRTを実行します。'.format(message))
            if (message.channel.id == 464804666782384138):
                tweet_id = message.content.split('/')
                if (tweet_id[2] == 'twitter.com'):
                    if ('?' in tweet_id[5]):
                        tweet_id = tweet_id[5].split('?')
                        consumer_key = "*"
                        consumer_secret = "*"
                        token = "*"
                        token_secret = "*"
                        t = Twitter(
                            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
                        t.statuses.retweet(id='{0}'.format(tweet_id[0]))
                    else:
                        consumer_key = "*"
                        consumer_secret = "*"
                        token = "*"
                        token_secret = "*"
                        t = Twitter(
                            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
                        t.statuses.retweet(id='{0}'.format(tweet_id[5]))
                else:
                    log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：TwitterURLではなかったので、処理をスキップしました。'.format(message))
            elif (message.channel.id == 465062712863490049):
                tweet_id = message.content.split('/')
                if (tweet_id[2] == 'twitter.com'):
                    if ('?' in tweet_id[5]):
                        tweet_id = tweet_id[5].split('?')
                        consumer_key = "*"
                        consumer_secret = "*"
                        token = "*"
                        token_secret = "*"
                        t = Twitter(
                            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
                        res = t.statuses.show(id='{0}'.format(tweet_id[0]), tweet_mode='extended')
                        await message.channel.send('ツイートIDを確認しました。{0}'.format(tweet_id[0]))
                        print(res['created_at'])
                        await message.channel.send(res['extended_entities']['media'][0]['video_info']['variants'][1]['url'])
                    else:
                        consumer_key = "*"
                        consumer_secret = "*"
                        token = "*"
                        token_secret = "*"
                        t = Twitter(
                            auth=OAuth(token, token_secret, consumer_key, consumer_secret))
                        res = t.statuses.show(id='{0}'.format(tweet_id[5]), tweet_mode='extended')
                        await message.channel.send('ツイートIDを確認しました。{0}'.format(tweet_id[5]))
                        print(res)

                        print(res['extended_entities']['media'][0]['video_info']['variants'][1]['url'])

                        #await message.channel.send(res['extended_entities']['media'][0]['media_url'])
                        if ('bitrate' in res['extended_entities']['media'][0]['video_info']['variants'][0]):
                            await message.channel.send('mp4形式です。')

                            await message.channel.send(res['extended_entities']['media'][0]['video_info']['variants'][0]['bitrate'])
                            print(res['extended_entities']['media'][0]['video_info']['variants'][0]['bitrate'])
                        else:
                            await message.channel.send('mp4形式ではありません。')
                            bit0 = 0
                            await message.channel.send(bit0)


                else:
                    log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：TwitterURLではなかったので、処理をスキップしました。'.format(message))
            else:
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：対象チャンネルではありません。'.format(message))
        '''
        if message.content.startswith('/daily'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            try:
                if os.path.exists('./Userdata/points/' + str(message.author.id) + '.txt'):
                    if os.path.exists('./Userdata/daily/' + str(message.author.id) + '.txt'):
                        await message.channel.send(':no_entry_sign: <@' + str(message.author.id) + '>よ。デイリーボーナスは一日一回までじゃ。また来るが良い。')
                        log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：既に獲得済みです。'.format(message))
                    else:
                        daily_point = random.randint(1, 999)
                        f = open('./Userdata/points/' + str(message.author.id) + '.txt', 'r')
                        file_point = f.readline()
                        file_point = int(file_point) + daily_point
                        f = open('./Userdata/points/' + str(message.author.id) + '.txt', 'w')
                        f.write(str(file_point))
                        f.close()
                        await message.channel.send(':tada: <@' + str(message.author.id) + '>がデイリーボーナスで' + str(daily_point) + 'WARPointを獲得しました。')
                        log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{1}ポイントを付与しました。'.format(message, str(daily_point)))
                        f = open('./Userdata/daily/' + str(message.author.id) + '.txt', 'w')
                        f.write(str(1))
                        f.close()
                else:
                    if os.path.exists('./Userdata/daily/' + str(message.author.id) + '.txt'):
                        await message.channel.send(':no_entry_sign: <@' + str(message.author.id) + '>よ。デイリーボーナスは一日一回までじゃ。また来るが良い。')
                        log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：既に獲得済みです。'.format(message))
                    else:
                        daily_point = random.randint(1, 999)
                        f = open('./Userdata/points/' + str(message.author.id) + '.txt', 'w')
                        f.write(str(daily_point))
                        f.close()
                        await message.channel.send(':tada: <@' + str(message.author.id) + '>がデイリーボーナスで' + str(daily_point) + 'WARPointを獲得しました。')
                        log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{1}ポイントを付与しました。'.format(message, str(daily_point)))
                        f = open('./Userdata/daily/' + str(message.author.id) + '.txt', 'w')
                        f.write(str(1))
                        f.close()
            except:
                await message.channel.send(':warning: エラーが発生しました。オーバーフローした可能性があります。')

        if message.content.startswith('/omikuji'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if os.path.exists('./Userdata/omikuji/{0.author.id}.txt'.format(message)):
                f = open('./Userdata/omikuji/{0.author.id}.txt'.format(message), 'r')
                file_omikuji = f.readline()
                if (int(file_omikuji) == 1):
                    await message.channel.send(':grinning: <@{0.author.id}>の今日の運勢は大吉！留年しないでしょう！'.format(message))
                elif (int(file_omikuji) == 2):
                    await message.channel.send(':sweat_smile: <@{0.author.id}>の今日の運勢は吉！ラッキーアイテムは金！'.format(message))
                elif (int(file_omikuji) == 3):
                    await message.channel.send(':tired_face: <@{0.author.id}>の今日の運勢は中吉！保存するチャンスが貰えないかも・・・？'.format(message))
                elif (int(file_omikuji) == 4):
                    await message.channel.send(':worried: <@{0.author.id}>の今日の運勢は小吉！プロジェクトファイルが消えるかも！？'.format(message))
                elif (int(file_omikuji) == 5):
                    await message.channel.send(':rage: <@{0.author.id}>の今日の運勢は凶！地獄に落ちろ！'.format(message))
            else:
                omikuji_result = random.randint(1, 5)
                if (omikuji_result == 1):
                    await message.channel.send(':grinning: <@{0.author.id}>の今日の運勢は大吉！留年しないでしょう！'.format(message))
                    f = open('./Userdata/omikuji/{0.author.id}.txt'.format(message), 'w')
                    f.write(str(1))
                    f.close()
                elif (omikuji_result == 2):
                    await message.channel.send(':sweat_smile: <@{0.author.id}>の今日の運勢は吉！ラッキーアイテムは金！'.format(message))
                    f = open('./Userdata/omikuji/{0.author.id}.txt'.format(message), 'w')
                    f.write(str(2))
                    f.close()
                elif (omikuji_result == 3):
                    await message.channel.send(':tired_face: <@{0.author.id}>の今日の運勢は中吉！保存するチャンスが貰えないかも・・・？'.format(message))
                    f = open('./Userdata/omikuji/{0.author.id}.txt'.format(message), 'w')
                    f.write(str(3))
                    f.close()
                elif (omikuji_result == 4):
                    await message.channel.send(':worried: <@{0.author.id}>の今日の運勢は小吉！プロジェクトファイルが消えるかも！？'.format(message))
                    f = open('./Userdata/omikuji/{0.author.id}.txt'.format(message), 'w')
                    f.write(str(4))
                    f.close()
                elif (omikuji_result == 5):
                    await message.channel.send(':rage: <@{0.author.id}>の今日の運勢は凶！地獄に落ちろ！'.format(message))
                    f = open('./Userdata/omikuji/{0.author.id}.txt'.format(message), 'w')
                    f.write(str(5))
                    f.close()

        if message.content.startswith('/うにさんルーレット'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            try:
                if os.path.exists('./Userdata/points/{0.author.id}.txt'.format(message)):
                    uni_rand = random.randint(1, 500)
                    if (uni_rand <= 250):
                        f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'r')
                        uni_points = f.readline()
                        uni_points = int(uni_points) * 2
                        f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'w')
                        f.write(str(uni_points))
                        f.close()
                        await message.channel.send(':confetti_ball: おめでとう！<@{0.author.id}>のWARPointは{1}Pointになった！'.format(message, uni_points))
                        log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：成功！{1}Pointになりました。'.format(message, uni_points))
                    else:
                        os.remove('./Userdata/points/{0.author.id}.txt'.format(message))
                        await message.channel.send(':stuck_out_tongue_winking_eye: 残念！ｗ<@{0.author.id}>のWARPointは0Pointになった！'.format(message))
                        log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：失敗！0Pointになりました。'.format(message))
                else:
                    await message.channel.send(':no_entry_sign: ポイントがありません！出直してこい')
                    log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：ポイントがありません。'.format(message))
            except:
                await message.channel.send(':warning: エラーが発生しました。オーバーフローした可能性があります。')

        if message.content.startswith('/バイオレントうにさんルーレット'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            try:
                if os.path.exists('./Userdata/points/{0.author.id}.txt'.format(message)):
                    uni_rand = random.randint(1, 100)
                    if (uni_rand == 45 or uni_rand == 48 or uni_rand == 64):
                        f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'r')
                        uni_points = f.readline()
                        uni_points = int(uni_points) * 100
                        f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'w')
                        f.write(str(uni_points))
                        f.close()
                        await message.channel.send(':confetti_ball: おめでとう！<@{0.author.id}>のWARPointは{1}Pointになった！'.format(message, uni_points))
                        log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：成功！{1}Pointになりました。'.format(message, uni_points))
                    else:
                        os.remove('./Userdata/points/{0.author.id}.txt'.format(message))
                        await message.channel.send(':stuck_out_tongue_winking_eye: 残念！ｗ<@{0.author.id}>のWARPointは0Pointになった！'.format(message))
                        log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：失敗！0Pointになりました。'.format(message))
                else:
                    await message.channel.send(':no_entry_sign: ポイントがありません！出直してこい')
                    log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：ポイントがありません。'.format(message))
            except:
                await message.channel.send(':warning: エラーが発生しました。オーバーフローした可能性があります。')

        if message.content.startswith('/say'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            try:
                if (message.channel.id == 498872353971765269):
                    say_command, say_mes, say_channel = message.content.split()
                    channel = client.get_channel(int(say_channel))
                    await channel.send(say_mes)
                else:
                    await message.channel.send('`Error : 対象のチャンネルではありません。`')
            except:
                await message.channel.send(':warning: エラーが発生しました。コマンドを間違えてないか再度確認してください。')

        if message.content.startswith('/dtm-odai'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            try:
                if (message.channel.id == 499236063265685505 or message.channel.id == 523452125515087872):
                    dtm_get = message.content
                    dtm_command, dtm_odai = dtm_get.split()
                    f = open('./Clientdata/odai/dtmodai.txt', 'a')
                    f.write(dtm_odai + '\n')
                    f.close()
                    await message.channel.send('限界DTM大会お題候補に`' + dtm_odai + '`が追加されました！')
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{1}が追加されました。'.format(message, dtm_odai))
                else:
                    await message.channel.send('`Error : 対象のチャンネルではありません。`')
                    log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name} : Error : 対象のチャンネルではありません。'.format(message))
            except:
                await message.channel.send(':warning: エラーが発生しました。コマンドを間違えてないか再度確認してください。')

        if message.content.startswith('/model-odai'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            try:
                if (message.channel.id == 499236063265685505 or message.channel.id == 523535877029494796):
                    model_get = message.content
                    model_command, model_odai = model_get.split()
                    f = open('./Clientdata/odai/modelodai.txt', 'a')
                    f.write(model_odai + '\n')
                    f.close()
                    await message.channel.send('限界モデリング大会お題候補に`' + model_odai + '`が追加されました！')
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{1}が追加されました。'.format(message, model_odai))
                else:
                    await message.channel.send(':no_entry_sign: このチャンネルでは実行できません。')
            except:
                await message.channel.send(':warning: エラーが発生しました。コマンドを間違えてないか再度確認してください。')

        if message.content.startswith('/design-odai'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if (message.channel.id == 499236063265685505 or message.channel.id == 523538511102738443):
                design_get = message.content
                design_command, design_odai = design_get.split()
                f = open('./Clientdata/odai/designodai.txt', 'a')
                f.write(design_odai + '\n')
                f.close()
                await message.channel.send('限界デザイン大会お題候補に`' + design_odai + '`が追加されました！')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{1}が追加されました。'.format(message, design_odai))
            elif (message.content.count(' ') != 1):
                await message.channel.send('`Error : コマンドの書き方が間違っています。`')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：コマンドの書き方が間違っています。'.format(message))
            else:
                await message.channel.send('`Error : 対象のチャンネルではありません。`')

        if message.content.startswith('/eizo-odai'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if (message.channel.id == 499236063265685505 and message.content.count(' ') == 1 or message.content.count('　') == 1 or message.channel.id == 523161114415071252 and message.content.count(' ') == 1 or message.content.count('　') == 1):
                eizo_get = message.content
                eizo_command, eizo_odai = eizo_get.split()
                f = open('./Clientdata/odai/eizoodai.txt', 'a')
                f.write(eizo_odai + '\n')
                f.close()
                await message.channel.send('映像大会お題候補に`' + eizo_odai + '`が追加されました！')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{1}が追加されました。'.format(message, eizo_odai))
            elif (message.content.count(' ') != 1):
                await message.channel.send('`Error : コマンドの書き方が間違っています。`')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：コマンドの書き方が間違っています。'.format(message))
            else:
                await message.channel.send('`Error : 対象のチャンネルではありません。`')

        if message.content.startswith('/give-point'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            give_get = message.content
            give_command, give_user, give_points = give_get.split()
            if (message.author.id == 227375367990542338):
                if os.path.exists('./Userdata/points/{0}.txt'.format(give_user)):
                    f = open('./Userdata/points/{0}.txt'.format(give_user), 'r')
                    war_points = f.readline()
                    war_points = int(war_points) + int(give_points)
                    f = open('./Userdata/points/{0}.txt'.format(give_user), 'w')
                    f.write(str(war_points))
                    f.close()
                    await message.channel.send('`info：`<@{0}>`に{1}Pointを付与しました。`'.format(give_user, give_points))
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} to {1}：{2}Point付与しました。'.format(message, give_user, give_points))
                else:
                    f = open('./Userdata/points/{0}.txt'.format(give_user), 'w')
                    f.write(str(give_points))
                    f.close()
                    await message.channel.send('`info：`<@{0}>`に{1}Pointを付与しました。`'.format(give_user, give_points))
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} to {1}：{2}Point付与しました。'.format(message, give_user, give_points))
            else:
                await message.channel.send('`Error : 開発者コマンドです。`')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：開発者コマンドです。'.format(message, give_points))

        if message.content.startswith('/war'):
            await message.channel.send('開　戦')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/画面共有'):
            try:
                await message.channel.send('https://discordapp.com/channels/{0}/{1}'.format(message.channel.guild.id, message.author.voice.channel.id))
            except:
                await message.channel.send(':cold_sweat: リンクの取得に失敗しました。通話に入っているか確認し、もう一度実行してください。')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/sw-start'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if os.path.exists('./Userdata/timer/{0.author.id}.txt'.format(message)):
                await message.channel.send(':no_entry_sign: ストップウォッチは既に開始されています。')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：ストップウォッチは既に開始されています。'.format(message))
            else:
                timer_now = datetime.datetime.now()
                f = open('./Userdata/timer/{0.author.id}.txt'.format(message), 'w')
                f.write(timer_now.strftime('%Y-%m-%d %H:%M:%S'))
                f.close()
                await message.channel.send(':stopwatch: <@{0.author.id}>のストップウォッチを開始しました。'.format(message))
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ストップウォッチを開始しました。'.format(message))

        if message.content.startswith('/sw-check'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if os.path.exists('./Userdata/timer/{0.author.id}.txt'.format(message)):
                f = open('./Userdata/timer/{0.author.id}.txt'.format(message), 'r')
                timer_file = f.readline()
                f.close()
                timer_format = '%Y-%m-%d %H:%M:%S'
                timer_now = datetime.datetime.now()
                timer_delta = datetime.datetime.strptime(timer_now.strftime('%Y-%m-%d %H:%M:%S'), timer_format) - datetime.datetime.strptime(timer_file, timer_format)
                timer_minute = divmod(timer_delta.seconds, 60)
                await message.channel.send(':stopwatch: <@{0.author.id}>の経過時間は{1}分{2}秒'.format(message, int(timer_minute[0]), int(timer_minute[1])))
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：経過時間は{1}分{2}秒'.format(message, int(timer_minute[0]), int(timer_minute[1])))
            else:
                await message.channel.send(':no_entry_sign: ストップウォッチを開始してください。')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：ストップウォッチが開始されていません。'.format(message))

        if message.content.startswith('/sw-stop'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if os.path.exists('./Userdata/timer/{0.author.id}.txt'.format(message)):
                f = open('./Userdata/timer/{0.author.id}.txt'.format(message), 'r')
                timer_file = f.readline()
                f.close()
                timer_format = '%Y-%m-%d %H:%M:%S'
                timer_now = datetime.datetime.now()
                timer_delta = datetime.datetime.strptime(timer_now.strftime('%Y-%m-%d %H:%M:%S'), timer_format) - datetime.datetime.strptime(timer_file, timer_format)

                timer_minute = divmod(timer_delta.seconds, 60)
                await message.channel.send(':stopwatch: <@{0.author.id}>の経過時間は{1}分{2}秒でした。'.format(message, int(timer_minute[0]), int(timer_minute[1])))
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：経過時間は{1}分{2}秒'.format(message, int(timer_minute[0]), int(timer_minute[1])))
            else:
                await message.channel.send(':no_entry_sign: ストップウォッチを開始してください。')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：ストップウォッチが開始されていません。'.format(message))

        if message.content.startswith('/sw-end'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if os.path.exists('./Userdata/timer/{0.author.id}.txt'.format(message)):
                f = open('./Userdata/timer/{0.author.id}.txt'.format(message), 'r')
                timer_file = f.readline()
                f.close()
                timer_format = '%Y-%m-%d %H:%M:%S'
                timer_now = datetime.datetime.now()
                timer_delta = datetime.datetime.strptime(timer_now.strftime('%Y-%m-%d %H:%M:%S'), timer_format) - datetime.datetime.strptime(timer_file, timer_format)
                timer_minute = divmod(timer_delta.seconds, 60)
                os.remove('./Userdata/timer/{0.author.id}.txt'.format(message))
                await message.channel.send(':stopwatch: <@{0.author.id}>のストップウォッチを終了しました。経過時間は{1}分{2}秒'.format(message, int(timer_minute[0]), int(timer_minute[1])))
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ストップウォッチを終了しました。経過時間は{1}分{2}秒'.format(message, int(timer_minute[0]), int(timer_minute[1])))
            else:
                await message.channel.send(':no_entry_sign: ストップウォッチを開始してください。')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：ストップウォッチが開始されていません。'.format(message))

        if message.content.startswith('/get-pixelsort'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            pixelsort_command, pixelsort_url, pixelsort_option, pixelsort_mode = message.content.split()
            gyazo = Api(access_token='*')
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(pixelsort_url,'pixelsort.png')
            img = Image.open('pixelsort.png')
            img_width,img_height = img.size
            if img_width > 1280:
                resize_height = 1280 / img_width * img_height
                img = img.resize((int(1280),int(resize_height)))
                img.save('pixelsort_after.png')
                os.remove('pixelsort.png')
                os.rename('pixelsort_after.png', 'pixelsort.png')
            for pixelsort_imgname in glob.iglob('pixelsort.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。実行します。`'.format(pixelsort_imgname))
            subprocess.call("python .\pixelsort\pixelsort.py pixelsort.png -a {0} -t 0 -u {1}".format(pixelsort_option, pixelsort_mode), shell=True)
            img.close()
            os.remove('{0}'.format(pixelsort_imgname))
            for pixelsort_imgname in glob.iglob('*.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。アップします。`'.format(pixelsort_imgname))
            with open(pixelsort_imgname, 'rb') as f:
                image = gyazo.upload_image(f)
            await message.channel.send(image.permalink_url)
            os.remove('{0}'.format(pixelsort_imgname))

        if message.content.startswith('/get-resize'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            resize_command, resize_url, resize_size = message.content.split()
            gyazo = Api(access_token='*')
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(resize_url,'resize.png')
            img = Image.open('resize.png')
            img_width,img_height = img.size
            resize_height = int(resize_size) / img_width * img_height
            if int(resize_height) <= 0:
                await message.channel.send('`Error : サイズが小さすぎます`')
            else:
                img = img.resize((int(resize_size),int(resize_height)))
                img.save('resize_after.png')
                img.close()
                os.remove('resize.png')
                os.rename('resize_after.png', 'resize.png')
                with open('resize.png', 'rb') as f:
                    image = gyazo.upload_image(f)
                await message.channel.send(image.permalink_url)
                os.remove('{0}'.format('resize.png'))

        if message.content.startswith('/get-sym'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            sym_command, sym_url, sym_option = message.content.split()
            gyazo = Api(access_token='*')
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(sym_url,'sym.png')
            img = Image.open('sym.png')
            img_width,img_height = img.size
            if img_width > 1280:
                resize_height = 1280 / img_width * img_height
                img = img.resize((int(1280),int(resize_height)))
                img.save('sym_after.png')
                os.remove('sym.png')
                os.rename('sym_after.png', 'sym.png')
            for pixelsort_imgname in glob.iglob('sym.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。実行します。`'.format(pixelsort_imgname))
            img.close()
            if sym_option == '1':
                img = Image.open('sym.png')
                tmp1 = img.crop((0, 0, img.size[0] // 2, img.size[1]))
                tmp2 = ImageOps.mirror(tmp1)
                dst = Image.new('RGB', (tmp1.width + tmp2.width, tmp1.height))
                dst.paste(tmp1, (0, 0))
                dst.paste(tmp2, (tmp1.width, 0))
                dst.save('upload.png')
                os.remove('{0}'.format(pixelsort_imgname))
            else:
                img = Image.open('sym.png')
                tmp2 = img.crop((img.size[0] // 2, 0, img.size[0], img.size[1]))
                tmp1 = ImageOps.mirror(tmp2)
                dst = Image.new('RGB', (tmp1.width + tmp2.width, tmp1.height))
                dst.paste(tmp1, (0, 0))
                dst.paste(tmp2, (tmp1.width, 0))
                dst.save('upload.png')
                os.remove('{0}'.format(pixelsort_imgname))
            for pixelsort_imgname in glob.iglob('*.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。アップします。`'.format(pixelsort_imgname))
            with open(pixelsort_imgname, 'rb') as f:
                image = gyazo.upload_image(f)
            await message.channel.send(image.permalink_url)
            os.remove('{0}'.format(pixelsort_imgname))

        if message.content.startswith('/get-reverse'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            rv_command, rv_url = message.content.split()
            gyazo = Api(access_token='*')
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(rv_url,'rv.png')
            img = Image.open('rv.png')
            img_width,img_height = img.size
            if img_width > 1280:
                resize_height = 1280 / img_width * img_height
                img = img.resize((int(1280),int(resize_height)))
                img.save('rv_after.png')
                os.remove('rv.png')
                os.rename('rv_after.png', 'rv.png')
            for pixelsort_imgname in glob.iglob('rv.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。実行します。`'.format(pixelsort_imgname))
            img.close()
            img = Image.open('rv.png')
            img_array = 255 - np.array(img)
            Image.fromarray(img_array).save('upload.png')
            os.remove('{0}'.format(pixelsort_imgname))
            for pixelsort_imgname in glob.iglob('*.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。アップします。`'.format(pixelsort_imgname))
            with open(pixelsort_imgname, 'rb') as f:
                image = gyazo.upload_image(f)
            await message.channel.send(image.permalink_url)
            os.remove('{0}'.format(pixelsort_imgname))

        if message.content.startswith('/get-color'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            color_command, color_url, color_option = message.content.split()
            gyazo = Api(access_token='*')
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(color_url,'color.png')
            img = Image.open('color.png')
            img_width,img_height = img.size
            if img_width > 1280:
                resize_height = 1280 / img_width * img_height
                img = img.resize((int(1280),int(resize_height)))
                img.save('color_after.png')
                os.remove('color.png')
                os.rename('color_after.png', 'color.png')
                img.close()
            for pixelsort_imgname in glob.iglob('color.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。実行します。`'.format(pixelsort_imgname))
            img.close()
            if color_option == '1':
                img = Image.open('color.png')
                img2 = Image.open('./Clientdata/image/color_blue.png')
                img_width,img_height = img.size
                img2 = img2.resize((int(img_width),int(img_height)))
                img2.save('color_blue2.png')
                img.close()
                img2.close()
                color_img1 = cv2.imread('color.png')
                color_img2 = cv2.imread('color_blue2.png')
                color_result = cv2.addWeighted(color_img1, 0.5, color_img2, 0.3, 2.2)
                color_result = cv2.addWeighted(color_result, 0.8, color_img1, 0.2, 2.2)
                cv2.imwrite('color_upload.png', color_result)
                os.remove('color.png')
                os.remove('color_blue2.png')
            elif color_option == '2':
                img = Image.open('color.png')
                img2 = Image.open('./Clientdata/image/color_cha.png')
                img3 = Image.open('./Clientdata/image/color_light.png')
                img_width,img_height = img.size
                img2 = img2.resize((int(img_width),int(img_height)))
                img3 = img3.resize((int(img_width),int(img_height)))
                img2.save('color_cha2.png')
                img3.save('color_light3.png')
                img.close()
                img2.close()
                img3.close()
                color_img1 = cv2.imread('color.png')
                color_img2 = cv2.imread('color_cha2.png')
                color_img3 = cv2.imread('color_light3.png')
                color_result = cv2.addWeighted(color_img1, 0.6, color_img2, 0.2, 2.2)
                color_result = cv2.addWeighted(color_result, 0.5, color_img3, 0.7, 1.0)
                cv2.imwrite('color_upload.png', color_result)
                os.remove('color.png')
                os.remove('color_cha2.png')
                os.remove('color_light3.png')
            else:
                img = Image.open('color.png')
                img2 = Image.open('./Clientdata/image/color_cha.png')
                img_width,img_height = img.size
                img2 = img2.resize((int(img_width),int(img_height)))
                img2.save('color_cha2.png')
                img.close()
                img2.close()
                color_img1 = cv2.imread('color.png')
                color_img2 = cv2.imread('color_cha2.png')
                color_result = cv2.addWeighted(color_img1, 0.5, color_img2, 0.3, 2.2)
                color_result = cv2.addWeighted(color_result, 0.8, color_img1, 0.2, 2.2)
                cv2.imwrite('color_upload.png', color_result)
                os.remove('color.png')
                os.remove('color_cha2.png')
            for pixelsort_imgname in glob.iglob('color_upload.png'):
                await message.channel.send('`info : {0} ファイルを確認しました。アップします。`'.format(pixelsort_imgname))
            with open(pixelsort_imgname, 'rb') as f:
                image = gyazo.upload_image(f)
            await message.channel.send(image.permalink_url)
            os.remove('{0}'.format(pixelsort_imgname))

        if message.content.startswith('/help'):
            await message.channel.send('https://apps.m86.work/warbot/')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        '''
        if message.content.startswith('/get-twitter'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            consumer = oauth2.Consumer(key='*', secret='*')
            twiclient = oauth2.Client(consumer)
            resp, twicontent = twiclient.request("https://api.twitter.com/oauth/request_token", "GET")
            twistr = twicontent.decode('utf-8')
            list = [t.split() for t in twistr.split("&")]
            d = ({})
            for t in list:
                a = t[0].split("=")
                d.update({ a[0] : a[1] }) # dの中身は文字列
            print("■tokenを辞書化")
            print(d)
            print("----")
            url = "https://api.twitter.com/oauth/authorize?oauth_token=" + d['oauth_token']
            twitter_dmuser = client.get_user(message.author.id)
            twitter_createdm = await twitter_dmuser.create_dm()
            await twitter_createdm.send('認証URL：{0}\n有効期限は30秒です。'.format(url))
            pin = [1]
            def check(m):
                pin[0] = m.content
                return m.content.isdecimal() == True and m.channel == twitter_createdm
            try:
                msg = await client.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await twitter_createdm.send('認証期限が切れました。再度認証してください。')
            else:
                await twitter_createdm.send('OK')
                pin = pin[0]
                otoken = d["oauth_token"].encode('utf-8')
                otsecret = d["oauth_token_secret"].encode('utf-8')
                print("■設定するやつ")
                print("・oauth token: ")
                print(otoken)
                print("・oauth token secret: ")
                print(otsecret)
                print("--")
                # Tokenを取得する
                token = oauth2.Token(otoken, otsecret)
                twiclient = oauth2.Client(consumer, token)
                resp, twicontent = twiclient.request("https://api.twitter.com/oauth/access_token", "POST", body="oauth_verifier={0}".format(pin))
                print(twicontent)
                print(resp)
                twistr = twicontent.decode('utf-8')
                list = [t.split() for t in twistr.split("&")]
                oauthToken = ({})
                for t in list:
                    a = t[0].split("=")
                    oauthToken.update({ a[0] : a[1] }) # dの中身は文字列
                #twitter = Twython(APP_KEY, APP_SECRET, oauthToken['oauth_token'], oauthToken['oauth_token_secret'])
                await twitter_createdm.send('アクセストークン：{0}\nアクセスシークレット：{1}'.format(oauthToken['oauth_token'], oauthToken['oauth_token_secret']))
        '''

        if message.content.startswith('/get-boturl'):
            await message.channel.send('https://discordapp.com/api/oauth2/authorize?client_id=473006066116984842&permissions=8&scope=bot')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/Naki'):
            await message.channel.send('Nakiました')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/donate'):
            await message.channel.send('https://dev.m86.work/donate/')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/PixelSort'):
            await message.channel.send('キレました')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/pixelsort'):
            await message.channel.send('キレました')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/ナダル'):
            await message.channel.send('可～～\nhttps://i.gyazo.com/fc57d30663eb33094f272c5545df5239.png')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/心'):
            await message.channel.send('寺田は好きだけど心が嫌い。')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/コッシュ'):
            await message.channel.send('ハイパボリックコサイン')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('こんばんWAR'):
            await message.channel.send('開　戦！{0.author.name}さん！今夜も開　戦が綺麗ですね！'.format(message))
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/open'):
            await message.channel.send('開　栓')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/ocean'):
            await message.channel.send('海　戦')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/wifi'):
            await message.channel.send('回　線')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/seafood'):
            await message.channel.send('海　鮮')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/th3_n00b13'):
            await message.channel.send('壊れちゃった・・・')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('うんちして'):
            await message.channel.send('ぶり！')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/高知判定'):
            await message.channel.send('https://twitter.com/seldo0607/status/1072848226267484161')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/changelog'):
            await message.channel.send('https://apps.m86.work/warbot/changelog.html')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/被写界深度'):
            await message.channel.send('被写界深度 ひー社会しんど')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/マイクラ'):
            #await message.channel.send('オンライン状況を確認できます:https://genkaivillage.aternos.me/')
            await message.channel.send(':no_entry_sign: このコマンドは廃止されました。')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/ゆるキャン'):
            await message.channel.send('わろてる場合カーッ')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/twitterやめろ'):
            await message.channel.send('https://cdn.discordapp.com/attachments/464804212136607744/476419941516443690/1533342254425.png')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/ジョウタ'):
            await message.channel.send('ｱ､ｿｯｶｧ.....')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/人生どうでも飯田橋'):
            await message.channel.send('人生どうでも飯田橋！w')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/しぬキャン'):
            await message.channel.send('https://cdn.discordapp.com/attachments/465062712863490049/532917977998163978/unknown.png')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/ゴフィ'):
            await message.channel.send('https://godfield.net/')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/クランカー'):
            await message.channel.send('https://krunker.io')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/そんなものはない'):
            await message.channel.send('https://cdn.discordapp.com/attachments/464804212136607744/531449192758116372/unknown.png')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/魔剤'):
            await message.channel.send('https://bit.ly/2MplBPo')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/SELDOルーレット'):
            await message.channel.send('`Error : んなもんねぇよ人生やり直せ`')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/4am'):
            await message.channel.send('おはよう！朝4時に何してるんだい？')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/redpoints'):
            redpoint = random.randint(1, 500)
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if redpoint <= 250:
                await message.channel.send('赤点回避！')
            else:
                await message.channel.send('赤点！オワタ！ア"（圧死）')

        '''
        if message.content.startswith('/抱負'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if os.path.exists('./Userdata/houfu/{0.author.name}.txt'.format(message)):
                await message.channel.send('`info : すでに抱負が投稿されています。`')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：すでに抱負が投稿されています。'.format(message))
            elif (message.content.count(' ') == 1 or message.content.count('　') == 1):
                houfu_get = message.content
                houfu_command, houfu_main = houfu_get.split()
                f = open('./Userdata/houfu/{0.author.name}.txt'.format(message), 'a')
                f.write(houfu_main)
                f.close()
                await message.channel.send('`info：抱負を投稿しました ' + houfu_main + '`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：抱負を投稿しました。{1}'.format(message, houfu_main))
            else:
                await message.channel.send('`Error : コマンドの書き方が間違っています。`')
                log_client.warning('{0.author.name} at {0.guild.name} in {0.channel.name}：コマンドの書き方が間違っています。'.format(message))
        '''

        if message.content.startswith('やったぜ'):
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if os.path.exists('./Userdata/points/{0.author.id}.txt'.format(message)):
                f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'r')
                war_points = f.readline()
                if message.author.id == 330285385504784386:
                    war_points = int(war_points) + 10
                elif message.author.id == 448894953490481165:
                    war_points = int(war_points) + 100000000000
                else:
                    war_points = int(war_points) + 1
                f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'w')
                f.write(str(war_points))
                f.close()
                await message.channel.send('`info：`<@{0.author.id}>`のWARPointは{1}Pointです。`'.format(message, war_points))
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{1}Pointになりました。'.format(message, war_points))
            else:
                f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'w')
                if message.author.id == 330285385504784386:
                    f.write(str(10))
                    f.close()
                    await message.channel.send('`info：`<@{0.author.id}>`のWARPointは10Pointです。`'.format(message))
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：10Pointになりました。'.format(message))
                elif message.author.id == 448894953490481165:
                    f.write(str(100000000000))
                    f.close()
                    await message.channel.send('`info：`<@{0.author.id}>`のWARPointは100000000000Pointです。`'.format(message))
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：100000000000Pointになりました。'.format(message))
                else:
                    f.write(str(1))
                    f.close()
                    await message.channel.send('`info：`<@{0.author.id}>`のWARPointは1Pointです。`'.format(message))
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：1Pointになりました。'.format(message))

        if message.content.startswith('/get-id'):
            await message.channel.send(str(message.author.id))
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/day-reset'):
            if (message.channel.id == 498872353971765269):
                shutil.rmtree('Userdata/daily')
                os.mkdir('Userdata/daily')
                shutil.rmtree('Userdata/omikuji')
                os.mkdir('Userdata/omikuji')
                await message.channel.send('デイリーデータを削除しました。')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：デイリーデータが削除されました。'.format(message))
            else:
                await message.channel.send('`Error : 対象のチャンネルではありません。`')
                log_client.warning('対象のチャンネルではありません。')

        if message.content.startswith('/easy'):
            easy_mes = message.content
            command, easy_nage , easy_akirame = easy_mes.split()
            await message.channel.send(easy_nage + '投げ出してもいいじゃないの？Used to be ' + easy_akirame + 'は easy')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/人とフレアえない'):
            await message.channel.send('https://twitter.com/yarita_cc/status/1051390172074373120')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/now'):
            await message.channel.send('現在時刻：' + str(datetime.datetime.now()))
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))

        if message.content.startswith('/北京'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error : やたらめったら北京`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/yatara.mp3'))
                await asyncio.sleep(3)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/チャレンジ北京'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error : やたらめったら北京`')
                await message.channel.send(message.author.voice.channel)
                try:
                    play_vc = await message.author.voice.channel.connect()
                except:
                    print('a')
                play_vc.play(discord.FFmpegPCMAudio('Clientdata/audio/yatara.mp3'))
                time = random.uniform(0, 2)
                print(time)
                sleep(time)
                await play_vc.disconnect(force=False)
                await message.channel.send('`info : 実行時間は{0}秒でした。`'.format(time))
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/除夜の鐘'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                f = open('./Clientdata/zyoya/count.txt', 'r')
                zyoya_file = f.readline()
                zyoya_count = int(zyoya_file) + 1
                f = open('./Clientdata/zyoya/count.txt', 'w')
                f.write(str(zyoya_count))
                f.close()
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：除夜の鐘{1}回目'.format(message, zyoya_count))
                await message.channel.send('`info : 除夜の鐘を鳴らしています。{0}回目`'.format(zyoya_count))
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/zyoya.mp3'))
                await asyncio.sleep(4)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/鈴'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`info : 鈴を鳴らしています。`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/bell.mp3'))
                await asyncio.sleep(4)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/爆破'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`info : 爆破します。`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/bakuhatu.mp3'))
                await asyncio.sleep(5)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/Minato86'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`info : やたらめったらみなと`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/yatamina.mp3'))
                await asyncio.sleep(3)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/disconnect'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`切断処理をします。`')
                vcid = message.author.voice.channel
                channel = discord.VoiceChannel
                play_vc = await channel.disconnect(vcid)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/Minato北京'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`info : 北京化`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/yataminapekin.mp3'))
                await asyncio.sleep(3)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('$t'):
            await message.channel.send(':no_entry_sign: このコマンドは廃止されました。')
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}廃止されたコマンドです。'.format(message))

        if message.content.startswith('/賽銭'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                if os.path.exists('./Userdata/points/{0.author.id}.txt'.format(message)):
                    f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'r')
                    saisen_file = f.readline()
                    f.close()
                    saisen_point = int(saisen_file) - 1
                    if (saisen_point <= 0):
                        os.remove('./Userdata/points/{0.author.id}.txt'.format(message))
                    else:
                        f = open('./Userdata/points/{0.author.id}.txt'.format(message), 'w')
                        f.write(str(saisen_point))
                        f.close()
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{1}Pointになりました。'.format(message, saisen_point))
                    await message.channel.send('`info : 賽銭しました。残り{0}Point`'.format(saisen_point))
                    channel = message.author.voice.channel
                    play_vc = await channel.connect()
                    play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/saisen.mp3'))
                    await asyncio.sleep(2)
                    await play_vc.disconnect(force=False)
                else:
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                    await message.channel.send('`Error：ポイントがありません。`')
                    log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ポイントがありません。'.format(message))
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/チャレンジ除夜の鐘'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                f = open('./Clientdata/zyoya/count.txt', 'r')
                zyoya_file = f.readline()
                zyoya_count = int(zyoya_file) + 1
                f = open('./Clientdata/zyoya/count.txt', 'w')
                f.write(str(zyoya_count))
                f.close()
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：除夜の鐘{1}回目'.format(message, zyoya_count))
                await message.channel.send('`info : 除夜の鐘を鳴らしています。{0}回目`'.format(zyoya_count))
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/zyoya.mp3'))
                time = random.uniform(0, 3.2)
                print(time)
                await asyncio.sleep(time)
                await play_vc.disconnect(force=False)
                await message.channel.send('`info : 実行時間は{0}秒でした。`'.format(time))
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/セライア'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error : ない！ｗ`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/nai.mp3'))
                await asyncio.sleep(3)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/チャレンジセライア'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error : ない！ｗ`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/nai.mp3'))
                time = random.uniform(0, 3)
                print(time)
                await asyncio.sleep(time)
                await play_vc.disconnect(force=False)
                await message.channel.send('`info : 実行時間は{0}秒でした。`'.format(time))
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/ソ連ない'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error : ソ連ない！ｗ`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/naiyo.mp3'))
                await asyncio.sleep(5)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/セランダ'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                reply = '`Error : やたらめったらきんたろう`'
                await message.channel.send(reply)
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/yata.mp3'))
                await asyncio.sleep(3)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/オランダ'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`マイク買った！ｗ`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/maikukatta.mp3'))
                await asyncio.sleep(4)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/チャレンジオランダ'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`マイク買った！ｗ`')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/maikukatta.mp3'))
                time = random.uniform(0, 4)
                print(time)
                await asyncio.sleep(time)
                await play_vc.disconnect(force=False)
                await message.channel.send('`info : 実行時間は{0}秒でした。`'.format(time))
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/クソ過疎'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('クソ過疎死ね')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/seru.mp3'))
                await asyncio.sleep(13)
                await play_vc.disconnect(force=False)
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/チャレンジクソ過疎'):
            if (message.author.voice != None):
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name} vc {0.author.voice.channel}：{0.content}が実行されました。'.format(message))
                await message.channel.send('クソ過疎死ね')
                channel = message.author.voice.channel
                play_vc = await channel.connect()
                play_vc.play(discord.FFmpegPCMAudio('./Clientdata/audio/seru.mp3'))
                time = random.uniform(0, 13)
                print(time)
                await asyncio.sleep(time)
                await play_vc.disconnect(force=False)
                await message.channel.send('`info : 実行時間は{0}秒でした。`'.format(time))
            else:
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
                await message.channel.send('`Error：ボイスチャンネルに入っていません。`')
                log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：ボイスチャンネルに入っていません。'.format(message))

        if message.content.startswith('/calc'):
            calc_get = message.content
            calc_command, calc_x, calc_symbol, calc_y = calc_get.split()
            log_client.info('{0.author.name} at {0.guild.name} in {0.channel.name}：{0.content}が実行されました。'.format(message))
            if (calc_symbol == '+'):
                calc_result = float(calc_x) + float(calc_y)
                await message.channel.send('`結果は' + str(calc_result) + 'です`')
            elif (calc_symbol == '-'):
                calc_result = float(calc_x) - float(calc_y)
                await message.channel.send('`結果は' + str(calc_result) + 'です`')
            elif (calc_symbol == '*'):
                calc_result = float(calc_x) * float(calc_y)
                await message.channel.send('`結果は' + str(calc_result) + 'です`')
            elif (calc_symbol == '/'):
                if (calc_y == '0'):
                    await message.channel.send('`Error : 0で割ることはできません。`')
                else:
                    calc_result = float(calc_x) / float(calc_y)
                    await message.channel.send('`結果は' + str(calc_result) + 'です`')
            else:
                await message.channel.send('`Error : 対応していない形式です。`')

client = MyClient()
client.run('*')
