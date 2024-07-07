from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import markdown
from datetime import datetime
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'

# Set up logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

users = {}  # In-memory user store, replace with a database in production

def save_post(title, content, author):
    filename = f"posts/{title.replace(' ', '_').lower()}.md"
    app.logger.debug('Saving post: %s', filename)
    with open(filename, 'w') as file:
        file.write(f"# {title}\n\n")
        file.write(f"**Author**: {author}\n\n")
        file.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write(content)
    return filename

def load_posts():
    posts = []
    app.logger.debug('Loading posts from directory: %s', os.path.abspath('posts'))
    for filename in os.listdir('posts'):
        if filename.endswith('.md'):
            with open(os.path.join('posts', filename), 'r') as file:
                content = file.read()
                post_html = markdown.markdown(content)
                posts.append((filename.replace('.md', ''), post_html))
    return posts

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists')
        else:
            users[username] = generate_password_hash(password)
            flash('Registration successful')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        save_post(title, content, author)
        return redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/posts/<post_id>')
def post(post_id):
    try:
        with open(f'posts/{post_id}.md', 'r') as file:
            content = file.read()
            post_html = markdown.markdown(content)
        return render_template('post.html', post=post_html)
    except Exception as e:
        app.logger.error('Error loading post %s: %s', post_id, e)
        return "Post not found", 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return "Internal server error", 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return "Unhandled exception", 500

if __name__ == '__main__':
    app.run(debug=True)
