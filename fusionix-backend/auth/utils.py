import jwt,datetime

def createJWT(username,secret,authz):
    return jwt.encode(
        {
            "username":username,
            "exp":datetime.datetime.now() + datetime.timedelta(days =1),
            "iat":datetime.datetime.now(),
            "admin":authz

        },
        secret,
        algorithm= "HS256"
    )

