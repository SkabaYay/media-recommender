from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(selectedGenres, selectedTags, albums):
    #Tfidf it, to convert words into numbers
    texts = []
    for album in albums:
        text = ""

        for tag in album["tags"]:
            text += tag + " "
        for genre in album["genres"]:
            text += genre + " "

        texts.append(text)

    selectedText = ""
    for tag in selectedTags:
        selectedText += tag + " "
    for genre in selectedGenres:
        selectedText += genre + " "

    vectorizer = TfidfVectorizer()
    allTexts = [selectedText] + texts
    vectors = vectorizer.fit_transform(allTexts)

    #get the index of selected album

    selected_vector = vectors[0]
    candidate_vectors = vectors[1:]
    
    #calculate similarity using cosine similarity
    similarity = cosine_similarity(selected_vector, candidate_vectors)
    
    #get the similarity scores
    scores = similarity[0]

    similarIndices = scores.argsort()[::-1]

    top_indices = similarIndices[1:19]

    recommendation = []

    for i in top_indices:
        album = albums[i]
        recommendation.append(album)

    return recommendation