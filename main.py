from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# download only if not present
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))  # load once

# load models
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextInput(BaseModel):
    message: str

# preprocessing (optimized)
def transform_text(text):
    text = text.lower()
    words = nltk.word_tokenize(text)

    words = [w for w in words if w.isalnum()]
    words = [w for w in words if w not in stop_words]

    words = [ps.stem(w) for w in words]

    return " ".join(words)

app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/predict")
def predict(data: TextInput):
    transformed = transform_text(data.message)

    # DEBUG (very important)
    print("Original:", data.message)
    print("Processed:", transformed)

    vector_input = tfidf.transform([transformed])

    result = model.predict(vector_input)[0]
    prob = model.predict_proba(vector_input)[0]

    return {
        "input": data.message,
        "processed": transformed,
        "prediction": "Spam" if result == 1 else "Not Spam",
        "confidence": {
            "Not Spam": float(prob[0]),
            "Spam": float(prob[1])
        }
    }