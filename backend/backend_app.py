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
    List all blog posts or add a new blog post.

    This endpoint serves two primary purposes:

    - For GET requests, it returns a list of all saved blog posts. You can also sort
      the results by specifying the 'sort' and 'direction' query parameters.

    - For POST requests, it allows adding a new blog post to the database. This
      requires a JSON payload with "title" and "content" attributes.

    Parameters:
    - For POST Requests:
        - JSON Payload (Required):
          {
              "title": "New Post",
              "content": "This is the content of the new post."
          }
        - Returns a JSON response with the newly added blog post or validation errors.

    Returns:
    - For GET:
        - A list of blog posts.
        - You can sort the results by specifying 'sort' (accepts 'title' or 'content')
          and 'direction' (accepts 'asc' or 'desc') query parameters.
        - Example: GET /api/posts?sort=title&direction=asc

    - For POST:
        - Either the newly added blog post or validation errors.

    Example Usage:
    - To retrieve all blog posts: GET /api/posts
    - To retrieve all blog posts sorted by title in ascending order: GET
        /api/posts?sort=title&direction=asc
    - To add a new blog post:
        POST /api/posts
        JSON Payload:
        {
            "title": "New Post",
            "content": "This is the content of the new post."
        }

    Note:
    - For sorting, 'sort' can be 'title' or 'content', and 'direction' can be 'asc' or 'desc'.
    - When posting a new blog post, make sure to include both "title" and "content" in the JSON payload.

    """
    # The existing code implementation for this endpoint remains the same.

    if request.method == "POST":
        post_request = request.get_json()
        title = post_request.get("title")
        content = post_request.get("content")

        # Check if either title or content is missing or empty
        if not title or not content:
            errors = {}
            if not title:
                errors["title error"] = "Title is missing."
            if not content:
                errors["content error"] = "Content is missing."
            return jsonify(errors), 400

        # If both title and content are present and not empty, proceed to add the post
        new_post = {
            "id": uuid4().int,
            "title": title,
            "content": content
        }

        POSTS.append(new_post)
        return jsonify(new_post), 201

    # Handle GET request:
    sort_by = request.args.get("sort")  # accepts "title" and "content"
    sort_direction = request.args.get("direction")  # accepts "asc" and "desc"

    # If no sort params are given, return posts in their default order
    if not sort_by and not sort_direction:
        return jsonify(POSTS)

    valid_params = (sort_by == "title" or sort_by == "content",
                    sort_direction == "asc" or sort_direction == "desc")

    # If params are all valid, return posts either in asc or desc order
    if all(valid_params):
        if sort_direction == "asc":
            sorted_posts_asc = sorted(POSTS, key=lambda x: x[sort_by])
            return jsonify(sorted_posts_asc)

        sorted_posts_desc = sorted(POSTS, key=lambda x: x[sort_by], reverse=True)
        return jsonify(sorted_posts_desc)

    # Handle invalid params
    return {
        "message": "Please enter valid parameters.",
        "title": "accepts 'title' and 'content' as parameters",
        "direction": "accepts 'asc' and 'desc' as parameters"
    }, 400


@app.route("/api/posts/<int:post_id>", methods=["DELETE", "PUT"])
def delete_post(post_id):
    """
    Delete a blog post by its ID.

    This endpoint allows the deletion of a blog post by specifying its unique ID in the URL.

    Args:
        post_id (int): The unique identifier of the blog post to be deleted.

    Returns:
        dict: A JSON response indicating the result of the deletion.
            - If the post is deleted successfully, returns a message and a status code 200.
            - If no post with the given ID is found, returns a message and a status code 404.
    """
    if request.method == "DELETE":
        for post in POSTS:
            if post["id"] == post_id:
                POSTS.remove(post)
                return {"message": f"Post with id {post_id} has been deleted successfully."}, 200
        return {"message": f"No post with id {post_id} was found"}, 404

    # Handle PUT request to update a blog post
    post_request = request.get_json()
    new_title = post_request.get("title")
    new_content = post_request.get("content")

    for post in POSTS:
        if post["id"] == post_id:
            if new_title:
                post["title"] = new_title
            if new_content:
                post["content"] = new_content
            return jsonify(post), 200

    # Return error if no post with requested id exists
    return {"message": f"No post with id {post_id} was found"}, 404


@app.route("/api/posts/search", methods=["GET"])
def search_post():
    """
    Search for blog posts by title and/or content.

    This endpoint allows searching for blog posts based on title and/or content.

    Parameters (query string):
        - title (str, optional): The title keyword to search for in blog posts.
        - content (str, optional): The content keyword to search for in blog posts.

    Returns:
        - If one or both search parameters are provided and match any blog post(s),
          returns a JSON response with the list of matching blog posts.
        - If no search parameters are provided or no matching posts are found,
          returns a JSON response with an appropriate message and status code.

    Example:
        To search for blog posts with the word "Python" in the title:
        GET /api/posts/search?title=Python

        To search for blog posts with the word "Flask" in the content:
        GET /api/posts/search?content=Flask

        To search for blog posts with both "Python" in title and "Flask" in content:
        GET /api/posts/search?title=Python&content=Flask

        If no matching posts are found:
        {
            "message": "No posts were found",
            "status_code": 404
        }
    """
    # Get search parameters from request
    search_title = request.args.get("title").lower()
    search_content = request.args.get("content").lower()

    found_posts = []

    # Check if either search term is provided and non-empty
    if not search_title and not search_content:
        return {"message": "Please enter at least one search query"}, 400

    # Search for posts matching the search criteria
    for post in POSTS:
        post_title = post["title"].lower()
        post_content = post["content"].lower()

        # Check if the post matches the search criteria
        if search_title:
            if search_title in post_title:
                found_posts.append(post)
        if search_content:
            if search_content in post_content:
                found_posts.append(post)

    # Handle error if no posts were found
    if not found_posts:
        return {"message": "No posts were found"}, 404

    # Return found posts
    return jsonify(found_posts), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
