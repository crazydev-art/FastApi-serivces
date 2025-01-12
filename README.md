# FastApi-serivces
This project involves building an API using FastAPI that supports generating quizzes for a web or mobile application. The API allows authenticated users to retrieve questions based on specific parameters or create new questions as an admin.


### Features

1. **Endpoints**:

   - `/verify` - Verifies that the API is functional.
   - `/generate_quiz` - Generates a quiz based on provided parameters.
   - `/create_question` - Allows an admin to create a new question.

2. **Authentication**:

   - Basic authentication using username and password, sent as a Base64-encoded string in the request headers.

3. **Dynamic Question Retrieval**:

   - Users can filter questions by test type, category, and quantity (e.g., 5, 10, 20 questions).
   - Randomized order of questions ensures variety in repeated queries.

4. **Data Source**:

   - Questions are stored in a CSV file that includes fields such as `question`, `subject`, `correct`, `use`, `responseA`, `responseB`, `responseC`, and `responseD`.

5. **Error Handling**:

   - Appropriate error messa



### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fastapi-quiz-service.git
   cd fastapi-quiz-service
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application locally:

   ```bash
   uvicorn main:app --reload
   ```

4. Access the API documentation at `http://127.0.0.1:8000/docs`.

---

### Testing the API

Use `curl` or any API testing tool like Postman to test the endpoints. Examples of `curl` requests are provided in the `requests.txt` file.

---

### File Structure

```
.
├── main.py               # Main application file
├── questions.csv         # CSV file containing question data
├── requirements.txt      # Dependencies for the project
├── requests.txt          # Sample curl requests
├── README.md             # Project documentation
```

---

### Contribution

Feel free to fork the repository and submit pull requests to improve the project. Ensure that all new features are tested and documented.

---

### License

This project is licensed under the MIT License.

