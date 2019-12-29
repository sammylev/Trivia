import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging
from logging import FileHandler,Formatter
from sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # Set up logging
  error_log = FileHandler('error.log')
  error_log.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  error_log.setLevel(logging.INFO)
  app.logger.setLevel(logging.INFO)
  app.logger.addHandler(error_log)
  app.logger.info("-----------------Starting Test---------------------")
  
  '''
  Setup for CORS. Allow '*' for origins.
  '''
  CORS(app, resources={r'*': {'origins': '*'}})

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
    return response

  def paginate(request,selection):
    page = request.args.get('page',1,type=int)
    first_displayed = (page-1)*QUESTIONS_PER_PAGE
    last_displayed = first_displayed + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    questions_pagniated = questions[first_displayed:last_displayed]

    return questions_pagniated

  '''
  Endpoint to handle GET requests for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    app.logger.info("/categories")
    try: 
      categories_query = Category.query.all()
      categories = [category.format() for category in categories_query]
      app.logger.info(categories)
      
      if len(categories) == 0:
        app.logger.info("/categories - No categories found.")
        abort(404)

      return jsonify({
        'success':True,
        'categories':categories,
        'total_categories':len(categories)
        }),200
    except Exception:
      app.logger.info("/categories - Unable to process.")
      app.logger.info(categories)
      abort(422)

  '''
  Endpoint to handle GET requests for questions 
  
  Output: a list of questions, number of total questions, current category, categories. 

  TEST: When you start the application, you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():

    try:
      questions_query = Question.query.order_by(Question.id).all()
      questions = paginate(request,questions_query)

      if len(questions) == 0:
        app.logger.info("/questions - No questions found.")
        abort(404)

      current_category=[question['category'] for question in questions]
      categories={category.id: category.type for category in Category.query.all()}

      return jsonify({
        'success':True,
        'questions':questions,
        'total_questions':len(questions_query),
        'current_category':current_category,
        'categories':categories
        }),200
    except Exception:
      app.logger.info(questions)
      
      if len(questions) == 0:
        app.logger.info("/questions - No questions found.")
        abort(404)
      else:
        app.logger.info("/questions - Unable to process.")
        abort(422)


 
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['Delete'])
  def delete_questions(question_id):
    try:
      question = Question.query.get(question_id)

      if not question:
        abort(404)

        question.delete()

        return jsonify({
          'success':True,
          'deleted':question_id,
          'total_questions':len(Question.query.all())
          }),200
    except Exception:
      if not question:
        app.logger.info("No question found")
        abort(404)
      else:
        app.logger.info(question)
        abort(422)

  '''
  @TODO: 
  Endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():

    try:
      data = request.get_json()
      new = Question(
        data['question'],
        data['answer'].
        data['category'],
        data['difficulty']
        )
      app.logger.info('/questions post')
      app.logger.info(new)
      new.insert()

      selection = Question.query.order_by(Question.id).all()
      questions = paginate(request,selection)

      return jsonify({
        'success':True,
        'questions':questions,
        'created':question.id,
        'total_questions':len(Question.query.all())
        }),200
    except Exception:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    try:
      search_term = request.json[search_term]

      query = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()

      results = paginate(reuest,query)

      return jsonify({
        'success':True,
        'questions':results,
        'total_questions':len(results),
        'current_category':[(question['category']) for question in results]
        }),200
    except Exception:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_categories(category_id):
    query= Question.query.filter_by(category=category_id).all()
    questions_pagniated=paginate(request,query)

    if len(questions_pagniated)==0:
      abort(404)

    return jsonify({
      'success':True,
      'questions':questions_pagniated,
      'total_questions':len(questions_pagniated),
      'current_category':category_id
      }),200


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
  def get_quizzes():
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    quiz_category = data.get('quiz_category')

    category_id = int(quiz_category['id'])

    if (len(previous_questions) > 0):
      if (category_id > 0):
        current_question = Question.query.filter_by(Question.category == category_id).filter(Question.id.in_(previous_questions)).order_by(func.random()).first()
      else:
        current_question = Question.query.filter(Question.id.in_(previous_questions)).order_by(func.random()).first()
    else:
      if (category_id > 0):
        current_question = Question.query.filter(Question.category == category_id).order_by(func.random()).first()
      else:
        current_question = Question.query.order_by(func.random()).order_by(func.random()).first()

    if len(current_question) > 0:
      formatted_question = current_question.format()
    else:
      formatted_question = None

    return jsonify({
      'success': True,
      'question': formatted_question
      }),200

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'message': 'unprocessable'
      }), 422

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'message': 'resource not found'
      }), 404

  return app