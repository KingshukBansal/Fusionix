import os, requests

def login(request):
    auth = request.authorization
    print(auth)
    if not auth:
        return None, ("missing credentials",401)

    basicAuth = (auth.username,auth.password)
    print(basicAuth)
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth = basicAuth
    )
    print(response)
    if response.status_code == 200:
        return response.text, None
    else:
        return None,(response.text, response.status_code)
    

def register(request):
    # Extract user credentials from the request
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return None, ("Please provide both email and password", 400)

    email = data['email']
    password = data['password']

    # Send registration request to the external authentication service
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/register",
        json={"email": email, "password": password}
    )

    if response.status_code == 201:
        # Successfully registered
        return response.text, None
    else:
        # Registration failed
        return None, (response.text, response.status_code)
