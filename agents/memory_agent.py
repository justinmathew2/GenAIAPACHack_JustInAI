from google.cloud import firestore

db = firestore.Client(database="justinai-db")

def save_memory(query, response):
    db.collection("history").add({
        "query": query,
        "response": response
    })