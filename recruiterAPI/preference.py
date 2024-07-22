# from sentence_transformers import SentenceTransformer, util
# from sklearn.metrics.pairwise import cosine_similarity

import requests

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": "Bearer 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"}

def aiComperision(job_description,resume):

    try: 

        payload = {
                    "inputs": {
                        "source_sentence": str(job_description),
                        "sentences": [str(resume)]
                    },
                }

        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        
        result = str(round((output[0] * 100 ), 2))


        # comparision = [job_description,resume]
        # embeddings = model.encode(comparision)
        # similarity_score = cosine_similarity(embeddings[0].reshape(1, -1), embeddings[1].reshape(1, -1))
        # percentage_similarity = ((similarity_score + 1) / 2) * 100
        # result = str(round(percentage_similarity[0][0],2))
        
        return result

    except:
        print("AI comparision Error.")
        return ""


