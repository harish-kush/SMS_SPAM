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
import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ NLTK setup (Render FIXED)
nltk_data_path = "/tmp/nltk_data"
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

# 🔥 IMPORTANT: download ALL required resources
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords', download_dir=nltk_data_path)

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt', download_dir=nltk_data_path)

# 🔥 THIS WAS MISSING (main bug)
try:
    nltk.data.find('tokenizers/punkt_tab')
except:
    nltk.download('punkt_tab', download_dir=nltk_data_path)

# init after downloads
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# ✅ Load models
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# request body
class TextInput(BaseModel):
    message: str

# preprocessing
def transform_text(text):
    text = text.lower()
    words = nltk.word_tokenize(text)

    words = [w for w in words if w.isalnum()]
    words = [w for w in words if w not in stop_words]

    words = [ps.stem(w) for w in words]

    return " ".join(words)

# ✅ Prediction API
@app.post("/predict")
def predict(data: TextInput):
    try:
        transformed = transform_text(data.message)
        vector_input = tfidf.transform([transformed])
        result = model.predict(vector_input)[0]
        prob = model.predict_proba(vector_input)[0]

        return {
            "prediction": "Spam" if result == 1 else "Not Spam",
            "confidence": {
                "Not Spam": float(prob[0]),
                "Spam": float(prob[1])
            }
        }
    except Exception as e:
        return {"error": str(e)}

# ✅ Homepage
@app.get("/")
def home():
    return FileResponse("index.html")

# ✅ Static files
app.mount("/static", StaticFiles(directory="."), name="static")