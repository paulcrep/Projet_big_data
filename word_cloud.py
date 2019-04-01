#CREPIN Paul William BI1 - Timothée Marguier P2020
import numpy as np # linear algebra
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from subprocess import check_output

mpl.rcParams['font.size']=12                #10
mpl.rcParams['savefig.dpi']=100             #72
mpl.rcParams['figure.subplot.bottom']=.1

#Utilisation de Wordcloud qui permet de générer un visuel en fonction de tout
# les mots trouvé.

stopwords = set(STOPWORDS)
data = pd.read_csv("result.csv")

# On génère word cloud
mask = np.array(Image.open("usa.png"))
wordcloud_usa = WordCloud(stopwords=stopwords, background_color="white", mode="RGBA", max_words=2000, mask=mask).generate(str(data['word']))

# On crée la couleur pour notre image
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[7,7])
plt.imshow(wordcloud_usa.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

# On enregistre l'image
plt.savefig("us.png", format="png")

plt.show()
