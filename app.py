from flask import (Flask, jsonify, flash, request)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'vanov'
app.config['MYSQL_PASSWORD'] = 'Allheilvon11$'
app.config['MYSQL_DB'] = 'larapi'
app.secret_key = 'sahkdksbfksbkfbsk'
mysql = MySQL(app)

@app.route('/user')
def user():
  try:
    cur = mysql.connection.cursor()
    query = "SELECT id, name, email FROM users"
    cur.execute(query)
    users = cur.fetchall()
    resp = jsonify(users)
    resp.status_code = 200
    return resp
  except Exception as e:
    print(e)
  finally:
    cur.close()
    
@app.route('/user/<id>')
def user_spec(id):
  try:
    cur = mysql.connection.cursor()
    query = "SELECT id, name, email FROM users WHERE id='{}'".format(id)
    cur.execute(query)
    users = cur.fetchall()
    resp = jsonify(users)
    resp.status_code = 200
    return resp
  except Exception as e:
    resp.status_code = 404
    return resp
  finally:
    cur.close() 


@app.route('/post')
def post():
  try:
    cur = mysql.connection.cursor()
    query = "SELECT posts.id AS post_id, users.id AS user_id, users.name AS user_name, posts.content AS post_content FROM posts INNER JOIN users ON posts.user_id=users.id ORDER BY posts.id DESC"
    cur.execute(query)
    users = cur.fetchall()
    data = transform(users)
    resp = jsonify(data)
    resp.status_code = 200
    return resp
  except Exception as e:
    print(e)
  finally:
    cur.close()

@app.route('/post/add', methods=['POST'])
def store_post():
  try:
    user_id = request.json['user']
    post = request.json['post']
    cur = mysql.connection.cursor()
    query  = "INSERT INTO posts (user_id, content) VALUES ('{}', '{}')".format(user_id, post)
    cur.execute(query)
    mysql.connection.commit()
    resp = jsonify('Post added successfully!')
    resp.status_code = 200
    return resp
  except Exception as e:
    print(e)
  finally:
    cur.close()

@app.route('/post/<id>', methods=['PUT', 'GET', 'DELETE'])
def post_spec(id):
  if request.method == 'GET':
    return show_post(id)
  elif request.method == 'DELETE':
    return delete_post(id)
  elif request.method == 'PUT':
    return update_post(id)

def show_post(id):
  try:
    cur = mysql.connection.cursor()
    query = "SELECT posts.id, users.id, users.name, posts.content FROM posts INNER JOIN users ON posts.user_id=users.id WHERE posts.id = {}".format(id)
    cur.execute(query)
    users = cur.fetchone()
    data = singleTransform(users)
    resp = jsonify(data)
    resp.status_code = 200
    return resp
  except Exception as e:
    resp = jsonify('POST NOT FOUND!')
    resp.status_code = 404
    return resp
  finally:
    cur.close()

def delete_post(id):
  try:
    cur = mysql.connection.cursor()
    query  = "DELETE FROM posts WHERE id = {}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    resp = jsonify('Post deleted successfully!')
    resp.status_code = 200
    return resp
  except Exception as e:
    print(e)
  finally:
    cur.close()

def update_post(id):
  try:
    post_id = id
    post = request.json['post']
    cur = mysql.connection.cursor()
    query  = "UPDATE posts SET content='{}' WHERE id='{}'".format(post, post_id)
    cur.execute(query)
    mysql.connection.commit()
    resp = jsonify('Post updated successfully!')
    resp.status_code = 200
    return resp
  except Exception as e:
    print(e)
  finally:
    cur.close()

def transform(value):
  array = []
  for i in value:
    array.append(singleTransform(i))
  return array

def singleTransform(value):
  data = {
    'id': value[0],
    'user_id': value[1],
    'user_name': value[2],
    'post_content' : value[3]
  }

  return data