#coding=utf-8
import os

teams = ['籃網','勇士','騎士','馬刺']
print str(teams).decode('string_escape')

for index in range(0,len(teams)):
	team = teams[index]

	tmp = os.popen("cat nba.raw | grep '%s\|星期' " % team)
	results = tmp.readlines()

	filter_results = []
	for index in range(0,len(results)):
		media_cnt = 0
		replay_str = ''
		if team in results[index]:

			#10:30馬刺VS勇士
			time = results[index].replace(" ", "").replace("\t","").replace("@","VS").split('-')[0] + '，'
			have_media = False
			if 'Videoland' in results[index]:

				#10:30馬刺VS勇士，緯來體育
				time = time + '緯來體育'
				have_media = True
				media_cnt = media_cnt + 1

				#(重播)VL:
				replay_str = replay_str + 'VL:'
			if 'ELTA TV' in results[index]:
				if have_media is True:
					time =  time + '、愛爾達體育'
				else: 
					time = time + '愛爾達體育'
				have_media = True
				media_cnt = media_cnt + 1
				replay_str = replay_str + 'ELTA:'
			if 'Fox Sports' in results[index]:
				if have_media is True:
					time =  time + '、FOX 2'
				else: 
					time = time + 'FOX 2'
				have_media = True
				media_cnt = media_cnt + 1
				replay_str = replay_str + 'FOX2:'
			if have_media is True:
				if media_cnt < 2:
					replay_str = ''

				#籃網- 10/29(六)7:30溜馬VS籃網，緯來體育、愛爾達體育(重播)VL:ELTA:
				final_result = team + '- ' +results[index - 1].replace(" ", "").replace("\n", "").replace("月","/").replace("日星期","(") + ')' + time + '(重播)' + replay_str + '，下一場/()'
				filter_results.append(final_result)

				#填下一場日期
				if len(filter_results) > 1:
					pre_item_next_game = final_result.split(' ')[1].split(')')[0] + ')'
					filter_results[len(filter_results) - 2] = filter_results[len(filter_results) - 2].replace('/()',pre_item_next_game)
				#filter_results.append(time)

	for elem in filter_results:
		print '\'' + str(elem).decode('string_escape') + '\','

