import os 
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
connection = psycopg2.connect(url)

CREATE_CAFE_SHOPS_TABLE = ("CREATE TABLE IF NOT EXISTS cafe_shops (id SERIAL PRIMARY KEY, cafe_username TEXT, "
                           "cafe TEXT, location TEXT, open TEXT, close TEXT, coffee_rating TEXT, wifi_rating TEXT, "
                           "power_rating TEXT);")

with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_CAFE_SHOPS_TABLE)

INSERT_CAFE_SHOP_RETURN_ID = ("INSERT INTO cafe_shops (cafe_username, cafe, location, open, close, "
                              "coffee_rating, wifi_rating, power_rating) "
                              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;")
SELECT_ALL_CAFE_SHOPS = "SELECT * FROM cafe_shops;"
SELECT_CAFE_SHOPS_BY_ID = ("SELECT id, cafe_username, cafe, location, open, close, coffee_rating, coffee_rating, "
                           "power_rating FROM cafe_shops WHERE id = %s;")
UPDATE_CAFE_USERNAME_BY_ID = "UPDATE cafe_shops SET cafe_username = %s WHERE id = %s;"
UPDATE_CAFE_SHOPS_BY_ID = "UPDATE cafe_shops SET cafe = %s WHERE id = %s;"
UPDATE_CAFE_LOCATION_BY_ID = "UPDATE cafe_shops SET location = %s WHERE id = %s;"
UPDATE_CAFE_OPEN_BY_ID = "UPDATE cafe_shops SET open = %s WHERE id = %s;"
UPDATE_CAFE_CLOSE_BY_ID = "UPDATE cafe_shops SET close = %s WHERE id = %s;"
UPDATE_CAFE_COFFE_RATING_BY_ID = "UPDATE cafe_shops SET coffee_rating = %s WHERE id = %s;"
UPDATE_CAFE_WIFI_RATING_BY_ID = "UPDATE cafe_shops SET wifi_rating = %s WHERE id = %s;"
UPDATE_CAFE_POWER_RATING_BY_ID = "UPDATE cafe_shops SET power_rating = %s WHERE id = %s;"
DELETE_CAFE_SHOP_BY_ID = "DELETE FROM cafe_shops WHERE id = %s;"


@app.route("/add/cafe-shop/<cafe_username>", endpoint='create_cafe_shop', methods=["POST"])
def create_cafe_shop(cafe_username):
    data = request.get_json()
    cafe_username = data["cafe_username"]
    cafe = data["cafe"]
    location = data["location"]
    open = data["open"]
    close = data["close"]
    coffee_rating = data["coffee_rating"]
    wifi_rating = data["wifi_rating"]
    power_rating = data["power_rating"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CAFE_SHOP_RETURN_ID, (cafe_username.data, cafe.data, location.data,
                                                        open.data, close.data, coffee_rating.data,
                                                        wifi_rating.data, power_rating.data))
            user_id = cursor.fetchone()[0]
    return {"id": user_id, "cafe_username": cafe_username, "cafe": "cafe",
            "message": f"Cafe with Cafe username:  {cafe_username} created successfully."}, 201

@app.route("/", methods=["GET"])
def get_all_cafe_shops():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_CAFE_SHOPS)
            cafe_shops = cursor.fetchall()
            if cafe_shops:
                result = []
                for cafe_shop in cafe_shops:
                    result.append({"id": cafe_shop[0], "cafe_username": cafe_shop[1], "cafe": cafe_shop[2]})
                return jsonify(result)
            else:
                return jsonify({"error": f"cafe_shops not found."}), 404


@app.route("/search/cafe-shop/<int:cafe_id>", endpoint='get_cafe', methods=["GET"])
def get_cafe(cafe_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM cafe_shops WHERE id = %s", (cafe_id,))
            cafe_shop = cursor.fetchone()
            if cafe_shop:
                return jsonify({"id": cafe_shop[0], "cafe_username": cafe_shop[1], "cafe": cafe_shop[2]})
            else:
                return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404


@app.route("/update/cafe-shops/<int:cafe_id>", endpoint='update_cafe_entries', methods=["PUT"])
def update_cafe_entries(cafe_id):
    data = request.get_json()
    cafe_username = data["cafe_username"]
    cafe = data["cafe"]
    location = data["location"]
    open = data["open"]
    close = data["close"]
    coffee_rating = data["coffee_rating"]
    wifi_rating = data["wifi_rating"]
    power_rating = data["power_rating"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CAFE_SHOP_RETURN_ID, (cafe_username, cafe, location,
                                                        open, close, coffee_rating, wifi_rating,
                                                        power_rating))
        if cursor.rowcount == 0:
            return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "Cafe Username": cafe_username, "Cafe": cafe, "Coffee Rating": coffee_rating,
                    "Wifi Rating": wifi_rating, "Power Rating": power_rating, "message": f"Cafe shop with cafe username"
                                                    f"  {cafe_username} entries updated successfully."})

