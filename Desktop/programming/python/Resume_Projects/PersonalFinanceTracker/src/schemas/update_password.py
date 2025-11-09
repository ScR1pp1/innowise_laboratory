from pydantic import BaseModel, Field, model_validator
import re


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode='after')
    def validate_password(self):
        password = self.new_password
        if len(password) < 8:
            raise ValueError("Password is too short, minimum 8 symbols")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain digits")
        return self

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords don't match")
        return self
