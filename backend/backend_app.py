from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    # Fehlerbehandlung
    if not data or "title" not in data:
        return jsonify({"error": "Missing field: title"}), 400
    if "content" not in data:
        return jsonify({"error": "Missing field: content"}), 400

    # Neue ID generieren
    new_id = max([p["id"] for p in POSTS], default=0) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    new_posts = [p for p in POSTS if p["id"] != post_id]

    if len(new_posts) == len(POSTS):
        return jsonify({"error": "Post not found"}), 404

    POSTS = new_posts
    return jsonify({"message": "Post deleted"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
