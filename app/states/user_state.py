import reflex as rx
import hashlib
import uuid
from datetime import datetime
import app.db as db
from app.states.auth_state import AuthState


class UserState(rx.State):
    users: list[dict] = []
    is_creating_user: bool = False
    editing_user_id: str = ""
    edit_username: str = ""
    edit_password: str = ""
    edit_role: str = "user"
    confirm_delete_user_id: str = ""
    current_password: str = ""
    new_password: str = ""
    confirm_new_password: str = ""

    @rx.event
    def load_users(self):
        self.users = db.get_all_users()

    @rx.event
    def open_create_user(self):
        self.is_creating_user = True
        self.editing_user_id = ""
        self.edit_username = ""
        self.edit_password = ""
        self.edit_role = "user"

    @rx.event
    def open_edit_user(self, user_id: str):
        for user in self.users:
            if user["id"] == user_id:
                self.editing_user_id = user_id
                self.edit_username = user["username"]
                self.edit_role = user["role"]
                self.edit_password = ""
                self.is_creating_user = True
                break

    @rx.event
    def close_user_modal(self):
        self.is_creating_user = False
        self.editing_user_id = ""

    @rx.event
    def set_edit_username(self, val: str):
        self.edit_username = val

    @rx.event
    def set_edit_password(self, val: str):
        self.edit_password = val

    @rx.event
    def set_edit_role(self, val: str):
        self.edit_role = val

    @rx.event
    def save_user(self):
        if not self.edit_username:
            return rx.toast("Username is required", type="error")
        if not self.editing_user_id and (not self.edit_password):
            return rx.toast("Password is required for new users", type="error")
        user_data = {"username": self.edit_username, "role": self.edit_role}
        if self.editing_user_id:
            user_data["id"] = self.editing_user_id
            if self.edit_password:
                user_data["password_hash"] = hashlib.sha256(
                    self.edit_password.encode()
                ).hexdigest()
            else:
                for u in self.users:
                    if u["id"] == self.editing_user_id:
                        user_data["password_hash"] = u["password_hash"]
                        user_data["created_at"] = u.get("created_at", "")
                        break
        else:
            user_data["id"] = str(uuid.uuid4())
            user_data["password_hash"] = hashlib.sha256(
                self.edit_password.encode()
            ).hexdigest()
            user_data["created_at"] = datetime.now().strftime("%Y-%m-%d")
        db.save_user(user_data)
        self.load_users()
        self.close_user_modal()
        yield rx.toast("User saved successfully")

    @rx.event
    def confirm_delete_user(self, user_id: str):
        self.confirm_delete_user_id = user_id

    @rx.event
    def cancel_delete(self):
        self.confirm_delete_user_id = ""

    @rx.event
    async def delete_user(self):
        auth_state = await self.get_state(AuthState)
        if self.confirm_delete_user_id == auth_state.current_user.get("id"):
            self.confirm_delete_user_id = ""
            yield rx.toast("Cannot delete yourself", type="error")
            return
        if self.confirm_delete_user_id:
            db.delete_user(self.confirm_delete_user_id)
            self.confirm_delete_user_id = ""
            self.load_users()
            yield rx.toast("User deleted")

    @rx.event
    def set_current_password(self, val: str):
        self.current_password = val

    @rx.event
    def set_new_password(self, val: str):
        self.new_password = val

    @rx.event
    def set_confirm_new_password(self, val: str):
        self.confirm_new_password = val

    @rx.event
    async def change_password(self):
        if (
            not self.current_password
            or not self.new_password
            or (not self.confirm_new_password)
        ):
            yield rx.toast("All fields are required", type="error")
            return
        if self.new_password != self.confirm_new_password:
            yield rx.toast("New passwords do not match", type="error")
            return
        auth_state = await self.get_state(AuthState)
        user_id = auth_state.current_user.get("id")
        if not user_id:
            yield rx.toast("User not authenticated", type="error")
            return
        user = db.get_user_by_username(auth_state.current_user.get("username"))
        if not user:
            yield rx.toast("User not found", type="error")
            return
        current_hash = hashlib.sha256(self.current_password.encode()).hexdigest()
        if current_hash != user["password_hash"]:
            yield rx.toast("Incorrect current password", type="error")
            return
        new_hash = hashlib.sha256(self.new_password.encode()).hexdigest()
        db.update_user_password(user_id, new_hash)
        self.current_password = ""
        self.new_password = ""
        self.confirm_new_password = ""
        yield rx.toast("Password updated successfully")