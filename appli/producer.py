import socket
import sys
import requests
import requests_oauthlib
import json
import time

CONSUMER_KEY = 'jFXCMMGq5ea8gy2nFm4De01nb'
CONSUMER_SECRET = 'tzYnklGubEaCwXQ7Qzsd9BEayOmwhaXs4hQjZwCUksuz406Kzj'
ACCESS_TOKEN = '1110547448123084801-jsP5STTqmW0wxmSbHeMb322ncshLmc'
ACCESS_SECRET = 'R7X27Z7XPVSY349FrvSIriEpPssFsn5NBoFYryhtgQOtL'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

def get_tweets():
	#url = 'https://stream.twitter.com/1.1/statuses/filter.json'
	#query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#NBAFantasy')]
	url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
	query_data = [("count", 5)]
	query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
	response = requests.get(query_url, auth=my_auth, stream=True)
	print(query_url, response)
	return response

def send_tweets_to_spark(http_resp, tcp_connection):
	for tweet in http_resp:
		try:
			tweet_text = tweet['text']
			print("Tweet Text: " + tweet_text)
			print ("------------------------------------------")
			tcp_connection.send((tweet_text + '\n').encode('ascii', 'ignore'))			
		except:
			e = sys.exc_info()[0]
			print("Error: %s" % e)
	return time.time()

TCP_IP = "172.22.224.79"
TCP_PORT = 9999
conn = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
resp = get_tweets()
print(resp)

while True:	
	print("Waiting for TCP connection...")
	start_time = time.time()
	conn, addr = s.accept()
	print("Connected... Starting getting tweets.")
	end_time = send_tweets_to_spark(resp.json(), conn)
	execution_time = end_time - start_time
	print("Execution time: {}".format(execution_time))
	print("................")
	conn.close()

