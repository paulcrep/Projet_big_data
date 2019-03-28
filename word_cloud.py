import numpy as np # linear algebra
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

mpl.rcParams['font.size']=12                #10
mpl.rcParams['savefig.dpi']=100             #72
mpl.rcParams['figure.subplot.bottom']=.1

#Utilisation de Wordcloud qui permet de générer un visuel en fonction de tout
# les mots trouvé.

stopwords = set(STOPWORDS)
data = pd.read_csv("result.csv")

wordcloud = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40,
                          random_state=42
                         ).generate(str(data['word']))

print(wordcloud) #affichage
fig = plt.figure(1)
plt.imshow(wordcloud)  #affichage
plt.axis('off')  #affichage
plt.show()  #affichage
fig.savefig("word1.png", dpi=900)  #affichage
