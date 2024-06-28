import os

class PostManager:
    def __init__(self, data_folder):
        self.data_folder = data_folder

    def load_post_data(self, filename):
        post_data = {}
        file_path = os.path.join(self.data_folder, filename)
        with open(file_path, 'r') as f:
            for line in f:
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    post_data[key.strip()] = value.strip()
        return post_data

    def get_all_posts(self):
        posts_data = []
        try:
            for filename in os.listdir(self.data_folder):
                if filename.endswith('.so'):
                    post = self.load_post_data(filename)
                    post['filename'] = filename.replace('.so', '')
                    posts_data.append(post)
        except FileNotFoundError:
            print(f"Data folder not found: {self.data_folder}")
        except Exception as e:
            print(f"Error loading posts: {str(e)}")
        return posts_data