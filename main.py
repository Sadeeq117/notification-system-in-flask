from flask import Flask, jsonify, request
import datetime
import time
import threading

app = Flask(__name__)

# Sample task list
tasks = [
    {'id': 1, 'title': 'Grocery Shopping', 'due_date': '2024-03-15', 'completed': False},
    {'id': 2, 'title': 'Pay Bills', 'due_date': '2024-03-20', 'completed': False},
]

next_task_id = 3  # For assigning new task IDs

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_task_id
    data = request.get_json()
    new_task = {
        'id': next_task_id,
        'title': data['title'],
        'completed': False,
        'due_date': data.get('due_date') or datetime.date.today().strftime("%Y-%m-%d")
    }
    next_task_id += 1
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            # Update task attributes as task is a dictionary.
            task.update(data)  # Update task attributes
            
            # Run notification in a separate thread
            # We Do even have asyncio to perform this asynchronously but as you mention i have used threading.
            # threading.Thread is used to simulate an asynchronous task and create new thread without blocking the main thread.
            # This is useful for I/O-bound tasks like sending notifications. And args should be tuple so we have comma(,) at the end to make it as tuple.
            threading.Thread(target=send_notification, args=(task_id,)).start()

            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 204

def send_notification(task_id):
    """Simulated function to send a notification asynchronously."""
    time.sleep(2)  # Simulate delay (e.g., sending email or push notification)
    print(f"Notification sent for task {task_id}")

if __name__ == '__main__':
    app.run(debug=True)
