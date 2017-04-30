import jwt
from src.common.authconfig import jwtsecret, jwtalgorithm

class JwtManager:

    def generate(self, user):
        authInfo = {
           "id": user.get_id(),
           "login": user.login,
        }
        return jwt.encode(authInfo, jwtsecret, algorithm=jwtalgorithm)

    def decodeToken(self, token):
        return jwt.decode(token, jwtsecret, algorithm=jwtalgorithm)

    def authenticate(self, token):
        try:
            authInfo = self.decodeToken(token)
        except:
            return False
        if 'login' not in authInfo or 'id' not in authInfo:
            return False
        return True
