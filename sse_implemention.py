from flask import Flask, jsonify, request, Response
import json
import time
import datetime

subscribers = []

app = Flask(__name__)

# Sample task list
tasks = [
    {'id': 1, 'title': 'Grocery Shopping', 'due_date': '2024-03-15', 'completed': False},
    {'id': 2, 'title': 'Pay Bills', 'due_date': '2024-03-20', 'completed': False},
]

next_task_id = 3  # For assigning new task IDs

@app.route('/api/stream')
def stream():
    """SSE endpoint to send real-time task updates to clients."""
    def event_stream():
        while True:
            if subscribers:
                message = json.dumps({"message": "Task list updated"})
                for sub in subscribers:
                    sub.write(f"data: {message}\n\n")
                    sub.flush()
            time.sleep(2)  # Check every 2 seconds for updates

    return Response(event_stream(), content_type='text/event-stream')

@app.route('/api/tasks', methods=['POST'])
def create_task_sse():
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
    
    # Notify subscribers
    for sub in subscribers:
        sub.write(f"data: {json.dumps(new_task)}\n\n")
        sub.flush()

    return jsonify(new_task), 201


#Front end method implementation.
"""
import { fromEventSource } from 'rxjs-sse';
import { map } from 'rxjs/operators';

const eventSource = fromEventSource('http://localhost:5000/api/stream');

eventSource.pipe(
  map(event => JSON.parse(event.data))
).subscribe(update => {
  console.log('Task update received:', update);
  // Update the UI with new task data
});

"""