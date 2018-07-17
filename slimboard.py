#!/usr/bin/env python

import datetime
import hashlib
import sqlite3

import bottle, bottlesession
from bottle import route, request, response, HTTPError, template, SimpleTemplate, static_file
            
def get_array(db, table, array_id):
    return db.execute('SELECT `'+table+'`.* FROM `array` INNER JOIN `'+table+'` ON `array`.`child_id` = `'+table+'`.`id` WHERE `array`.`id`=?', (array_id,)).fetchall()

salt = 'SZ6^GI7T5Vf@%oz7'

session_manager = bottlesession.CookieSession()
valid_user = bottlesession.authenticator(session_manager)
db = sqlite3.connect('test.db')
app = bottle.Bottle()

@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@app.route('/')
def index():
    page = ''
    page += '<a href="/post/create">New Post</a><br/><br/>'
    rows = db.execute('SELECT * FROM `post`').fetchall()
    
    posts = []
    for row in rows:
        posts.append([str(row[0]), row[2]])
    
    return template('index', {
        'title': "SlimBB", 
        'posts': posts, 
        'group_name': "Default", 
        'user_name': request.get_cookie("user_name", secret=salt)})
        
@app.route('/post/create')
def post_create():
    return '''
<form action="/post/create" method="post">
  Title: <input type="text" name="title" />
</form>
'''

@app.route('/post/create', method='POST')
def post_create_post():
    title = request.forms.title
    db.execute('INSERT INTO `post` '
        '(`created`, `title`, `user_id`) '
        'VALUES (datetime(\'now\'), ?, ?)', 
        (title, 0))
    
    return '{"code":0, "message":Successfully created a new post!"}'

@app.route('/post/show/:post_id')
def post_show(post_id):
    row = db.execute('SELECT `title` FROM `post` WHERE `id`=?', (post_id,)).fetchone()
    if row == None:
        return HTTPError(404, 'Post not found')
    
    title = row[0]
    
    rows = db.execute('SELECT `text` FROM `comment` WHERE `post_id`=?', (post_id,)).fetchall()
    escaped_comments = []
    for row in rows:
        
        escaped_comments.append(bottle.html_escape(row[0]).replace("\n", "<br>"))
        
    return template('post_show', {
        'title': title, 
        'escaped_comments': escaped_comments, 
        'post_id': post_id, 
        'group_name': "Default", 
        'user_name': request.get_cookie("user_name", secret=salt)})
    
    

@app.route('/comment', method='POST')
def comment_post():
    post_id = request.forms.post_id
    text = request.forms.text
    
    db.execute('INSERT INTO `comment` '
        '(`created`, `text`, `user_id`, `post_id`) '
        'VALUES (?, ?, ?, ?)', 
        (datetime.datetime.now(), text, 0, post_id))
    
    return '{"code":0, "message": "Successfully commented!"}'

@app.route('/poll/show/:poll_id')
def poll(poll_id):
    
    #Should prolly show current results if user has voted... maybe
    return template('poll_show', {
        'title': 'Which Quest?', 
        'poll_id': 1, 
        'group_name': "Default", 
        'user_name': request.get_cookie("user_name", secret=salt)})

@app.route('/poll/vote', method='POST')
def poll_vote_post(db):
    if not request.forms.get('poll_id'):
        return '{"code":1, "message": "Malformed request!"}'
    if not request.forms.get('choice'):
        return '{"code":1, "message": "Please select your choice!"}'
    if not request.get_cookie("user_id", secret=salt):
        return '{"code":1, "message": "You are not logged in!"}'
    
    choice = request.forms.get('choice')
    user_id = request.get_cookie("user_id", secret=salt)
    poll_id = request.forms.get('poll_id')
    
    #Get the poll in question
    row = db.execute('SELECT * \
        FROM `poll` \
        WHERE `id`=?', (poll_id,)).fetchone()
    vote_array_id = row[2]
    
    #See if user has voted yet
    row = db.execute('SELECT `vote`.* \
        FROM `array` \
        INNER JOIN `vote` ON `array`.`child_id` = `vote`.`id` \
        WHERE `array`.`id`=? \
            AND `vote`.`user_id`=?',
        (vote_array_id, user_id)).fetchone()
    if row:
        #If they have, we'll just change the vote
        db.execute('UPDATE `vote` \
            SET `choice`=? \
            WHERE `id`=?', (choice, row[0]))
        return '{"code":0, "message": "Successfully updated vote!"}'
    
    #Add another vote to the array
    vote_id = db.execute('INSERT INTO `vote` \
        (`user_id`, `choice`) \
        VALUES (?, ?)', (user_id, choice)).lastrowid
    
    db.execute('INSERT INTO `array` \
        (`id`, `child_id`) \
        VALUES (?, ?)', (vote_array_id, vote_id))
    
    return '{"code":0, "message": "Successfully voted!"}'

@app.route('/user/login')
def user_login():
    return template('user_login', {
        'group_name': "Default", 
        'user_name': request.get_cookie("user_name", secret=salt)})

@app.route('/user/login', method='POST')
def user_login_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == '' or not username:
        return '{"code":1, "message": "Username cannot be blank!"}'
    if password == '' or not password:
        return '{"code":1, "message": "Password cannot be blank!"}'
    
    row = db.execute('SELECT `password`, `id`, `name` FROM `user` WHERE `name` LIKE ?', (username,)).fetchone()
    
    if not row:
        return '{"code":1, "message": "Username or password do not match!"}'
    
    if hashlib.sha256((salt+password).encode('utf-8')).hexdigest() != row[0]:
        return '{"code":1, "message": "Username or password do not match!"}'
    
    print(row[1])
    print(row[2])
    
    response.set_cookie("user_id", row[1], secret=salt, path='/')
    response.set_cookie("user_name", row[2], secret=salt, path='/')
    return '{"code":0, "message": "Successfully logged in!"}'

@app.route('/user/logout')
def user_logout():
    response.delete_cookie("user_id", path='/')
    response.delete_cookie("user_name", path='/')
    return 'You have been logged out!'

@app.route('/user/test')
def user_test():
    if not request.get_cookie("user_id", secret=salt):
        return "You are not logged in!"
    
    user_id = request.get_cookie("user_id", secret=salt)
    print(user_id)
    return "Welcome user "+str(user_id)

@app.route('/auth/login')
def login():
    session = session_manager.get_session()
    session['valid'] = True
    session_manager.save(session)
    return "Logged in!"
    
@app.route('/auth/logout')
def logout():
    session = session_manager.get_session()
    session['valid'] = False
    session_manager.save(session)
    bottle.redirect('/auth/login')
         
app.run(host='0.0.0.0', port=8080, debug=True, reloader=False);
