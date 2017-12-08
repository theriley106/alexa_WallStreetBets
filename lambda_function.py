import requests
import bs4
import random
import re

def grabNewPost():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://www.reddit.com/r/wallstreetbets/search?q=what+are+your+moves&sort=new&restrict_sr=on&t=all', headers=headers)
	page = bs4.BeautifulSoup(res.text,"lxml")
	for title in page.select(".search-title"):
		if '[' in title.getText() and ',' in title.getText():
			return 'https://www.reddit.com' + str(title).partition('data-href-url="')[2].partition('"')[0] + '?sort=top'

def returnTopComment(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get(url, headers=headers)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	comments = page.select('.unvoted')[3:]
	parentComments = []
	for comment in comments:
		if 'data-event-action="downvote"' in str(comment) or len(str(comment)) < 30 or 'data-event-action="parent"' in str(comment):
			pass
		else:
			try:
				parentComments.append(str(comment.select('.md p')[0].getText()))
			except:
				pass
	return parentComments


def lambda_handler(event, context):
	print event
	print context
	# TODO implement
	return {
  "version": "1.0",
  "sessionAttributes": {},
  "response": {
	"outputSpeech": {
	  "type": "PlainText",
	  "text": str(random.choice(returnTopComment(grabNewPost())))
	},
	"shouldEndSession": False
  }
}


if __name__ == '__main__':
	pass
	#print lambda_handler('event', 'context')