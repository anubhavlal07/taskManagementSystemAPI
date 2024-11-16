from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Mock database and authentication
tasks = {}
task_id_counter = 1  # This will automatically generate IDs for new tasks
users = {
    "admin": generate_password_hash("password")
}

# Authentication handler
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

# Helper function for validation
def validate_task(data):
    errors = []
    if 'title' not in data or not isinstance(data['title'], str):
        errors.append("Title is required and must be a string.")
    if 'description' in data and not isinstance(data['description'], str):
        errors.append("Description must be a string.")
    if 'due_date' in data:
        try:
            datetime.strptime(data['due_date'], "%Y-%m-%d")
        except ValueError:
            errors.append("Due date must be in YYYY-MM-DD format.")
    return errors

# GET /tasks: Retrieve all tasks
@app.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify(list(tasks.values())), 200

# GET /tasks/{id}: Retrieve a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200

# POST /tasks: Create a new task
@app.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    global task_id_counter
    data = request.json

    errors = validate_task(data)
    if errors:
        return jsonify({'errors': errors}), 400

    task = {
        'id': task_id_counter,  # Automatically set the task id based on counter
        'title': data['title'],
        'description': data.get('description', ''),
        'due_date': data.get('due_date', None),
        'status': 'pending',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }

    tasks[task_id_counter] = task  # Store the task with the generated ID
    task_id_counter += 1  # Increment the task ID counter for the next task

    return jsonify(task), 201

# PUT /tasks/{id}: Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.json
    errors = validate_task(data)
    if errors:
        return jsonify({'errors': errors}), 400

    task.update({
        'title': data.get('title', task['title']),
        'description': data.get('description', task['description']),
        'due_date': data.get('due_date', task['due_date']),
        'updated_at': datetime.now(timezone.utc).isoformat()
    })

    return jsonify(task), 200

# DELETE /tasks/{id}: Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = tasks.pop(task_id, None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted'}), 200

# PATCH /tasks/{id}/complete: Mark a task as complete
@app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
@auth.login_required
def complete_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    task['status'] = 'completed'
    task['updated_at'] = datetime.datetime.now(timezone.utc).isoformat()

    return jsonify(task), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
