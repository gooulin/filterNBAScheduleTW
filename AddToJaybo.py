#coding=utf-8
import os
import time
import datetime
from send_post import *
import json,httplib

"""
Parameter example

year = '2016'

teams = {

'籃網':'', #channel ID
'勇士':'',
'騎士':'',
'馬刺':''

}

schedule = [

'騎士- 10/26(三)7:30尼克VS騎士，緯來體育、愛爾達體育(重播)VL:隔天0230 ELTA:2400，下一場11/4(五)',
'勇士- 10/26(三)10:30馬刺VS勇士，緯來體育(重播)隔天1030，下一場10/29(六)',
'勇士- 10/29(六)9:30勇士VS鵜鶘，FOX 2(重播1630/1855，下一場10/31(一)',
'馬刺- 10/26(三)10:30馬刺VS勇士，緯來體育(重播)隔天1030，下一場11/6(日)',
'籃網- 10/27(四)7:30籃網VS塞爾蒂克，緯來體育(重播)隔天0300/0800，下一場10/29(六)',
'籃網- 10/29(六)7:30溜馬VS籃網，緯來體育、愛爾達體育(重播)VL:1030 ELTA:2130，下一場10/30(日)',
'籃網- 10/30(日)8:00籃網VS公鹿，緯來體育(重播)2130，下一場11/1(二)'

]
"""
year = '2016'

teams = {

'籃網':'',
'勇士':'',
'騎士':'',
'馬刺':''

}

schedule = [

'騎士- 10/26(三)7:30尼克VS騎士，緯來體育、愛爾達體育(重播)VL:隔天0230 ELTA:2400，下一場11/4(五)',
'勇士- 10/26(三)10:30馬刺VS勇士，緯來體育(重播)隔天1030，下一場10/29(六)',
'勇士- 10/29(六)9:30勇士VS鵜鶘，FOX 2(重播)1630/1855，下一場10/31(一)',
'馬刺- 10/26(三)10:30馬刺VS勇士，緯來體育(重播)隔天1030，下一場11/6(日)',
'籃網- 10/27(四)7:30籃網VS塞爾蒂克，緯來體育(重播)隔天0300/0800，下一場10/29(六)',
'籃網- 10/29(六)7:30溜馬VS籃網，緯來體育、愛爾達體育(重播)VL:1030 ELTA:2130，下一場10/30(日)',
'籃網- 10/30(日)8:00籃網VS公鹿，緯來體育(重播)2130，下一場11/1(二)'

]

date_cnt = {}

for team in teams.keys():
	for index in range(0,len(schedule)):
		game = schedule[index]
		game_team = game.split('-')[0]
		if team == game_team:
			month = game.split(' ')[1].split('/')[0]
			date = game.split('/')[1].split('(')[0]
			key = month + '/' + date
			#當天場次若有多場發通知要間隔五分鐘，計算當天有幾場要發
			if key not in date_cnt.keys():
				date_cnt[key] = 1
			else:
				date_cnt[key] = date_cnt[key] + 1
			#發的時間為前一天的18:01因為UTC所以要扣8hr
			firetime_str = '2016-' + month + '-' + date + ' 18:01:00.000'
			print firetime_str
			fire_datetime = datetime.datetime.strptime(firetime_str, "%Y-%m-%d %H:%M:%S.%f")
			timestamp = time.mktime(fire_datetime.timetuple()) * 1000 + fire_datetime.microsecond / 1000
			#昨天：24 * 3600 * 1000
			#多場，間隔五分鐘：5 * 60 * 1000 * (date_cnt[key] - 1)
			fire_timestamp = timestamp - 24 * 3600 * 1000 + 5 * 60 * 1000 * (date_cnt[key] - 1)
			# online timestamp converter
			#http://www.epochconverter.com/
			print fire_timestamp
			if '緯來體育' in game:
				btnLink = 'http://sport.videoland.com.tw/chn/jc.asp'
				btnText = '緯來體育'
			elif '愛爾達體育' in game:
				btnLink = 'http://www.elta.tv/hd/program.php'
				btnText = '愛爾達體育'
			elif 'FOX' in game:
				btnLink = 'http://www.foxsportsasia.com/zh-tw/tv-listing/'
				btnText = 'FOX'
			#imageUrl = "http://www.cwb.gov.tw/V7/prevent/warning/Data/B20.gif?" + 'time=' + datetime.datetime.now().strftime('%d%H%M')
			d = {
			            "title": game,
			            "isNotify": True,
			            "onTop": False,
			            "isSchedule": True,
			            "fireTime": fire_timestamp,
			            "isADCandidate": False,
			            "content": "",
			            "hasQrcode": False,
			            "btnText": btnText,
			            "btnLink": btnLink,
			            "youtube": "",
			            "imgUrl": ""
			         }

			sendPost("api-jaybo.parseapp.com","",d,teams[team])
print date_cnt

