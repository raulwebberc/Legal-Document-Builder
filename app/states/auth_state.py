import reflex as rx
import hashlib
import asyncio
import app.db as db


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    login_error: str = ""
    is_authenticated: bool = False
    current_user: dict[str, str] = {}
    is_loading: bool = False

    @rx.event
    def set_username(self, val: str):
        self.username = val

    @rx.event
    def set_password(self, val: str):
        self.password = val

    @rx.event
    async def login(self):
        self.is_loading = True
        self.login_error = ""
        yield
        await asyncio.sleep(0.5)
        user = db.get_user_by_username(self.username)
        if user:
            hashed_pass = hashlib.sha256(self.password.encode()).hexdigest()
            if user["password_hash"] == hashed_pass:
                self.is_authenticated = True
                self.current_user = {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"],
                }
                self.is_loading = False
                self.password = ""
                yield rx.redirect("/")
                return
        self.login_error = "Invalid username or password."
        self.is_loading = False

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.current_user = {}
        self.username = ""
        self.password = ""
        return rx.redirect("/login")

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.var
    def is_admin(self) -> bool:
        return self.current_user.get("role") == "admin"

    @rx.var
    def display_name(self) -> str:
        return self.current_user.get("username", "Guest")