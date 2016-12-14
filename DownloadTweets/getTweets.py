import tweepy
import re

#Sources:
#Tweepy documentation: http://docs.tweepy.org/en/v3.5.0/index.html
#Regular expression to remove links from tweet: http://stackoverflow.com/questions/24399820/expression-to-remove-url-links-from-twitter-tweet
#Delete contents of python file: http://stackoverflow.com/questions/17126037/how-to-delete-only-the-content-of-file-in-python

#Twitter keys to download tweets using the API are marked as XXXXXX.
#We got the original keys through a twitter account we created. New twitter keys are needed to run this code.

auth = tweepy.OAuthHandler("XXXXXX", "XXXXXX")
auth.set_access_token("XXXXXX", "XXXXXX")

api = tweepy.API(auth)

def deleteContent(pfile):
    #Function to empty a twitter file before it is updated with more recent tweets
    pfile.seek(0)
    pfile.truncate()


user_input = raw_input("Enter users:")
while(user_input != "exit"):
    input_users = user_input.split(',')
    total_tweets = 0
    for user in input_users:
        file_name = "TweetDatabases/tweetDatabase_" + user
        dbase = open(file_name, 'w') #Open the user's tweet file or create new one if it does not exist
        deleteContent(dbase) #Delete the contents of the file
        i = 0
        print(user)
        print("#-----------------------------------------------------")
        for status in tweepy.Cursor(api.user_timeline, id=user).items(): #Iterate over the user's tweets
            tweet = re.sub(r"http\S+", "", status.text)
            tweet = re.sub('[^a-zA-Z0-9\s\.,@#]', '', tweet)
            tweet = re.sub('\n', '', tweet)
            dbase.write("[" + user + "][" + str(tweet) + "]\n")
            print(str(i) + '. ' + tweet)
            i += 1
            total_tweets += 1
        print("#-----------------------------------------------------")

    print("Total number of tweets retrieved: " + str(total_tweets))
    user_input = raw_input("Enter users:")



