from bs4 import BeautifulSoup
import requests
import csv
import time


class notification_bot(object):

	def get_article():

		article = ''
		source = requests.get('https://www.avito.ma/fr/maroc/asus_rog').text

		soup = BeautifulSoup(source, 'lxml')

		articles = soup.find('div', class_='listing listing-thumbs')
		article_name = articles.find('h2', class_= 'fs14').text
		#article_date = article.find('div', class_='item-age').text
		#article_date = 'abc'

		#alpha = ['a','b','c','d','e','f','g','h','i','j','k','m','n','l','o','p','q','r','s','t','u','v','w','x','y','z',"'"]
		#alphaA = ['A','B','C','D','E','F','G','H','I','J','K','M','N','L','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
		#for elt in article_date:
		#	if elt in alpha or elt in alphaA:
		#		article_date = article_date.replace(elt, '')

		return article_name


	def is_new(article_name):
		with open ('avito-product', 'r+') as f:
			csv_reader = csv.reader(f)
			counter = 0
			for ids, row in enumerate(csv_reader):
				if len(row)> 0:
					if ids == counter:
						if ''.join(row) == article_name:
							return True
				counter += 1

		csv_file = open('avito-product', 'a')
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(article_name)
		return False


	def send_message(article_new, article):
		
		TOKEN = '973461519:AAFYv6-fA7SwGovhvZ8IPgKlixyd0MCzHAY'
		BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
		UPDATE_TELEGRAM_URL = 'https://api.telegram.org/bot{}/getUpdates'.format(TOKEN)
		TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'

		req = requests.get(UPDATE_TELEGRAM_URL)
		req = req.json()
		if len(req)> 0:
			req = req['result']
			if article_new == False:
				chat_id = req[-1]['message']['chat']['id']
				Send_message = BASE_TELEGRAM_URL+'/sendMessage?chat_id={}&text={}'.format(chat_id, article)
				requests.get(Send_message)



while True:	
	notif = notification_bot
	article_name = notif.get_article()
	print(article_name)
	print(notif.is_new(article_name))
	article_new = notif.is_new(article_name)
	notif.send_message(article_new, article_name)
	time.sleep(60)