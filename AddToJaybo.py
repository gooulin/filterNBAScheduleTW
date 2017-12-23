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

'籃網- 12/27(二)8:30黃蜂VS籃網，緯來體育(重播)，下一場12/29(四)',
'籃網- 12/29(四)9:00籃網VS公牛，緯來體育、愛爾達體育(重播)VL:ELTA:，下一場12/31(六)',
'籃網- 12/31(六)8:00籃網VS巫師，緯來體育(重播)，下一場1/3(二)',
'籃網- 1/3(二)8:30爵士VS籃網，緯來體育(重播)，下一場1/6(五)',
'籃網- 1/6(五)8:00籃網VS溜馬，緯來體育(重播)，下一場1/7(六)',
'籃網- 1/7(六)8:30騎士VS籃網，緯來體育、愛爾達體育(重播)VL:ELTA:，下一場/()',
'勇士- 12/26(一)3:30勇士VS騎士，緯來體育、愛爾達體育(重播)VL:ELTA:，下一場12/29(四)',
'勇士- 12/29(四)11:30暴龍VS勇士，緯來體育(重播)，下一場12/31(六)',
'勇士- 12/31(六)11:30小牛VS勇士，愛爾達體育、FOX 2(重播)ELTA:FOX2:，下一場1/5(四)',
'勇士- 1/5(四)11:30拓荒者VS勇士，緯來體育、愛爾達體育(重播)VL:ELTA:，下一場1/7(六)',
'勇士- 1/7(六)11:30灰熊VS勇士，FOX 2(重播)，下一場/()',
'騎士- 12/26(一)3:30勇士VS騎士，緯來體育、愛爾達體育(重播)VL:ELTA:，下一場12/30(五)',
'騎士- 12/30(五)9:00塞爾蒂克VS騎士，緯來體育(重播)，下一場1/7(六)',
'騎士- 1/7(六)8:30騎士VS籃網，緯來體育、愛爾達體育(重播)VL:ELTA:，下一場/()'

]
"""
year = '2016'

teams = {

'籃網':'jDXuYbpFT8',
'勇士':'HaH36EdH2L',
'騎士':'pAOaO0I4nX',
'馬刺':'Uzef3V5wYO'

}

schedule = [

'勇士- 12/26(二)11:30 D-LIVE 騎士VS勇士，LINE、緯來體育(重播)VL:2230，下一場12/28(四)',
'勇士- 12/28(四)11:30爵士VS勇士，LINE、緯來體育、愛爾達體育(重播)LINE:1630 VL:2300 ELTA:1930，下一場12/30(六)',
'勇士- 12/30(六)11:30黃蜂VS勇士，緯來體育(重播)2100，下一場12/31(日)',
'勇士- 12/31(日)9:30灰熊VS勇士，緯來體育(重播)2100，下一場1/5(五)',

'騎士- 12/26(二)11:30 D-LIVE 騎士VS勇士，LINE、緯來體育(重播)VL:2230，下一場12/31(日)',
'騎士- 12/31(日)9:00騎士VS爵士，愛爾達體育(重播)1930，下一場1/3(三)'
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
			firetime_str = '2018-' + month + '-' + date + ' 21:01:00.000'
			print firetime_str
			fire_datetime = datetime.datetime.strptime(firetime_str, "%Y-%m-%d %H:%M:%S.%f")
			timestamp = time.mktime(fire_datetime.timetuple()) * 1000 + fire_datetime.microsecond / 1000
			#昨天：24 * 3600 * 1000
			#多場，間隔五分鐘：5 * 60 * 1000 * (date_cnt[key] - 1)
			fire_timestamp = timestamp - 24 * 3600 * 1000 + 5 * 60 * 1000 * (date_cnt[key] - 1)
			# online timestamp converter
			#http://www.epochconverter.com/
			btnText = ''
			btnLink = ''
			print fire_timestamp
			if '緯來體育' in game:
				btnLink = 'http://sport.videoland.com.tw/chn/jc.asp'
				btnText = '緯來體育'
			elif '愛爾達體育' in game:
				btnLink = 'http://www.elta.tv/hd/program.php'
				btnText = '愛爾達'
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

			sendPost("api.jayboapp.com:3002","",d,teams[team])
print date_cnt

