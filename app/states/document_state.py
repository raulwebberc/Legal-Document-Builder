import reflex as rx
from typing import TypedDict
import re
from datetime import datetime
from app.states.app_state import AppState, Document, Template
import app.db as db


class DocumentState(rx.State):
    documents: list[Document] = []
    is_builder_open: bool = False
    document_step: int = 1
    selected_template_id: str = ""
    current_doc_name: str = "New Document"
    entity_field_values: dict[str, str] = {}

    @rx.event
    def load_documents(self):
        self.documents = db.get_all_documents()

    @rx.event
    def open_builder(self):
        self.is_builder_open = True
        self.document_step = 1
        self.selected_template_id = ""
        self.entity_field_values = {}
        self.current_doc_name = "New Document"

    @rx.event
    def close_builder(self):
        self.is_builder_open = False

    @rx.event
    def set_step(self, step: int):
        self.document_step = step

    @rx.event
    def select_template(self, template_id: str):
        self.selected_template_id = template_id
        self.document_step = 2

    @rx.event
    def update_field(self, key: str, value: str):
        self.entity_field_values[key] = value

    @rx.event
    def save_document(self, status: str):
        new_doc: Document = {
            "id": str(len(self.documents) + 1),
            "name": self.current_doc_name,
            "template_id": self.selected_template_id,
            "status": status,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        }
        self.documents.append(new_doc)
        db.save_document(new_doc)
        self.is_builder_open = False