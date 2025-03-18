import requests
import logging

def process_query_with_rasa(query: str):
    try:
        rasa_url = "http://localhost:5005/model/parse"
        payload = {"text": query}
        response = requests.post(rasa_url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Rasa service error: {e}")
        raise Exception("Rasa service error")
