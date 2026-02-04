from passlib.context import CryptContext

# Set up the encryption algorithm (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str):
        """Hashes a plain-text password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        """Verifies if the plain password matches the stored hash."""
        return pwd_context.verify(plain_password, hashed_password)