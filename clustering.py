from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cluster_complaints(complaints):
    if not complaints:
        return {}

    texts = [
        str(complaint[1]) + " " + str(complaint[2])
        for complaint in complaints
    ]

    if len(texts) == 1:
        return {complaints[0][0]: "Cluster 1"}

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(texts)
    similarity = cosine_similarity(matrix)

    groups = {}
    assigned = set()
    cluster_number = 1
    threshold = 0.25

    for i in range(len(complaints)):
        if i in assigned:
            continue

        cluster_name= f"{complaints[i][3]} - Group {cluster_number}"
        groups.setdefault(cluster_name, [])

        groups[cluster_name].append(complaints[i])
        assigned.add(i)

        for j in range(i + 1, len(complaints)):
            if j not in assigned and similarity[i, j] >= threshold:
                groups[cluster_name].append(complaints[j])
                assigned.add(j)

        cluster_number += 1

    return groups