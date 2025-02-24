import os
import requests


def retrieve_chunks(question):
    response = requests.post("https://api.ragie.ai/retrievals",
                             json={
                                 "query": question,
                                 "rerank": True
                             },
                             headers={
                                 "accept":
                                 "application/json",
                                 "content-type":
                                 "application/json",
                                 "authorization":
                                 f"Bearer {os.getenv('RAGIE_API_KEY')}"
                             })

    data = response.json()
    clean_data = [chunk["text"] for chunk in data["scored_chunks"]]

    print(f"Found {len(clean_data)} results")

    return clean_data
