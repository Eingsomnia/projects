from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/todos*": {"origins": ["http://todo-app.local"]}})

def init_db():
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/ready", methods=["GET"])
def ready():
    try:
        with sqlite3.connect("todos.db") as conn:
            conn.execute("SELECT 1")
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503

@app.route("/todos", methods=["GET"])
def get_todos():
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        todos = [{"id": row[0], "task": row[1], "completed": bool(row[2])} for row in cursor.fetchall()]
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    task = data.get("task")
    if not task:
        return jsonify({"error": "Task is required"}), 400
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task, completed) VALUES (?, ?)", (task, False))
        conn.commit()
        todo_id = cursor.lastrowid
    return jsonify({"id": todo_id, "task": task, "completed": False}), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    task = data.get("task")
    completed = data.get("completed")
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET task = ?, completed = ? WHERE id = ?", (task, completed, todo_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Todo not found"}), 404
    return jsonify({"id": todo_id, "task": task, "completed": completed})

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Todo not found"}), 404
    return jsonify({"message": "Todo deleted"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8585)