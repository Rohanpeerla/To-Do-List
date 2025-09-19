from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
TASK_FILE = "tasks.txt"

# Load tasks from file
def load_tasks():
    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            for line in file:
                name, priority, status = line.strip().split(" | ")
                tasks.append({"name": name, "priority": priority.split(": ")[1], "status": status.split(": ")[1]})
    return tasks

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            file.write(f"{task['name']} | Priority: {task['priority']} | Status: {task['status']}\n")

# Prefill default tasks if not present
def prefill_tasks():
    default_tasks = [
        {"name": "Reading Books", "priority": "Medium", "status": "Pending"},
        {"name": "Listening to Music", "priority": "Low", "status": "Pending"},
        {"name": "Cooking", "priority": "High", "status": "Pending"}
    ]
    tasks = load_tasks()
    existing_names = [t['name'] for t in tasks]
    for t in default_tasks:
        if t['name'] not in existing_names:
            tasks.append(t)
    save_tasks(tasks)

prefill_tasks()

# Routes
@app.route("/")
def index():
    tasks = load_tasks()
    pending_tasks = [t for t in tasks if t['status'] == "Pending"]
    completed_tasks = [t for t in tasks if t['status'] == "Completed"]
    return render_template("index.html", pending_tasks=pending_tasks, completed_tasks=completed_tasks)

@app.route("/add", methods=["POST"])
def add_task():
    name = request.form.get("task")
    priority = request.form.get("priority")
    tasks = load_tasks()
    tasks.append({"name": name, "priority": priority, "status": "Pending"})
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_index>/<status>")
def delete_task(task_index, status):
    tasks = load_tasks()
    # Determine which list the index belongs to
    if status == "Pending":
        pending_tasks = [t for t in tasks if t['status'] == "Pending"]
        task_to_delete = pending_tasks[task_index]
    else:
        completed_tasks = [t for t in tasks if t['status'] == "Completed"]
        task_to_delete = completed_tasks[task_index]

    tasks.remove(task_to_delete)
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/complete/<int:task_index>")
def complete_task(task_index):
    tasks = load_tasks()
    pending_tasks = [t for t in tasks if t['status'] == "Pending"]
    task_to_complete = pending_tasks[task_index]
    task_to_complete['status'] = "Completed"
    save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port = 5006, debug=True)
