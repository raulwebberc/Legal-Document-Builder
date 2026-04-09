import reflex as rx
from typing import TypedDict, Any
from datetime import datetime
import app.db as db


class Attribute(TypedDict):
    name: str
    type: str
    required: bool


class EntityType(TypedDict):
    id: str
    name: str
    icon: str
    description: str
    attributes: list[Attribute]


class Template(TypedDict):
    id: str
    name: str
    category: str
    description: str
    content: str
    template_data: str
    last_modified: str


class Document(TypedDict):
    id: str
    name: str
    template_id: str
    status: str
    created_at: str


class AppState(rx.State):
    """
    # AppState for LegalDoc IDE
    # Forces recompilation of the state module to refresh cached structures.
    """

    sidebar_collapsed: bool = False
    current_path: str = "/"
    entities: list[EntityType] = []
    templates: list[Template] = []
    editing_entity_id: str = ""
    is_creating_entity: bool = False
    edit_entity_name: str = ""
    edit_entity_icon: str = "user"
    edit_entity_description: str = ""
    edit_entity_attributes: list[Attribute] = []
    is_adding_inline_attribute: dict[str, bool] = {}
    inline_attr_name: str = ""
    inline_attr_type: str = "text"
    inline_attr_required: bool = False
    confirm_delete_entity_id: str = ""
    confirm_delete_template_id: str = ""
    entity_search: str = ""

    @rx.event
    def load_data(self):
        try:
            db.init_db()
            self.entities = db.get_all_entities()
            self.templates = db.get_all_templates()
        except Exception as e:
            import logging

            logging.exception(f"Error initializing database: {e}")

    @rx.var
    def filtered_entities(self) -> list[EntityType]:
        if not self.entity_search:
            return self.entities
        search_lower = self.entity_search.lower()
        return [e for e in self.entities if search_lower in e["name"].lower()]

    @rx.event
    def get_template_usage_count(self, entity_name: str) -> int:
        count = 0
        placeholder = f"{{{{{entity_name}."
        for t in self.templates:
            if placeholder in t["content"]:
                count += 1
        return count

    @rx.event
    def set_entity_search(self, val: str):
        self.entity_search = val

    @rx.event
    def open_create_entity(self):
        self.is_creating_entity = True
        self.editing_entity_id = ""
        self.edit_entity_name = ""
        self.edit_entity_icon = "user"
        self.edit_entity_description = ""
        self.edit_entity_attributes = [{"name": "", "type": "text", "required": False}]

    @rx.event
    def open_edit_entity(self, entity_id: str):
        for e in self.entities:
            if e["id"] == entity_id:
                self.editing_entity_id = entity_id
                self.edit_entity_name = e["name"]
                self.edit_entity_icon = e["icon"]
                self.edit_entity_description = e["description"]
                self.edit_entity_attributes = e["attributes"].copy()
                self.is_creating_entity = True
                break

    @rx.event
    def duplicate_entity(self, entity_id: str):
        import uuid

        for e in self.entities:
            if e["id"] == entity_id:
                new_entity = e.copy()
                new_entity["id"] = str(uuid.uuid4())
                new_entity["name"] = f"{e['name']} (Copy)"
                self.entities.append(new_entity)
                db.save_entity(new_entity)
                yield rx.toast(f"Duplicated {e['name']}")
                break

    @rx.event
    def close_entity_modal(self):
        self.is_creating_entity = False
        self.editing_entity_id = ""

    @rx.event
    def set_edit_entity_name(self, val: str):
        self.edit_entity_name = val

    @rx.event
    def set_edit_entity_icon(self, val: str):
        self.edit_entity_icon = val

    @rx.event
    def set_edit_entity_description(self, val: str):
        self.edit_entity_description = val

    @rx.event
    def add_edit_attribute(self):
        self.edit_entity_attributes.append(
            {"name": "", "type": "text", "required": False}
        )

    @rx.event
    def remove_edit_attribute(self, idx: int):
        if 0 <= idx < len(self.edit_entity_attributes):
            self.edit_entity_attributes.pop(idx)

    @rx.event
    def update_edit_attribute_name(self, idx: int, val: str):
        if 0 <= idx < len(self.edit_entity_attributes):
            self.edit_entity_attributes[idx]["name"] = val

    @rx.event
    def update_edit_attribute_type(self, idx: int, val: str):
        if 0 <= idx < len(self.edit_entity_attributes):
            self.edit_entity_attributes[idx]["type"] = val

    @rx.event
    def update_edit_attribute_required(self, idx: int, val: bool):
        if 0 <= idx < len(self.edit_entity_attributes):
            self.edit_entity_attributes[idx]["required"] = val

    @rx.event
    def save_entity(self):
        import uuid

        if not self.edit_entity_name:
            return rx.toast("Entity name is required", type="error")
        entity_data = {
            "id": self.editing_entity_id
            if self.editing_entity_id
            else str(uuid.uuid4()),
            "name": self.edit_entity_name,
            "icon": self.edit_entity_icon,
            "description": self.edit_entity_description,
            "attributes": self.edit_entity_attributes.copy(),
        }
        if self.editing_entity_id:
            for i, e in enumerate(self.entities):
                if e["id"] == self.editing_entity_id:
                    self.entities[i] = entity_data
                    break
        else:
            self.entities.append(entity_data)
        db.save_entity(entity_data)
        self.close_entity_modal()
        yield rx.toast("Entity saved successfully")

    @rx.event
    def confirm_delete_entity(self, entity_id: str):
        self.confirm_delete_entity_id = entity_id

    @rx.event
    def cancel_delete(self):
        self.confirm_delete_entity_id = ""

    @rx.event
    def delete_entity(self):
        if self.confirm_delete_entity_id:
            self.entities = [
                e for e in self.entities if e["id"] != self.confirm_delete_entity_id
            ]
            db.delete_entity(self.confirm_delete_entity_id)
            if self.editing_entity_id == self.confirm_delete_entity_id:
                self.close_entity_modal()
            self.confirm_delete_entity_id = ""
            yield rx.toast("Entity deleted")

    @rx.event
    def duplicate_template(self, template_id: str):
        import uuid
        from datetime import datetime

        for t in self.templates:
            if t["id"] == template_id:
                new_template = t.copy()
                new_template["id"] = str(uuid.uuid4())
                new_template["name"] = f"{t['name']} (Copy)"
                new_template["last_modified"] = datetime.now().strftime("%Y-%m-%d")
                self.templates.append(new_template)
                db.save_template(new_template)
                yield rx.toast(f"Duplicated {t['name']}")
                break

    @rx.event
    def confirm_delete_template(self, template_id: str):
        self.confirm_delete_template_id = template_id

    @rx.event
    def cancel_delete_template(self):
        self.confirm_delete_template_id = ""

    @rx.event
    def delete_template(self):
        if self.confirm_delete_template_id:
            self.templates = [
                t for t in self.templates if t["id"] != self.confirm_delete_template_id
            ]
            db.delete_template(self.confirm_delete_template_id)
            self.confirm_delete_template_id = ""
            yield rx.toast("Template deleted")

    @rx.event
    def start_inline_add(self, entity_id: str):
        self.is_adding_inline_attribute = {entity_id: True}
        self.inline_attr_name = ""
        self.inline_attr_type = "text"
        self.inline_attr_required = False

    @rx.event
    def cancel_inline_add(self, entity_id: str):
        self.is_adding_inline_attribute = {entity_id: False}

    @rx.event
    def set_inline_attr_name(self, val: str):
        self.inline_attr_name = val

    @rx.event
    def set_inline_attr_type(self, val: str):
        self.inline_attr_type = val

    @rx.event
    def set_inline_attr_required(self, val: bool):
        self.inline_attr_required = val

    @rx.event
    def save_inline_attribute(self, entity_id: str):
        if not self.inline_attr_name:
            return rx.toast("Attribute name required", type="error")
        for e in self.entities:
            if e["id"] == entity_id:
                e["attributes"].append(
                    {
                        "name": self.inline_attr_name,
                        "type": self.inline_attr_type,
                        "required": self.inline_attr_required,
                    }
                )
                db.save_entity(e)
                break
        self.cancel_inline_add(entity_id)
        yield rx.toast("Attribute added")

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed

    @rx.event
    def set_path(self, path: str):
        self.current_path = path