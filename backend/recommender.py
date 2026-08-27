from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(selectedAlbum, albums):
    #Tfidf it, to convert words into numbers
    texts = []

    for album in albums:
        text = ""

        for tag in album["tags"]:
            text += tag + " "

        for genre in album["genres"]:
            text += genre + " "

        texts.append(text)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)

    #get the index of selected album
    selectedIndex = -1

    for i, album in enumerate(albums):
        if album["title"].lower() == selectedAlbum.lower():
            selectedIndex = i
            break

    if selectedIndex == -1:
        return []

    selected_vector = vectors[selectedIndex]
    candidate_vectors = vectors
    
    #calculate similarity using cosine similarity
    similarity = cosine_similarity(selected_vector, candidate_vectors)
    
    #get the similarity scores
    scores = similarity[0]

    similarIndices = scores.argsort()[::-1]

    #get rid of the first score because it's literally the album itself
    tempSimilarIndices = []

    for i in similarIndices:
        if i != selectedIndex:
            tempSimilarIndices.append(i)

    similarIndices = tempSimilarIndices

    #print out the top 3
    top_indices = similarIndices[:18]
    recommendation = []

    for i in top_indices:
        album = albums[i]
        recommendation.append(album)

    return recommendation