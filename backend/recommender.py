from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

albums = [
    {
        "title": "OK Computer",
        "artist": "Radiohead",
        "tags": "alternative rock art rock experimental rock"
    },
    {
        "title": "The Bends",
        "artist": "Radiohead",
        "tags": "alternative rock britpop guitar rock"
    },
    {
        "title": "Kid A",
        "artist": "Radiohead",
        "tags": "alternative rock electronic experimental"
    },
    {
        "title": "In Rainbows",
        "artist": "Radiohead",
        "tags": "alternative rock art rock"
    },
    {
        "title": "Currents",
        "artist": "Tame Impala",
        "tags": "psychedelic rock electronic psychedelic pop"
    },
    {
        "title": "Discovery",
        "artist": "Daft Punk",
        "tags": "electronic house dance french house"
    }
]

def recommend(selectedAlbum, albums):
    #Tfidf it, to convert words into numbers
    texts = [album["tags"] for album in albums]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(texts)

    #calculate similarity using cosine similarity
    similarity = cosine_similarity(vectors)

    #get the index of selected album
    selectedIndex = 0

    for i, album in enumerate(albums):
        if album["title"] == selectedAlbum:
            selectedIndex = i
            break

    #get the similarity scores
    scores = similarity[selectedIndex]

    similarIndices = scores.argsort()[::-1]

    #get rid of the first score because it's literally the album itself
    tempSimilarIndices = []

    for i in similarIndices:
        if i != selectedIndex:
            tempSimilarIndices.append(i)

    similarIndices = tempSimilarIndices

    #print out the top 3
    top_indices = similarIndices[:3]
    recommendation = []

    for i in top_indices:
        album = albums[i]
        recommendation.append(album["title"])

    return recommendation

recommendations = recommend("OK computer", albums)
print(recommendations)