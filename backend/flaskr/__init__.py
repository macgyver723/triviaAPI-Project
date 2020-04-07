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

  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()

    if question is None:
      abort(404)
    
    question.delete()

    return jsonify({
      'success' : True,

    })

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
    
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    quiz_category = data.get('quiz_category')
    previous_questions = data.get('previous_questions')

    if quiz_category['id'] == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category == quiz_category['id']).all()
    
    i = 0
    while i < len(questions):
      if questions[i].id in previous_questions:
        questions.remove(questions[i])
      else:
        i += 1
    
    if questions:
      question = random.choice(questions).format()
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
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success" : False,
      "error" : 404,
      "message" : "Not Found"
    }), 404
  
  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success" : False,
      "error" : 422,
      "message" : "Unprocessable Entity"
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success" : False,
      "error" : 405,
      "message" : "Not Allowed"
    }), 405

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success" : False,
      "error" : 400,
      "message" : "Bad Request"
    }), 400
  
  @app.errorhandler(500)
  def internal_service_error(error):
    return jsonify({
      "success" : False,
      "error" : 500,
      "message" : "Internal Service Error"
    }), 500
  
  return app

    