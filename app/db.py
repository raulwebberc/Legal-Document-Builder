import sqlite3
import json
import os
import hashlib
from typing import Any

DB_PATH = "legaldoc.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        created_at TEXT DEFAULT ''
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS entities (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        icon TEXT NOT NULL,
        description TEXT DEFAULT '',
        attributes TEXT NOT NULL DEFAULT '[]'
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS templates (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT 'Contract',
        description TEXT DEFAULT '',
        content TEXT DEFAULT '',
        last_modified TEXT DEFAULT ''
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        template_id TEXT DEFAULT '',
        status TEXT NOT NULL DEFAULT 'draft',
        created_at TEXT DEFAULT ''
    )""")
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (id, username, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
            ("1", "admin", admin_hash, "admin", "2024-01-01"),
        )
    cursor.execute("SELECT COUNT(*) FROM entities")
    if cursor.fetchone()[0] == 0:
        entities = [
            {
                "id": "1",
                "name": "Person",
                "icon": "user",
                "description": "Individual person details",
                "attributes": [
                    {"name": "Full Name", "type": "text", "required": True},
                    {"name": "ID Number", "type": "text", "required": True},
                    {"name": "Date of Birth", "type": "date", "required": False},
                    {"name": "Address", "type": "address", "required": True},
                    {"name": "Email", "type": "email", "required": False},
                    {"name": "Phone", "type": "phone", "required": False},
                ],
            },
            {
                "id": "2",
                "name": "Company",
                "icon": "building",
                "description": "Corporate entity details",
                "attributes": [
                    {"name": "Legal Name", "type": "text", "required": True},
                    {"name": "Trade Name", "type": "text", "required": False},
                    {"name": "Registration Number", "type": "text", "required": True},
                    {"name": "Tax ID", "type": "text", "required": True},
                    {"name": "Address", "type": "address", "required": True},
                    {"name": "Representative", "type": "text", "required": True},
                ],
            },
            {
                "id": "3",
                "name": "Property",
                "icon": "home",
                "description": "Real estate property details",
                "attributes": [
                    {"name": "Address", "type": "address", "required": True},
                    {"name": "Registration Number", "type": "text", "required": True},
                    {"name": "Area", "type": "number", "required": True},
                    {"name": "Type", "type": "text", "required": False},
                    {"name": "Owner", "type": "text", "required": True},
                ],
            },
            {
                "id": "4",
                "name": "Vehicle",
                "icon": "car",
                "description": "Vehicle registration details",
                "attributes": [
                    {"name": "Make", "type": "text", "required": True},
                    {"name": "Model", "type": "text", "required": True},
                    {"name": "Year", "type": "number", "required": True},
                    {"name": "Plate Number", "type": "text", "required": True},
                    {"name": "VIN", "type": "text", "required": True},
                    {"name": "Owner", "type": "text", "required": True},
                ],
            },
        ]
        for e in entities:
            save_entity(e)
        templates = [
            {
                "id": "1",
                "name": "Non-Disclosure Agreement",
                "category": "Agreement",
                "description": "Standard mutual NDA",
                "content": "This Non-Disclosure Agreement is entered into by and between {{Person.Full Name}} and {{Company.Legal Name}}...",
                "last_modified": "2023-10-25",
            },
            {
                "id": "2",
                "name": "Power of Attorney",
                "category": "Authorization",
                "description": "General power of attorney",
                "content": "I, {{Person.Full Name}}, residing at {{Person.Address}}, hereby appoint...",
                "last_modified": "2023-10-26",
            },
            {
                "id": "3",
                "name": "Lease Agreement",
                "category": "Contract",
                "description": "Residential property lease",
                "content": "This Lease Agreement is made between {{Company.Legal Name}} (Landlord) and {{Person.Full Name}} (Tenant) for the property located at {{Property.Address}}...",
                "last_modified": "2023-10-27",
            },
        ]
        for t in templates:
            save_template(t)
        documents = [
            {
                "id": "1",
                "name": "Acme Corp NDA",
                "template_id": "1",
                "status": "completed",
                "created_at": "2023-10-28",
            },
            {
                "id": "2",
                "name": "Jane Doe Lease",
                "template_id": "3",
                "status": "in-progress",
                "created_at": "2023-10-29",
            },
        ]
        for d in documents:
            save_document(d)
    conn.commit()
    conn.close()


def get_all_entities() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entities")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "icon": row["icon"],
            "description": row["description"],
            "attributes": json.loads(row["attributes"]),
        }
        for row in rows
    ]


def save_entity(entity: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO entities (id, name, icon, description, attributes) VALUES (?, ?, ?, ?, ?)",
        (
            entity["id"],
            entity["name"],
            entity["icon"],
            entity.get("description", ""),
            json.dumps(entity.get("attributes", [])),
        ),
    )
    conn.commit()
    conn.close()


def delete_entity(entity_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entities WHERE id = ?", (entity_id,))
    conn.commit()
    conn.close()


def get_all_templates() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM templates")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "description": row["description"],
            "content": row["content"],
            "last_modified": row["last_modified"],
        }
        for row in rows
    ]


def save_template(template: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO templates (id, name, category, description, content, last_modified) VALUES (?, ?, ?, ?, ?, ?)",
        (
            template["id"],
            template["name"],
            template.get("category", "Contract"),
            template.get("description", ""),
            template.get("content", ""),
            template.get("last_modified", ""),
        ),
    )
    conn.commit()
    conn.close()


def delete_template(template_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))
    conn.commit()
    conn.close()


def get_all_documents() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "template_id": row["template_id"],
            "status": row["status"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def save_document(doc: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO documents (id, name, template_id, status, created_at) VALUES (?, ?, ?, ?, ?)",
        (
            doc["id"],
            doc["name"],
            doc.get("template_id", ""),
            doc.get("status", "draft"),
            doc.get("created_at", ""),
        ),
    )
    conn.commit()
    conn.close()


def delete_document(doc_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()


def get_user_by_username(username: str) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_all_users() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_user(user: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO users (id, username, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
        (
            user["id"],
            user["username"],
            user["password_hash"],
            user.get("role", "user"),
            user.get("created_at", ""),
        ),
    )
    conn.commit()
    conn.close()


def delete_user(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def update_user_password(user_id: str, password_hash: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id)
    )
    conn.commit()
    conn.close()