@app.route("/update/cafe-shop/<int:cafe_id>", endpoint='update_cafe_username_entry', methods=["PATCH"])
def update__cafe_username_entry(cafe_id):
    data = request.get_json()
    cafe_username = data["cafe_username"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CAFE_USERNAME_BY_ID, (cafe_id, cafe_username))
        if cursor.rowcount == 0:
            return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "cafe username": cafe_username, "message": f"Cafe shop with ID {cafe_id} "
                                f"and cafe_username : {cafe_username} updated successfully."})

@app.route("/update/cafe-shop/<int:cafe_id>", endpoint='update_location_entry', methods=["PATCH"])
def update_location_entry(cafe_id):
    data = request.get_json()
    location = data["location"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CAFE_LOCATION_BY_ID, (cafe_id, location))
        if cursor.rowcount == 0:
            return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "location": location, "message": f"Cafe shop with ID {cafe_id} and "
                                                                f"location : {location} updated successfully."})
@app.route("/update/cafe-shop/<int:cafe_id>", endpoint='update_open_entry', methods=["PATCH"])
def update_open_entry(cafe_id):
    data = request.get_json()
    open = data["open"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CAFE_OPEN_BY_ID, (cafe_id, open))
        if cursor.rowcount == 0:
            return jsonify({"error": f"User with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "open": open, "message": f"Cafe shop with ID {cafe_id} "
                                                        f"and open : {open} updated successfully."})

@app.route("/update/cafe-shop/<int:cafe_id>", endpoint='update_close_entry', methods=["PATCH"])
def update_close_entry(cafe_id):
    data = request.get_json()
    close = data["close"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CAFE_CLOSE_BY_ID, (cafe_id, close))
        if cursor.rowcount == 0:
            return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "close": close, "message": f"User with ID {cafe_id} "
                                                        f"and close : {close} updated successfully."})

@app.route("/update/cafe-shop/<int:cafe_id>", endpoint='update_coffe_rating_entry', methods=["PATCH"])
def update_coffee_rating_entry(cafe_id):
    data = request.get_json()
    coffee_rating = data["coffee_rating"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CAFE_COFFE_RATING_BY_ID, (cafe_id, coffee_rating))
        if cursor.rowcount == 0:
            return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "coffee_rating": coffee_rating, "message": f"Cafe shop ID {cafe_id} "
                                                        f" and coffee_rating : {coffee_rating} updated successfully."})

@app.route("/update/cafe-shop/<int:cafe_id>", endpoint='update_wifi_rating_entry', methods=["PATCH"])
def update_wifi_rating_entry(cafe_id):
    data = request.get_json()
    wifi_rating = data["wifi_rating"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CAFE_WIFI_RATING_BY_ID, (cafe_id, wifi_rating))
        if cursor.rowcount == 0:
            return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "wifi_rating": wifi_rating, "message": f"Cafe shop with ID {cafe_id} "
                                                        f"and Wifi rating : {wifi_rating} updated successfully."})

@app.route("/update/cafe-shop/<int:cafe_id>", endpoint='update_power_rating_entry', methods=["PATCH"])
def update_power_rating_entry(cafe_id):
    data = request.get_json()
    power_rating = data["wifi_rating"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CAFE_POWER_RATING_BY_ID, (cafe_id, power_rating))
        if cursor.rowcount == 0:
            return jsonify({"error": f"Cafe shop with ID {cafe_id} not found."}), 404
    return jsonify({"id": cafe_id, "power_rating": power_rating, "message": f"Cafe shop with ID {cafe_id} "
                                                        f"and open : {power_rating} updated successfully."})
@app.route("/delete/cafe-shop/<int:cafe_id>", methods=["DELETE"])
def delete_user(cafe_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_CAFE_SHOP_BY_ID, (cafe_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"User with ID {cafe_id} not found."}), 404
    return jsonify({"message": f"Cafe shop with ID {cafe_id} deleted."})


if __name__ == '__main__':
    app.run(debug=True)