# Flask API

This is a simple Flask-based blog application that allows users to view, add, delete, and search blog posts. The application consists of both a frontend and a backend, with the frontend being responsible for the user interface and the backend handling data storage and API endpoints.


## Prerequisites

Before running this application, make sure you have the following installed:

- Python (3.6 or higher)
- Flask
- Flask-CORS (for enabling Cross-Origin Resource Sharing)
- A modern web browser


## Installation

1. Clone or download the project from the [GitHub repository](https://github.com/your-repo-url).

2. Navigate to the project directory in your terminal.

3. Install the required Python packages using pip:

```bash
pip install flask flask-cors
```


## Usage

### Running the Backend

1. Open a terminal and navigate to the project directory.

2. Run the backend server by executing the following command:

```bash
python backend/backend.py
```

This will start the Flask server, and you should see output indicating that the server is running.


### Running the Frontend

1. Open another terminal window (or tab) and navigate to the project directory.

2. Run the frontend server using the following command:

```bash
python frontend/frontend.py
```

The frontend server will start, and you'll see output indicating that the server is running. By default, it will run on `http://0.0.0.0:5001`.

3. Open your web browser and navigate to `http://0.0.0.0:5001` (or `http://localhost:5001`). You should see the blog application's user interface. Now, enter your API Base URL which is `http://0.0.0.0:5002/api` by default.


### Using the Application

- **View Posts**: When you open the application, it will display existing blog posts (if any).

- **Add a Post**: To add a new post, enter a title and content in the input fields and click the "Add Post" button.

- **Delete a Post**: Each post has a "Delete" button. Click it to delete the corresponding post.

- **Search Posts**: You can search for posts by title and/or content. Enter your search criteria in the respective input fields and click the "Search" button.


## API Endpoints

The backend provides the following API endpoints:

- `GET /api/posts`: Get a list of all blog posts or filter and sort them using query parameters (`sort` and `direction`).
  
- `POST /api/posts`: Add a new blog post by sending a JSON payload with "title" and "content" attributes.

- `DELETE /api/posts/{post_id}`: Delete a blog post by its unique ID (`post_id`).

- `PUT /api/posts/{post_id}`: Update a blog post by its unique ID (`post_id`) by sending a JSON payload with new "title" and/or "content" attributes.

- `GET /api/posts/search`: Search for blog posts using query parameters `title` and `content`. Posts will be loaded in their default order if no parameters are given.