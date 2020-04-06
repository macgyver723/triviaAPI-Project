import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_paginated(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [q.format() for q in selection]

  return questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app, resources={r"/api/*" : {"origins" : "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH,OPTIONS")
    return response

  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.type).all()

    if len(categories) == 0:
      abort(404)
    
    return jsonify({
      'success' : True,
      'categories' : {c.id : c.type for c in categories}
    })


  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_all_questions():
    questions = Question.query.order_by(Question.category).all()
    selected_questions = get_paginated(request, questions)

    return jsonify({
      'success' : True,
      'questions' : selected_questions,
      'total_questions' : len(questions),
      'categories' : {c.id : c.type for c in Category.query.order_by(Category.type).all()},
      'current_category' : 'all',
      'questions_displayed' : len(selected_questions)
    })

  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):    
    category = Category.query.filter(Category.id == category_id).one_or_none()

    if category is None:
      abort(404)

    questions = Question.query.filter(Question.category == category_id).all()
    selected_questions = get_paginated(request, questions)

    return jsonify( {
      'success' : True,
      'questions' : selected_questions,
      'current_category' : category.type,
      'total_questions' : len(questions)
    })
    
  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()

    if question is None:
      abort(404)
    
    question.delete()

    return jsonify({
      'success' : True,

    })

  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods = ['POST'])
  def add_question():
    data = request.get_json()

    question = data.get('question', None)
    category = data.get('category', None)
    difficulty = data.get('difficulty', None)
    answer = data.get('answer', None)
    search = data.get('searchTerm', None)

    try:
      print(f"search is : {search}")
      if search:
        selection = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
        current_selection = get_paginated(request, selection)
        print(f"current_selection[0]: {current_selection[0]}")
      
        return jsonify({
          "success" : True,
          "questions" : current_selection,
          "total_questions" : len(selection),
          "current_category" : current_selection[0]['category'],
        })
      
      else:
        new_question = Question(question, answer, category, difficulty)
        new_question.insert()

        return jsonify({
          "success" : True
        })
    
    except:
      abort(400)
    
   
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    quiz_category = data.get('quiz_category')
    previous_questions = data.get('previous_questions')
    print(f"\n\tprevious_questions: {previous_questions}")
    questions = Question.query.filter(Question.category == quiz_category['id']).all()
    print(f"\tAll questions: {questions}")
    

    ### maybe try to make this loop more efficient somehow?

    removed = False
    for q in questions[:]:
      print(f"\t\tChecking if {q.id} is in {previous_questions}")
      if q.id in previous_questions:
        questions.remove(q)
        print(f"\tremoved <Question {q.id}>")
        removed = True
    
    
    if removed:
      print(f"\tquestions after remove loop: {questions}")
    
    if questions:
      question = random.choice(questions).format()
      print(f"\trandom question chosen: <Question {question['id']}>")

      previous_questions.append(int(question['id']))
    else: 
      question = False

    return jsonify({
      "success" : True,
      "question" : question,
      "previousQuestions" : previous_questions
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    