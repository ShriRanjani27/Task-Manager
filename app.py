from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_url_path='/static')
#app = Flask(__name__, template_folder="templates")


todos = [{"task": "Sample Todo", "done": False, "date_completed": None}]

@app.route("/")
def index():
    total_tasks = len(todos)
    completed_tasks = sum(1 for todo in todos if todo.get('done', False))

    
    percentage_completed = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    return render_template("index.html", todos=todos, percentage_completed=percentage_completed)

@app.route("/add", methods=["POST"])
def add():
    todo = request.form['todo']
    todos.append({"task": todo, "done": False, "date_completed": None})
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    todo = todos[index]
    if request.method == "POST":
        todo['task'] = request.form["todo"]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, index=index)

@app.route("/check/<int:index>")
def check(index):
    task = todos[index]

    
    if 'date_completed' not in task or task['date_completed'] is None:
        task['done'] = not task.get('done', False)
        task['date_completed'] = datetime.now()
    elif task['date_completed'].date() != datetime.now().date():
        task['done'] = not task.get('done', False)
        task['date_completed'] = datetime.now()

    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    del todos[index]
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
