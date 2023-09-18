from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
CORS(app)

POSTS = [
    {
        "id": 150827827629351278599002114473176449446,
        "title": "First post",
        "content": "This is the first post."
    },
    {
        "id": 993283712504264096323267467220203096123,
        "title": "Second post",
        "content": "This is the second post."
    },
]


@app.route("/api/posts", methods=["GET", "POST"])
def list_or_create_posts():
    """
    Endpoint [/api/post] to either list all blog posts or to add a new blog post.
    Behaviour of route changes depending on request method:

    GET:
        - Return all saved blog posts in database

    POST:
        - Add a new blog post to database and return it
    """
    if request.method == "POST":
        post_request = request.get_json()
        has_title = post_request["title"] != ""
        has_content = post_request["content"] != ""

        if has_title and has_content:
            new_post = {
                "id": uuid4().int,
                "title": post_request["title"],
                "content": post_request["content"]
            }

            POSTS.append(new_post)
            return jsonify(new_post), 201
        return "Title and Content are mandatory to add new posts. Please try again", 400
    return jsonify(POSTS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
