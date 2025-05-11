from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'secret'  # Needed for flashing messages

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
        

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        tasks = load_tasks()
        tasks.append({'task': task, 'done': False})
        save_tasks(tasks)
        flash('Task added!')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
        flash('Task deleted.')
    else:
        flash('Error: Task does not exist.')
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = True
        save_tasks(tasks)
        flash('Task marked as completed.')
    else:
        flash('Error: Task does not exist.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

