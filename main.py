import os 
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
connection = psycopg2.connect(url)

CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS api_users (id SERIAL PRIMARY KEY, username TEXT, email TEXT, phone TEXT, name TEXT);"

with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_USERS_TABLE)

INSERT_USER_RETURN_ID = "INSERT INTO api_users (username, name, email, phone) VALUES (%s, %s, %s, %s) RETURNING id;"
SELECT_ALL_USERS = "SELECT * FROM api_users;"
SELECT_USER_BY_ID = "SELECT id, username, name, email, phone FROM api_users WHERE id = %s;"
UPDATE_NAME_BY_ID = "UPDATE api_users SET name = %s WHERE id = %s;"
UPDATE_USERNAME_BY_ID = "UPDATE api_users SET username = %s WHERE id = %s;"
UPDATE_EMAIL_BY_ID = "UPDATE api_users SET email = %s WHERE id = %s;"
UPDATE_PHONE_BY_ID = "UPDATE api_users SET phone = %s WHERE id = %s;"
DELETE_USER_BY_ID = "DELETE FROM api_users WHERE id = %s;"

@app.route("/add/user/<username>", methods=["POST"])
def create_user(username):
    data = request.get_json()
    name = data["name"]
    username = data["username"]
    email = data["email"]
    phone = data["phone"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER_RETURN_ID, (username,name,email,phone))
            user_id = cursor.fetchone()[0]
    return {"id": user_id, "name": name, "email": email, "phone": phone, "message": f"Username:  {username} created successfully."}, 201

@app.route("/", methods=["GET"])
def get_all_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_USERS)
            users = cursor.fetchall()
            if users:
                result = []
                for user in users:
                    result.append({"id": user[0], "username": user[1]})
                return jsonify(result)
            else:
                return jsonify({"error": f"Users not found."}), 404

@app.route("/search/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM api_users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return jsonify({"id": user[0], "name": user[1]})
            else:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404


@app.route("/update/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    username = data["username"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_USERNAME_BY_ID, (username, user_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404
    return jsonify({"id": user_id, "username": username, "message": f"User with ID {user_id} and username : {username} updated successfully."})

@app.route("/update/user/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()
    username = data["username"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_USERNAME_BY_ID, (username, user_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404
    return jsonify({"id": user_id, "username": username, "message": f"User with ID {user_id} and username : {username} updated successfully."})

@app.route("/update/user/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()
    email = data["email"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_EMAIL_BY_ID, (email, user_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404
    return jsonify({"id": user_id, "email": email, "message": f"User with ID {user_id} and email : {email} updated successfully."})


@app.route("/update/user/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()
    phone = data["phone"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_PHONE_BY_ID, (phone, user_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404
    return jsonify({"id": user_id, "phone": phone, "message": f"User with ID {user_id} and email : {phone} updated successfully."})


@app.route("/delete/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_USER_BY_ID, (user_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404
    return jsonify({"message": f"User with ID {user_id} deleted."})


if __name__ == '__main__':
    app.run(debug=True)