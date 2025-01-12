from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import pandas as pd
import random



#data
try:
    data = pd.read_csv('./questions.csv')
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Data file not found.")

# Initialize FastAPI
app = FastAPI()

# Authentication setup
security = HTTPBasic()
users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

admin_credentials = {
    "admin": "4dm1N"
}

def authenticate(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password
    if users.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return username

def authenticate_admin(credentials: HTTPBasicCredentials):
    if credentials.username != "admin" or credentials.password != "4dm1N":
        raise HTTPException(status_code=401, detail="Authentification échouée. Accès interdit.")

# Models
class QuizRequest(BaseModel):
    test_type: str
    categories: list[str]
    number_of_questions: int


class QuestionAdminRequest(BaseModel):
    admin_username: str
    admin_password: str
    question: str
    subject: str
    correct: list[str]
    use: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str


# Endpoints
@app.get("/verify")
def verify():
    return {"message": "L'API est fonctionnelle."}

@app.post("/generate_quiz")
def generate_quiz(request: QuizRequest, credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)

    # Validate number of questions
    if request.number_of_questions not in [5, 10, 20]:
        raise HTTPException(status_code=419, detail="Invalid number of questions. Must be 5, 10, or 20.")

    # Filter questions by type and category
    filtered_data = data[
        (data["use"] == request.test_type) &
        (data["subject"].isin(request.categories))
    ]


    filtered_data = filtered_data.iloc[:, :-1]


    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="No questions match your Criteria.")

    if request.number_of_questions > len(filtered_data):
        raise HTTPException(status_code=400, detail="ther is Not enough questions available.")

    #select questions Randomly
    try:
        selected_questions = filtered_data.sample(request.number_of_questions).to_dict(orient="records")
        # Ensure all data is JSON compliant
        for question in selected_questions:
            for key, value in question.items():
                if isinstance(value, float) and (pd.isna(value) or value in [float('inf'), float('-inf')]):
                    question[key] = None
    except Exception as e:
        
        raise HTTPException(status_code=500, detail="Error generating quiz.")

    # Shuffle the questions to ensure randomness
    random.shuffle(selected_questions)

    return selected_questions


data = []

@app.post("/create_question")
def create_question(request: QuestionAdminRequest, credentials: HTTPBasicCredentials = Depends(security)):
    # Authenticate the admin
    authenticate_admin(credentials)

    # Create a new question dictionary
    new_question = {
        "question": request.question,
        "subject": request.subject,
        "correct": ",".join(request.correct),
        "use": request.use,
        "responseA": request.responseA,
        "responseB": request.responseB,
        "responseC": request.responseC,
        "responseD": request.responseD
    }

    # Add the new question to the data list
    data.append(new_question)

    # Convert the data list to a DataFrame for further processing if needed
    df = pd.DataFrame(data)

    return {"message": "Question créée avec succès."}
