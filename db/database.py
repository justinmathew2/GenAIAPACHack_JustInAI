from google.cloud import firestore

db = firestore.Client(database="justinai-db")

def add_task(task):
    db.collection("tasks").add({
        "task": task,
        "status": "pending"
    })

def get_tasks():
    docs = db.collection("tasks").stream()
    tasks = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        tasks.append(data)

    return tasks

def clear_tasks():
    docs = db.collection("tasks").stream()
    for doc in docs:
        doc.reference.delete()    