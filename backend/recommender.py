# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def recommend(selectedGenres, selectedTags, albums):
#     #Tfidf it, to convert words into numbers
#     texts = []
#     for album in albums:
#         text = ""

#         for tag in album["tags"]:
#             text += tag + " "
#         for genre in album["genres"]:
#             text += genre + " "

#         texts.append(text)

#     selectedText = ""
#     for tag in selectedTags:
#         selectedText += tag + " "
#     for genre in selectedGenres:
#         selectedText += genre + " "

#     vectorizer = TfidfVectorizer()
#     allTexts = [selectedText] + texts
#     vectors = vectorizer.fit_transform(allTexts)

#     #get the index of selected album

#     selected_vector = vectors[0]
#     candidate_vectors = vectors[1:]
    
#     #calculate similarity using cosine similarity
#     similarity = cosine_similarity(selected_vector, candidate_vectors)
    
#     #get the similarity scores
#     scores = similarity[0]

#     similarIndices = scores.argsort()[::-1]

#     top_indices = similarIndices[1:19]

#     recommendation = []

#     for i in top_indices:
#         album = albums[i]
#         recommendation.append(album)

#     return recommendation

import math
from collections import Counter


def recommend(selectedGenres, selectedTags, albums):

    # Create text for each candidate
    texts = []

    for album in albums:
        words = album["genres"] + album["tags"]
        texts.append(words)

    # Text for selected album
    selectedWords = selectedGenres + selectedTags

    # Number of documents
    totalDocuments = len(texts) + 1

    # Count how many documents contain each word
    documentFrequency = Counter()

    for words in texts:
        for word in set(words):
            documentFrequency[word] += 1

    for word in set(selectedWords):
        documentFrequency[word] += 1

    # Calculate IDF
    idf = {}

    for word, frequency in documentFrequency.items():
        idf[word] = math.log(totalDocuments / frequency)

    # Calculate TF-IDF vector
    def createVector(words):

        counts = Counter(words)
        totalWords = len(words)

        vector = {}

        for word, count in counts.items():
            tf = count / totalWords
            vector[word] = tf * idf.get(word, 0)

        return vector

    selectedVector = createVector(selectedWords)

    # Cosine similarity
    def cosineSimilarity(vectorA, vectorB):

        dotProduct = 0

        for word in vectorA:
            if word in vectorB:
                dotProduct += vectorA[word] * vectorB[word]

        magnitudeA = math.sqrt(
            sum(value ** 2 for value in vectorA.values())
        )

        magnitudeB = math.sqrt(
            sum(value ** 2 for value in vectorB.values())
        )

        if magnitudeA == 0 or magnitudeB == 0:
            return 0

        return dotProduct / (magnitudeA * magnitudeB)

    # Score every candidate
    scoredAlbums = []

    for album, words in zip(albums, texts):

        vector = createVector(words)

        similarity = cosineSimilarity(
            selectedVector,
            vector
        )

        scoredAlbums.append(
            (similarity, album)
        )

    # Highest similarity first
    scoredAlbums.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # Return top 18
    return [
        album
        for similarity, album in scoredAlbums[:18]
    ]