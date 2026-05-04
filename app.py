from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Simple in-memory blog storage (in production, use a database)
posts = [
    {
        'id': 1,
        'title': 'Welcome to My Blog Sunny',
        'content': 'This is the first blog post. Welcome to our blogging platform!',
        'author': 'Admin',
        'date': '2026-05-01'
    },
    {
        'id': 2,
        'title': 'Getting Started with Python',
        'content': 'Python is a versatile programming language. Learn the basics to get started with web development.',
        'author': 'Admin',
        'date': '2026-05-02'
    },
    {
        'id': 3,
        'title': 'Docker for Beginners',
        'content': 'Docker containerization makes deployment easier. Learn how to containerize your Python applications.',
        'author': 'Admin',
        'date': '2026-05-03'
    }
]

# Simple counter for new posts
next_id = 4


@app.route('/')
def index():
    """Home page - display all blog posts"""
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """View a single blog post"""
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    return "Post not found", 404


@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create a new blog post"""
    if request.method == 'POST':
        global next_id
        data = request.get_json()
        
        new_post = {
            'id': next_id,
            'title': data.get('title', 'Untitled'),
            'content': data.get('content', ''),
            'author': data.get('author', 'Anonymous'),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        posts.append(new_post)
        next_id += 1
        
        return jsonify(new_post), 201
    
    return render_template('create.html')


@app.route('/api/posts')
def api_posts():
    """API endpoint to get all posts"""
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>')
def api_post(post_id):
    """API endpoint to get a single post"""
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """API endpoint to delete a post"""
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return jsonify({'message': 'Post deleted'}), 200


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Run on port 3000
    app.run(host='0.0.0.0', port=3000, debug=True)
