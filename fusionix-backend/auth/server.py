import os
import jwt
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from utils import createJWT

server = Flask(__name__)
mysql = MySQL(server) 

# Configure MySQL connection
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))



@server.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()


    # Check if all required fields are provided
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Please provide both email and password"}), 400

    email = data['email']
    password = data['password']

    try:
        # Check if the user already exists
        cursor = mysql.connection.cursor()
        query = "SELECT email FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        # Insert the new user into the database with the plain password
        insert_query = "INSERT INTO user (email, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (email, password))
        mysql.connection.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Database error", "error": str(e)}), 500


@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return jsonify({"message": "Please provide credentials"}), 401

    try:
        # Check db for username and password
        cursor = mysql.connection.cursor()
        query = "SELECT email, password FROM user WHERE email = %s"
        cursor.execute(query, (auth.username,))
        
        user_row = cursor.fetchone()
        if user_row:
            email, password = user_row
            if email == auth.username and password == auth.password:
                return jsonify({"token": createJWT(auth.username, os.environ.get("JWT_SECRET"), True)}), 200
            else:
                return jsonify({"message": "Invalid Credentials"}), 401
        else:
            return jsonify({"message": "Invalid Credentials"}), 401
    except Exception as e:
        print(f"Error: {str(e)}")

        return jsonify({"message": "Database error", "error": str(e)}), 500

@server.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers.get('Authorization')
    
    if not encoded_jwt:
        return jsonify({"message": "Missing credentials"}), 401
    
    try:
        # Decode JWT
        encoded_jwt = encoded_jwt.split(" ")[1]  # Extract token part after 'Bearer'
        decoded = jwt.decode(encoded_jwt, os.environ.get('JWT_SECRET'), algorithms=['HS256'])
        return jsonify(decoded), 200
    except jwt.ExpiredSignatureError:
        print("Error: Token Expired")
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        print("Error: Not Authorized")
        return jsonify({"message": "Not authorized"}), 403
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Invalid token", "error": str(e)}), 403


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
