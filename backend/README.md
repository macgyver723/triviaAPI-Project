# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Endpoints

### Endpoints

```
GET '/categories'
GET '/questions'
POST '/questions'
POST '/categories/{category_id}/questions'
DELETE '/questions/{question_id}'
POST '/quizzes'
```

### Error Handling

Errors are returned as JSON objects in the following format:

```python
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Not Allowed
- 422: Unprocessable Entity
- 500: Internal Service Error

#### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Sample: `curl http//127.0.0.1:5000/categories`

```javascript
{
    'categories' : {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    "success" : true
}
```

#### GET '/questions'

- Fetches a paginated view of all questions in the database ordered by category
- Request arguments: None
- Optional URL query: `?page={num}`
- Returns a json object with a list of paginated questions, total number of questions in the database, dictionary of the categories, current category displayed, and the number of questions currently displayed.
- Sample: `curl 127.0.0.1:5000/questions?page=2`

```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "all", 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Angus", 
      "category": 5, 
      "difficulty": 4, 
      "id": 31, 
      "question": "What is MacGyver's first name?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "lkja", 
      "category": 5, 
      "difficulty": 1, 
      "id": 34, 
      "question": "ljawej"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ], 
  "questions_displayed": 10, 
  "success": true, 
  "total_questions": 28
}
```

#### GET '/categories/{category_id}/questions'

- Fetches all questions of a selected category
- Request args: None
- Returns a list of question objects, the current category, and the number of questions returned
- Sample: `curl 127.0.0.1:5000/categories/3/questions`

```javascript
{
  "current_category": "Geography", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### DELETE '/questions/{question_id}'

- Deletes the question at the given `question_id`
- Request arguments: None
- Returns `id` of deleted question
- Sample: `curl -X DELETE -H '{"Content-Type: application/json"}' http://127.0.0.1:5000/questions/4`

```javascript
{
  "deleted_question": 4, 
  "success": true
}
```

### POST '/questions'

#### Search via POST

- Fetches all questions that contain search text
- Request arguments: `searchTerm`
- Returns questions which match the search and number of total questions returned
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "who"}' http://127.0.0.1:5000/questions`

```javascript
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

#### Add new question via POST

- Adds a new question to the database
- Request arguments: 
  - `question`
  - `category` (`int` 1-5)
  - `difficulty` (`int` 1-5)
  - `answer`
- Returns new question id
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the capital of New York?", "answer" : "Albany", "category" : "3", "difficulty" : "2"}' http://127.0.0.1:5000/questions`

```javascript
{
  "new_question_id": 35, 
  "success": true
}
```

### POST '/quizzes'

- Fetches a random question from specific category, or all categories if category id is 0
- Request Arguments:
  - `quiz_category`: dictionary containing `id` and `type` of category
  - `previous_questions` : list of `id`s of previous questions of selected category
- Returns a question object to be displayed on the frontend
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"quiz_category" : {"id" : "5", "type" : "Entertainment"}, "previous_questions" : [2, 4, 6]}' http://127.0.0.1:5000/quizzes`

```javascript
{
  "question": {
    "answer": "Angus", 
    "category": 5, 
    "difficulty": 4, 
    "id": 31, 
    "question": "What is MacGyver's first name?"
  }, 
  "success": true
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```