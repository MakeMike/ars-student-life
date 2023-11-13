from db_functions import *
from flask import Flask, request, flash, render_template, url_for, redirect, session, send_file
from markupsafe import escape
import markdown as md
from werkzeug.utils import secure_filename
import os
import bleach

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_TYPE"] = "filesystem"
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

userFunc = userFunctions()
postFunc = postFunctions()
eventFunc = eventFunctions()
imageFunc = imageFunctions()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/echo/')
def news(posts=None):
    return render_template("echo.html", posts=postFunc.getPosts())

@app.route('/echo/<id>/')
def newsContent(id=None):
    return render_template("post.html", content=md.markdown(postFunc.getContent(id)))

@app.route('/events/')
def events():
    return render_template("events.html", events=eventFunc.getEvents())

@app.route('/admin/')
def admin():
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        return render_template('admin.html', posts=postFunc.getPosts(), events=eventFunc.getEvents())

    except AssertionError:
        return redirect(url_for('login'))
        

@app.route('/admin/add/', methods = ['POST', 'GET'])
def addPost(id=None):
    if request.method == 'POST':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            title = bleach.clean(request.form['title'])
            caption = bleach.clean(request.form['caption'])
            image = bleach.clean(request.form['image-link'])
            content = bleach.clean(request.form['content'])
            if title and caption and image and content:
                postFunc.addPost(title, True, caption, image, content)
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('addPost'))
        except AssertionError:
            return redirect(url_for('login'))
        
    if request.method == 'GET':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            postFunc.delPost(id)
            return render_template('form.html')
        except AssertionError:
            return redirect(url_for('login'))

@app.route('/admin/edit/<id>/', methods = ['POST', 'GET'])
def adminEdit(id=None):
    if request.method == 'POST':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            title = bleach.clean(request.form['title'])
            caption = bleach.clean(request.form['caption'])
            image = bleach.clean(request.form['image-link'])
            content = bleach.clean(request.form['content'])
            if title and caption and image and content:
                postFunc.updatePost(id, title, caption, image, content)
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('adminEdit'))
        except AssertionError:
            return redirect(url_for('login'))
    if request.method == 'GET':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            post = postFunc.getPost(id)
            return render_template('editform.html', post=post)
        except AssertionError:
            return redirect(url_for('login'))
    
@app.route('/admin/new-user/', methods = ['POST', 'GET'])
def newUser():
    if request.method == 'POST':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            name = bleach.clean(request.form['title'])
            password = bleach.clean(request.form['caption'])
            if name and password:
                userFunc.addUser(name, password)
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('newUser'))
        except AssertionError:
            return redirect(url_for('userManagement'))
    if request.method == 'GET':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            return render_template('newuser.html')
        except AssertionError:
            return redirect(url_for('login'))

@app.route('/admin/users/')
def userManagement():
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        return render_template('userman.html', users=userFunc.listUser())
    except AssertionError:
        return redirect(url_for('login'))

@app.route('/admin/delete/<id>/')
def deletePost(id=None):
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        postFunc.delPost(id)
        return redirect(url_for('admin'))

    except AssertionError:
        return redirect(url_for('login'))

@app.route('/admin/delete-user/<id>/')
def deleteUser(id=None):
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        userFunc.deleteUser(id)
        return redirect(url_for('admin'))

    except AssertionError:
        return redirect(url_for('login'))

@app.route('/admin/add-event/', methods = ['POST', 'GET'])
def addEvent(id=None):
    if request.method == 'POST':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            title = bleach.clean(request.form['title'])
            caption = bleach.clean(request.form['caption'])
            image = bleach.clean(request.form['image-link'])
            date = bleach.clean(request.form['date'])
            if title and caption and image and date:
                eventFunc.addEvent(title, True, caption, image, date)
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('addEvent'))
        except AssertionError:
            return redirect(url_for('login'))
        
    if request.method == 'GET':
        try:
            assert 'session_id' in session
            assert userFunc.checkSession(session['session_id'])
            postFunc.delPost(id)
            return render_template('eventform.html')
        except AssertionError:
            return redirect(url_for('login'))

@app.route('/admin/delete-event/<id>/')
def deleteEvent(id=None):
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        eventFunc.delEvent(id)
        return redirect(url_for('admin'))

    except AssertionError:
        return redirect(url_for('login'))

@app.route('/admin/edit-event/<id>/', methods = ['POST', 'GET'])
def eventEdit(id=None):
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        if request.method == 'POST':        
            title = bleach.clean(request.form['title'])
            caption = bleach.clean(request.form['caption'])
            image = bleach.clean(request.form['image-link'])
            date = bleach.clean(request.form['date'])
            if title and caption and image and date:
                eventFunc.updateEvent(id, title, caption, image, date)
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('eventEdit'))
        else:
            event = eventFunc.getEvent(id)
            return render_template('eventedit.html', event=event)
    except AssertionError:
        return redirect(url_for('login'))

@app.route('/admin/media/', methods=['GET', 'POST'])
def media():
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect(url_for('media'))
            
            file = request.files['file']
            
            if file.filename == '':
                return redirect(url_for('media'))
            title = bleach.clean(request.form['title'])
            if file and allowed_file(file.filename) and title!='':
                filename = bleach.clean(secure_filename(file.filename))
                unique_filename = f"{str(uuid.uuid4())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                file_location = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                imageFunc.upload(title, file_location)
                return redirect(url_for('media'))
            else:
                print(imageFunc.getImages())
                return redirect(url_for('media'), images=imageFunc.getImages())
        else:
            return render_template('images.html', images=imageFunc.getImages())
    except AssertionError:
        return redirect(url_for('login'))

@app.route('/admin/delete-image/<id>/')
def imageDelete(id):
    try:
        assert 'session_id' in session
        assert userFunc.checkSession(session['session_id'])
        os.remove(imageFunc.getImage(id))
        imageFunc.deleteImage(id)
        return redirect(url_for('media'))
    except AssertionError:
        return redirect(url_for('login'))


@app.route('/login/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = bleach.clean(request.form['username'])
        password = bleach.clean(request.form['password'])
        sessionID = userFunc.login(username, password)
        
        if sessionID:
            session['session_id'] = sessionID
            return redirect(url_for('admin'))

        else:
            return redirect(url_for('login'))
        
    if request.method == 'GET':
        return render_template('login.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/image/<id>/')
def image(id):
    return send_file(imageFunc.getImage(id), mimetype='image/png')

@app.route('/logout/')
def logout():
    if 'session_id' in session:
        userFunc.logout(session['session_id'])
        session.pop('session_id')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

if __name__=="__main__":
    app.run(port="8000", debug=True)