from app import db
from datetime import datetime
from dataclasses import dataclass
from .database import get_db



class InvalidTokens(db.Model):
    __tablename__ = "invalidtokens"  # Specify the table name here

    token = db.Column(db.String(255), primary_key=True)
    blacklisted_on = db.Column(db.String(255), primary_key=True)

@dataclass
class BlackJWToken:
    token: str
    blacklisted_on: datetime = datetime.now()
    id: int = -1

    def commit(self) -> None:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO invalidtokens (token, blacklisted_on) VALUES (%s, %s)",
                (self.token, self.blacklisted_on),
            )
            db.commit()  # You should commit the transaction
            cursor.close()

    def is_blacklisted(self) -> bool:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT token FROM invalidtokens WHERE token = %s",
            (self.token,)
        )

        result = cursor.fetchone()
        cursor.close()
        
        return bool(result)  # Check if the token was found in the database
