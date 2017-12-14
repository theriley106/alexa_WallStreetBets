import requests
import bs4
import random
import re
import csv

STOCKS = ["JayNug", "Ayy Em Dee", "Tess a la", "En Vid Ia"]
POSTITION = ["Short", "Long"]

def csvToList(fileName):
	with open(fileName, 'rb') as f:
		reader = csv.reader(f)
		return list(reader)[1:]


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
	if event["request"]["type"] == "LaunchRequest":
		return on_launch(event["request"], event["session"])
	elif event["request"]["type"] == "IntentRequest":
		return on_intent(event["request"], event["session"])
	elif intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()

def on_launch(launch_request, session):
	return get_welcome_response()

def on_intent(intent_request, session):
	intent = intent_request["intent"]
	intent_name = intent_request["intent"]["name"]
	if intent_name == "getAdvice":
		return returnComment()
	else:
		raise handle_session_end_request()

def getTicker(word):
	for ticker in STOCKS:
		if str(ticker[0]) == str(word):
			return str(ticker[1]).lower().replace('coorporation', '').replace('incorporated', '').replace(', the', '')
	return word

def getRandomComment():
	'''comment = str(random.choice(returnTopComment(grabNewPost())))
	for word in comment.split(" "):
		if word.isupper() == True and len(word) > 1 and len(word) < 6:
			comment.replace(word, getTicker(word))

		if "$" in word:
			if len(''.join(re.findall("[a-zA-Z]+", word))) == len(word) - 1:
				comment.replace(word, getTicker(word))'''
	f = open('moves.txt','r')
	message = f.read()
	comments = message.split('\n')
	f.close()
	return random.choice(comments)




def returnComment():
	return {
	"version": "1.0",
	"sessionAttributes": {},
	"response": {
	"outputSpeech": {
	"type": "PlainText",
	"text": getRandomComment()
		},
		"shouldEndSession": False
	  }
	}

def handle_session_end_request():
	card_title = "WallStreetBets"
	speech_output = "I have no idea what you said, so I'm going to exit.  Thank you for asking an inanimate circular object how to invest your money"
	should_end_session = True
	return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


def get_welcome_response():
	session_attributes = {}
	card_title = "WallStreetBets"
	speech_output = "Welcome to the are slash Wall Street Bets alexa skill. " \
					" You can ask me for investment advice, or expert D D or whatever you want I don't care"
	reprompt_text = "Please ask me for advice or what my moves are in the coming days, " \
					"I can answer a lot of the simple questions that are posted on to the wall street bets subreddit"
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
	return {
		"outputSpeech": {
			"type": "PlainText",
			"text": output
		},
		"card": {
			"type": "Simple",
			"title": title,
			"content": output
		},
		"reprompt": {
			"outputSpeech": {
				"type": "PlainText",
				"text": reprompt_text
			}
		},
		"shouldEndSession": should_end_session
	}

def build_response(session_attributes, speechlet_response):
	return {
		"version": "1.0",
		"sessionAttributes": session_attributes,
		"response": speechlet_response
	}

if __name__ == '__main__':
	pass
	#print lambda_handler('event', 'context')