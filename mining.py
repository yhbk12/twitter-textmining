import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Authenticating
consumer_key = 'GyfyFJEkU6cyGBq0PPLjHlvz0'
consumer_secret = 'q3ghkBA8i1qheGFFnpd5mmCmlAlrNIk02wqTqeoQ2gERHiwqLw'
access_token = '855727868-h0MenCCakLLaz6engeaIm2mh77j3uoOnN5DIXV07'
access_secret = 'c4TWPLTCmdx8ijhXS3gkH59Wcv8PGJ8BUFDTFXfT6hMiS'

#Listener class
class PrintOutListener(StreamListener):

    def on_data(self, raw_data):
        print (raw_data)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)

if __name__ == "__main__":
    holder = PrintOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, holder)
    stream.filter(track=['glaxosmithkline', 'new'])

