import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging
from logging import FileHandler,Formatter

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  #Set up logging
  error_log = FileHandler('error.log')
  error_log.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  error_log.setLevel(logging.INFO)
  app.logger.setLevel(logging.INFO)
  app.logger.addHandler(error_log)
  app.logger.info("-----------------Starting Test---------------------")
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r'*': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
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

    questions = Question.query.all()
    questions_all = [question.format() for question in questions]

    return questions_all

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories_query = Category.query.all()
    categories = [category.format() for category in categories_query]

    try: 
      if len(categories) == 0:
        app.logger.info("/categories - No categories found.")
        abort(404)

      return jsonify({
        'success':True,
        'categories':categories,
        'total_categories':len(categories)
        })
    except Exception:
      app.logger.info("/categories - Unable to process.")
      abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions_query = Quetion.query.all()
    questions = [question.format() for question in question_query]

    if len(questions) == 0:
      app.logger.info("/questions - No questions found.")
      abort(404)

    return jsonify({
      'success':True,
      'categories':categories_all})


 
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['Delete'])
  def delete_questions(question_id):
    return QUESTIONS_PER_PAGE


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    return QUESTIONS_PER_PAGE

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
    return QUESTIONS_PER_PAGE


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_categories(category_id):
    return QUESTIONS_PER_PAGE


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
    return QUESTIONS_PER_PAGE

  '''
  Error handlers for 404 and 422 status codes
  '''

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

    