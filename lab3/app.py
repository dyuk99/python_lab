from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from pymongo import MongoClient
MONGO_URL = "localhost:27017"

client = MongoClient(MONGO_URL)
messages = []
for d in client.forum_db.forum.find().limit(1000):
messages.append(d['message'])

tokenizer = RegexpTokenizer(r"\w+")
lemmatizer = WordNetLemmatizer()
processed = []
for m in messages:
    tokens = [t for t in tokenizer.tokenize(str.lower(m)) if t not in stopwords.words("english")]
    if len(tokens) > 0:
        processed.append([lemmatizer.lemmatize(t) for t in tokens])

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform([y for x in processed for y in x])

clusters = 10
model = KMeans(n_clusters=clusters)
model.fit(X)
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(clusters):
    print("Cluster %d:\n" % i)
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])
print('\n')



