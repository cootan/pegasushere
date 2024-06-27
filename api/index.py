import os
from flask import Flask, render_template, jsonify
from post_manager import PostManager
from route_creator import RouteCreator

app = Flask(__name__)
data_folder = os.path.join(os.path.dirname(__file__), 'data')
post_manager = PostManager(data_folder)
route_creator = RouteCreator(app, post_manager)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/genre")
def genre():
    return render_template("genre.html")

@app.route("/posts")
def posts():
    posts_data = post_manager.get_all_posts()
    return render_template("posts.html", posts=posts_data)

@app.route("/api/posts")
def api_posts():
    posts_data = post_manager.get_all_posts()
    return jsonify(posts_data)

if __name__ == "__main__":
    route_creator.create_post_routes()
    app.run(debug=True)