
# Cafe-Rating-Postgres-API

Cafe-Rating-Postgres-API is a simple RESTful API built using Flask and PostgreSQL. It allows you to perform CRUD (Create, Read, Update, Delete) operations on a database through HTTP requests.

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/olusesa/cafe-rating-postgres-api.git
    ```

2. Navigate into the project directory:
    ```
    cd cafe-rating-api
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Set up your PostgreSQL database and configure the connection details as environment variable.

5. Run the application:
    ```
    python main.py
    ```

By default, the application will run on `http://localhost:5000`.

## Endpoints

- **GET /**: Retrieve all cafe shops.
- **GET /search/cafe-shop/<id>**: Retrieve a specific cafe shop by ID.
- **POST /add/cafe-shop/<username>**: Create a new cafe shop.
- **PUT /update/cafe-shop/<id>**: Update a cafe shop username by ID.
- **PATCH /update/cafe-shop/<id>**: Update a cafe shop name entry by ID.
- **DELETE /delete/cafe-shop/<id>**: Delete a cafe shop by ID.

## Request & Response Examples

### GET all ("/")

Request:
```
curl http://localhost:5000/
```

Response:
```
[
    {
        "id": #,
        "cafe_username": "<cafe_username>
        "cafe": "<cafe>",
        "location": "<location>",
        "open": "<open>"
        "close": "<close>"
        "coffee_rating": "<coffee_rating>"
        "wifi_rating": "<wifi_rating>"
        "power_rating": "<power_rating>"
    },
    {
        "id": #,
        "cafe_username": "<cafe_username>
        "cafe": "<cafe>",
        "location": "<location>",
        "open": "<open>"
        "close": "<close>"
        "coffee_rating": "<coffee_rating>"
        "wifi_rating": "<wifi_rating>"
        "power_rating": "<power_rating>"
    }
]
```

### GET /search/cafe-shop/1

Request:
```
curl http://localhost:5000/1
```

Response:
```
{
        "id": 1,
        "cafe_username": "<cafe_username>"
        "cafe": "<cafe>",
        "location": "<location>",
        "open": "<open>"
        "close": "<close>"
        "coffee_rating": "<coffee_rating>"
        "wifi_rating": "<wifi_rating>"
        "power_rating": "<power_rating>"
}
```

### POST /add/cafe-shop/<cafe_username>

Request:
```
curl -X POST -H "Content-Type: application/json" -d '{"id":"id", "cafe": "New cafe name", "cafe_username": "New cafe username", "location": "location"}' http://localhost:5000/add/cafe-shop/<username>
```

Response:
```
{
        "id": "new  ID",cafe shop
        "cafe_username": "<cafe_username>
        "cafe": "<cafe>",
        "open": "<open>",
        "close": "<close>"
}
```

### PATCH /update/cafe-shop/3

Request:
```
curl -X PATCH -H "Content-Type: application/json" -d '{"cafe": "New cafe name", "Message": "name entry updated successfully"}' http://localhost:5000/update/user/3
```

Response:
```
{
         "id": "new  ID",cafe shop
        "cafe_username": "<cafe_username>
        "cafe": "<cafe>",
        "open": "<open>",
        "close": "<close>"
}
```

### DELETE /delete/cafe-shop/3

Request:
```
curl -X DELETE http://localhost:5000/delete/user/3
```

Response:
```
{
    "message": "Cafe shop with ID 3 has been deleted successfully"
}
```

## License

This project is licensed under the MIT License