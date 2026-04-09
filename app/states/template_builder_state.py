import reflex as rx
from typing import TypedDict, Any
import uuid
import app.db as db
import logging


class Requirement(TypedDict):
    id: str
    entity_id: str
    attribute_name: str
    required: bool


class Paragraph(TypedDict):
    id: str
    title: str
    example_text: str
    requirements: list[Requirement]


class TemplateEntityAttribute(TypedDict):
    name: str
    type: str
    required: bool


class TemplateEntity(TypedDict):
    id: str
    name: str
    type: str
    attributes: list[TemplateEntityAttribute]


class GlobalRequirement(TypedDict):
    id: str
    name: str
    type: str
    description: str


class TemplateBuilderState(rx.State):
    template_name: str = ""
    template_category: str = "Contract"
    template_description: str = ""
    paragraphs: list[Paragraph] = []
    template_entities: list[TemplateEntity] = []
    global_requirements: list[GlobalRequirement] = []
    is_creating_entity: bool = False
    new_entity_name: str = ""
    new_entity_type: str = "Person"
    new_entity_attributes: list[TemplateEntityAttribute] = []
    available_entity_types_list: list[dict[str, str | list[dict[str, str | bool]]]] = []
    selected_entity_type_attributes: list[dict[str, str | bool]] = []
    is_builder_active: bool = False
    show_preview: bool = False
    editing_template_id: str = ""

    @rx.var
    async def available_entity_types(self) -> list[str]:
        from app.states.app_state import AppState

        app_state = await self.get_state(AppState)
        return [e["name"] for e in app_state.entities]

    @rx.event
    async def open_builder(self):
        self.is_builder_active = True
        self.editing_template_id = ""
        self.template_name = ""
        self.template_category = "Contract"
        self.template_description = ""
        self.global_requirements = []
        self.paragraphs = [
            {
                "id": str(uuid.uuid4()),
                "title": "",
                "example_text": "",
                "requirements": [],
            }
        ]
        self.template_entities = []
        self.is_creating_entity = False
        self.show_preview = False

    @rx.event
    async def open_builder_with_template(self, template: dict[str, str]):
        import json
        from app.states.app_state import AppState

        self.is_builder_active = True
        self.editing_template_id = template["id"]
        self.template_name = template["name"]
        self.template_category = template["category"]
        self.template_description = template["description"]
        template_data_json = template.get("template_data", "")
        if template_data_json:
            try:
                data = json.loads(template_data_json)
                self.paragraphs = data.get("paragraphs", [])
                self.template_entities = data.get("template_entities", [])
                self.global_requirements = data.get("global_requirements", [])
            except Exception:
                logging.exception("Unexpected error")
                template_data_json = ""
        if not template_data_json:
            self.global_requirements = []
            raw_paragraphs = template["content"].split("""

""")
            self.paragraphs = []
            for chunk in raw_paragraphs:
                if chunk.strip():
                    self.paragraphs.append(
                        {
                            "id": str(uuid.uuid4()),
                            "title": "",
                            "example_text": chunk.strip(),
                            "requirements": [],
                        }
                    )
            if len(self.paragraphs) == 0:
                self.paragraphs = [
                    {
                        "id": str(uuid.uuid4()),
                        "title": "",
                        "example_text": "",
                        "requirements": [],
                    }
                ]
            app_state = await self.get_state(AppState)
            self.template_entities = []
            for e in app_state.entities:
                self.template_entities.append(
                    {
                        "id": e["id"],
                        "name": e["name"],
                        "type": e["name"],
                        "attributes": [
                            {
                                "name": a["name"],
                                "type": a["type"],
                                "required": a["required"],
                            }
                            for a in e["attributes"]
                        ],
                    }
                )
        self.is_creating_entity = False
        self.show_preview = False

    @rx.event
    def close_builder(self):
        self.is_builder_active = False
        self.editing_template_id = ""

    @rx.event
    def set_template_name(self, val: str):
        self.template_name = val

    @rx.event
    def set_template_category(self, val: str):
        self.template_category = val

    @rx.event
    def set_template_description(self, val: str):
        self.template_description = val

    @rx.event
    def add_paragraph(self):
        self.paragraphs.append(
            {
                "id": str(uuid.uuid4()),
                "title": "",
                "example_text": "",
                "requirements": [],
            }
        )

    @rx.event
    def remove_paragraph(self, p_id: str):
        self.paragraphs = [p for p in self.paragraphs if p["id"] != p_id]

    @rx.event
    def update_paragraph_title(self, p_id: str, title: str):
        for p in self.paragraphs:
            if p["id"] == p_id:
                p["title"] = title

    @rx.event
    def update_paragraph_text(self, p_id: str, text: str):
        for p in self.paragraphs:
            if p["id"] == p_id:
                p["example_text"] = text

    @rx.event
    def add_global_requirement(self):
        self.global_requirements.append(
            {"id": str(uuid.uuid4()), "name": "", "type": "text", "description": ""}
        )

    @rx.event
    def remove_global_requirement(self, req_id: str):
        self.global_requirements = [
            r for r in self.global_requirements if r["id"] != req_id
        ]

    @rx.event
    def update_global_requirement(self, req_id: str, field: str, value: str):
        for r in self.global_requirements:
            if r["id"] == req_id:
                r[field] = value

    @rx.event
    def move_paragraph_up(self, p_id: str):
        idx = next((i for i, p in enumerate(self.paragraphs) if p["id"] == p_id), -1)
        if idx > 0:
            self.paragraphs[idx], self.paragraphs[idx - 1] = (
                self.paragraphs[idx - 1],
                self.paragraphs[idx],
            )

    @rx.event
    def move_paragraph_down(self, p_id: str):
        idx = next((i for i, p in enumerate(self.paragraphs) if p["id"] == p_id), -1)
        if 0 <= idx < len(self.paragraphs) - 1:
            self.paragraphs[idx], self.paragraphs[idx + 1] = (
                self.paragraphs[idx + 1],
                self.paragraphs[idx],
            )

    @rx.event
    def add_requirement(self, p_id: str):
        for p in self.paragraphs:
            if p["id"] == p_id:
                p["requirements"].append(
                    {
                        "id": str(uuid.uuid4()),
                        "entity_id": "",
                        "attribute_name": "",
                        "required": True,
                    }
                )

    @rx.event
    def remove_requirement(self, p_id: str, r_id: str):
        for p in self.paragraphs:
            if p["id"] == p_id:
                p["requirements"] = [r for r in p["requirements"] if r["id"] != r_id]

    @rx.event
    def update_requirement_entity(self, p_id: str, r_id: str, val: str):
        for p in self.paragraphs:
            if p["id"] == p_id:
                for r in p["requirements"]:
                    if r["id"] == r_id:
                        r["entity_id"] = val
                        r["attribute_name"] = ""

    @rx.event
    def update_requirement_attribute(self, p_id: str, r_id: str, val: str):
        for p in self.paragraphs:
            if p["id"] == p_id:
                for r in p["requirements"]:
                    if r["id"] == r_id:
                        r["attribute_name"] = val

    @rx.event
    def update_requirement_required(self, p_id: str, r_id: str, val: bool):
        for p in self.paragraphs:
            if p["id"] == p_id:
                for r in p["requirements"]:
                    if r["id"] == r_id:
                        r["required"] = val

    @rx.event
    def add_attribute_to_entity(self, entity_id: str):
        for e in self.template_entities:
            if e["id"] == entity_id:
                e["attributes"].append({"name": "", "type": "text", "required": True})

    @rx.event
    def remove_attribute_from_entity(self, entity_id: str, attr_index: int):
        for e in self.template_entities:
            if e["id"] == entity_id:
                if 0 <= attr_index < len(e["attributes"]):
                    e["attributes"].pop(attr_index)

    @rx.event
    def update_entity_attribute(
        self, entity_id: str, attr_index: int, field: str, value: str | bool
    ):
        for e in self.template_entities:
            if e["id"] == entity_id:
                if 0 <= attr_index < len(e["attributes"]):
                    e["attributes"][attr_index][field] = value

    @rx.event
    def update_entity_name(self, entity_id: str, name: str):
        for e in self.template_entities:
            if e["id"] == entity_id:
                e["name"] = name

    @rx.event
    def remove_entity(self, entity_id: str):
        self.template_entities = [
            e for e in self.template_entities if e["id"] != entity_id
        ]
        for p in self.paragraphs:
            for r in p["requirements"]:
                if r["entity_id"] == entity_id:
                    r["entity_id"] = ""
                    r["attribute_name"] = ""

    @rx.event
    async def start_new_entity(self):
        from app.states.app_state import AppState

        app_state = await self.get_state(AppState)
        self.available_entity_types_list = [
            {"name": e["name"], "attributes": e["attributes"]}
            for e in app_state.entities
        ]
        self.is_creating_entity = True
        self.new_entity_name = ""
        self.new_entity_type = (
            self.available_entity_types_list[0]["name"]
            if self.available_entity_types_list
            else "Person"
        )
        yield TemplateBuilderState.populate_attributes_for_type(self.new_entity_type)

    @rx.event
    def populate_attributes_for_type(self, entity_type_name: str):
        matched_type = next(
            (
                e
                for e in self.available_entity_types_list
                if e["name"] == entity_type_name
            ),
            None,
        )
        if matched_type:
            self.selected_entity_type_attributes = [
                {
                    "name": a["name"],
                    "type": a["type"],
                    "selected": True,
                    "required": a.get("required", False),
                }
                for a in matched_type["attributes"]
            ]
            self.new_entity_attributes = [
                {
                    "name": a["name"],
                    "type": str(a["type"]),
                    "required": bool(a.get("required", False)),
                }
                for a in matched_type["attributes"]
            ]

    @rx.event
    def cancel_new_entity(self):
        self.is_creating_entity = False

    @rx.event
    def set_new_entity_name(self, val: str):
        self.new_entity_name = val

    @rx.event
    def set_new_entity_type(self, val: str):
        self.new_entity_type = val
        yield TemplateBuilderState.populate_attributes_for_type(val)

    @rx.event
    def toggle_new_entity_attribute(self, attr_name: str):
        for a in self.selected_entity_type_attributes:
            if a["name"] == attr_name:
                a["selected"] = not a["selected"]
        matched_attr = next(
            (a for a in self.selected_entity_type_attributes if a["name"] == attr_name),
            None,
        )
        if matched_attr:
            if matched_attr["selected"]:
                if not any(
                    (a["name"] == attr_name for a in self.new_entity_attributes)
                ):
                    self.new_entity_attributes.append(
                        {
                            "name": str(matched_attr["name"]),
                            "type": str(matched_attr["type"]),
                            "required": bool(matched_attr["required"]),
                        }
                    )
            else:
                self.new_entity_attributes = [
                    a for a in self.new_entity_attributes if a["name"] != attr_name
                ]

    @rx.event
    def save_entity(self):
        if self.new_entity_name:
            self.template_entities.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": self.new_entity_name,
                    "type": self.new_entity_type,
                    "attributes": self.new_entity_attributes.copy(),
                }
            )
        self.is_creating_entity = False

    @rx.event
    def toggle_preview(self):
        self.show_preview = not self.show_preview

    @rx.event
    async def save_template(self, status: str):
        import json
        from app.states.app_state import AppState
        from datetime import datetime

        content = ""
        for p in self.paragraphs:
            p_text = p["example_text"]
            content += (
                p_text
                + """

"""
            )
        template_data = json.dumps(
            {
                "paragraphs": self.paragraphs,
                "template_entities": self.template_entities,
                "global_requirements": self.global_requirements,
            }
        )
        app_state = await self.get_state(AppState)
        if self.editing_template_id != "":
            for i, t in enumerate(app_state.templates):
                if t["id"] == self.editing_template_id:
                    updated_template = {
                        "id": self.editing_template_id,
                        "name": self.template_name or "Untitled Template",
                        "category": self.template_category,
                        "description": self.template_description,
                        "content": content.strip(),
                        "template_data": template_data,
                        "last_modified": datetime.now().strftime("%Y-%m-%d"),
                    }
                    app_state.templates[i] = updated_template
                    db.save_template(updated_template)
                    break
        else:
            new_template = {
                "id": str(uuid.uuid4()),
                "name": self.template_name or "Untitled Template",
                "category": self.template_category,
                "description": self.template_description,
                "content": content.strip(),
                "template_data": template_data,
                "last_modified": datetime.now().strftime("%Y-%m-%d"),
            }
            app_state.templates.append(new_template)
            db.save_template(new_template)
        self.is_builder_active = False
        self.editing_template_id = ""

    @rx.var
    def preview_content(self) -> str:
        content = ""
        for p in self.paragraphs:
            content += f"[{p['title']}]\n" if p["title"] else ""
            content += (
                p["example_text"]
                + """

"""
            )
        return content