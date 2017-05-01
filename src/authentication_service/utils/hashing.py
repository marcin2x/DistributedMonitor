

class PasswordHasher:
    def hash(self, password):
        return generate_password_hash(password)