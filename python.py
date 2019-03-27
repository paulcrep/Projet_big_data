#CREPIN Paul William BI1 - P2020
import tweepy #outils indispensable pour récupérer les tweets
from tweepy import OAuthHandler
from textblob import TextBlob #outils pour les sentiments
import numpy as np # fonction mathématique
import csv #Import csv
import time #pour marquer des pauses dans le code
import pandas as pd
import re #expression régulière
import collections
import matplotlib.pyplot as plt
from matplotlib import style, rcParams
import string

'''
Pour réaliser ce Projet nous avons crée plusieurs fonction afin de permettre la récupération, le filtrage,
ainsi que l'analyse de nos tweets en fonction d'un query déterminé en amont
'''

class TwitterProject(object):
	# Script d'analyse des sentiments des tweets .
	def __init__(self):
        #initialisation du programme
		# on identitie des clefs de l'api twitter
		consumer_key_twitter = 'dVURgADi9GrHWksUOGlgNPgzo'
		consumer_secret_twitter = 'CMmFsupwPUDGxg7ZVH3paAH2EIYaOm1S8J9aitYKafILiJkhLI'
		access_token_twitter = '775398075221286912-jRCoSaZM5sHxv1dwPry7Z35HszOMFAh'
		access_token_secret_twitter = 'moHDSa2ZbzFBrsasi0I6nMvIhPKlNRRzkOe2oarI8AYwH'

		# Essaie de connection à l'API
		try:
			# création du OAuthHandler object venant de tweepy
			self.auth = OAuthHandler(consumer_key_twitter, consumer_secret_twitter)
			# on crée un access token et au secret
			self.auth.set_access_token(access_token_twitter, access_token_secret_twitter)
            # On crée une tweepy API pour récupérer les tweets
			self.api = tweepy.API(self.auth)
		except:
            # Erreur
			print("Erreur : La connexion à échouée")

	def trouver_tweet_sentiment(self, tweet):
        # Pour réaliser cette fonction(sentiments) nous utilisons la fonction textblob
        # Cette fonction permet de classifier les tweets en fonction de keywords prédéfini dans une bibliothèque
		analyse = TextBlob(self.tweet_cleaner(tweet))
		# On analyse les sentiments
		analyse.sentiment
		print(analyse.sentiment)
		#
		if analyse.sentiment.polarity > 0:
			return "positive"
			# par rapport au fonctionnement de textblob
			#si un tweet à une polarité inférieur ou supérieur à 0 son état change
		elif analyse.sentiment.polarity == 0:
			return "neutral"
		else:
			return "negative"
    # Fonction pour cleaner les tweet afin d'enlever les liens ainsi que les caractères spéciaux.
	def tweet_cleaner(self, tweet):
		return ' '.join(re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|RT|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet).split())

# On récupère une liste de tweet
	def recuperer_les_tweets(self, query, count = 10):
		'''
        Cette fonction permet parser les tweets, nous avons eu certaines difficulté pour implémenter cette fonction
        En raison d'une première utilisation du module tweepy
		'''
		# on crée une liste vide
		tweets = []

		try:
			# On appel l'API tweepy qui à été checké auparavant en lui indiquant notre query
			fetched_tweets = self.api.search(q = query, count = count)

			# on check les tweets 1 par 1
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# On enregistre le text des tweets
				parsed_tweet['text'] = tweet.text
				# on enregistre le sentiment des tweets à partir de texteblob
				parsed_tweet['sentiment'] = self.trouver_tweet_sentiment(tweet.text)

				# ajout du  tweet analysé à la liste twitter
				if tweet.retweet_count > 0:
					# Si les tweets on été retwitté on les mets dans une liste
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
				#	Ajoute un élément à la fin de la liste.

			# On retourne les tweets parcourus
			return tweets

		except tweepy.TweepError as e:
			# Affichage d'une eventuelle erreur
			print("ERREUR : " + str(e))

def main():

    # Ouverture de notre fichier database qui enregistrera nos données
    csvFile = open('database.csv', 'a')
    # Utilisation de Csv Writer pour créer notre document
    csvWriter = csv.writer(csvFile)
	# Création d'une classe twitter client
    api = TwitterProject()
	# On appelle une fonction pour récupérer les tweets
    tweets = api.recuperer_les_tweets(query = 'Donald Trump', count = 300)
    # Récupération des tweets
    print('\x1b[6;30;42m' + "\n\nRécupération des tweets pour :" + '\x1b[0m')
    print("Enregistrement des tweets sur un fichier csv")
    # Enregistrement des tweets sur un fichier csv
    csvWriter.writerow([tweets])
    csvFile.close()
    #Pause
    time.sleep(1)
    print("Done.")
    #pause
    time.sleep(1)
	# On trie les tweets et on prend les tweets positif à partir de textblob
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# On calcul le pourcentage de tweet positif
    print("\033[1;32;40m Positive tweets percentage: {} %".format(100*len(positive_tweets)/len(tweets)))
	# On parse les tweets négatif
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# On calcul le pourcentage de tweet negatif
    print("\033[1;31m Negative tweets percentage: {} %".format(100*len(negative_tweets)/len(tweets)))
	# Pourcentage de tweets neutres
    print("\033[1;37m Neutral tweets percentage: {} %".format(100*(len(tweets) - len(negative_tweets) - len(positive_tweets))/len(tweets)))
	# On affiche les premiers tweets positif
    print('\x1b[1;30;42m' + "\n\nPositive tweets:" + '\x1b[0m')
    for tweet in positive_tweets[:15]:
        print(tweet['text'])

	# On affiche les 5 premiers tweets negatif
    print('\033[6;30;41m' +"\n\nNegative tweets:" + '\x1b[0m')
    for tweet in negative_tweets[:15]:
        print(tweet['text'])
# Fin du programme
    time.sleep(2)
    print("fin")
    time.sleep(2)
# Ouverture
# On compte combien de fois chaque words à été utilisé
text = open('database.csv').read()
words = text.split()
# On enlève toute la ponctuation
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in words]
print(stripped[:1000])
# Notre fichier de donnée est nettoyé de sorte à enlever la ponctuation
output_file = open('databaseclean.csv', 'w')
writer = csv.writer(output_file)
writer.writerow(stripped)

#######################################################################
translator = str.maketrans('', '', string.punctuation)
word_count = {}
db = open('databaseclean.csv').read()
words = text.split()

for word in words:
    word = word.translate(translator).lower()
    count = word_count.get(word, 0)
    count += 1
    word_count[word] = count

word_count_list = sorted(word_count, key=word_count.get, reverse=True)
for word in word_count_list[:20]:
    print(word, word_count[word])

output_file = open('result.csv', 'w')
writer = csv.writer(output_file)
writer.writerow(['word', 'count'])
for word in word_count_list:
    writer.writerow([word, word_count[word]])
#######################################################################

if __name__ == "__main__":
	# On rapelle la fonction principale
    main()
