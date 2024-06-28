import os
from flask import render_template

class RouteCreator:
    def __init__(self, app, post_manager):
        self.app = app
        self.post_manager = post_manager

    def create_post_route(self, filename):
        def post_route():
            post_data = self.post_manager.load_post_data(filename)
            return render_template("post.html", data=post_data, title=post_data.get('Name', 'No Title'))
        
        route_name = filename.replace('.so', '_so')
        self.app.add_url_rule(f'/{filename.replace(".so", "")}', endpoint=route_name, view_func=post_route)
        print(f"Created route: /{filename.replace('.so', '')}")

    def create_post_routes(self):
        for filename in os.listdir(self.post_manager.data_folder):
            if filename.endswith('.so'):
                self.create_post_route(filename)