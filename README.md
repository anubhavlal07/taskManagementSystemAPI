
# Task Management API

This is a simple RESTful API for managing tasks. The API allows users to create, retrieve, update, delete, and mark tasks as complete.

## Features

- **GET /tasks**: Retrieve all tasks.
- **GET /tasks/{id}**: Retrieve a specific task by ID.
- **POST /tasks**: Create a new task.
- **PUT /tasks/{id}**: Update an existing task.
- **DELETE /tasks/{id}**: Delete a task.
- **PATCH /tasks/{id}/complete**: Mark a task as complete.

## Prerequisites

Before running the application, you will need to have the following installed:
- Python 3.x
- pip (Python's package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/task-management-api.git
   cd task-management-api
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. The application will run on `http://127.0.0.1:5000`.

## Testing the API

You can test the API using tools like [Postman](https://www.postman.com/) or `curl`.

### Example Requests:

1. **GET All Tasks**
   ```bash
   curl -X GET http://127.0.0.1:5000/tasks
   ```

2. **POST Create a Task**
   ```bash
   curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title": "New Task", "description": "Test task", "due_date": "2024-12-01"}'
   ```

3. **PUT Update a Task**
   ```bash
   curl -X PUT http://127.0.0.1:5000/tasks/1 -H "Content-Type: application/json" -d '{"title": "Updated Task", "description": "Updated task description", "due_date": "2024-12-10"}'
   ```

4. **PATCH Mark a Task as Complete**
   ```bash
   curl -X PATCH http://127.0.0.1:5000/tasks/1/complete
   ```

5. **DELETE Delete a Task**
   ```bash
   curl -X DELETE http://127.0.0.1:5000/tasks/1
   ```
