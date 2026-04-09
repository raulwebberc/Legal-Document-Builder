import reflex as rx
from app.pages.entities import entities_page
from app.pages.templates import templates_page
from app.components.sidebar import layout
from app.states.app_state import AppState
from app.states.document_state import DocumentState


def stat_card(title: str, value: rx.Var, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(title, class_name="text-sm font-medium text-[#525252]"),
            rx.icon(icon, class_name="h-5 w-5 text-[#0f62fe]"),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.p(value, class_name="text-3xl font-semibold text-[#161616]"),
        class_name="bg-white p-6 border border-[#e5e5e5] rounded-sm shadow-sm",
    )


def index() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h1(
                "LegalDoc IDE",
                class_name="text-3xl font-normal text-[#161616] tracking-tight mb-2",
            ),
            rx.el.p(
                "Manage your legal data models, templates, and documents.",
                class_name="text-[#525252] mb-8",
            ),
            rx.el.div(
                stat_card("Total Entities", AppState.entities.length(), "database"),
                stat_card("Total Templates", AppState.templates.length(), "file-text"),
                stat_card(
                    "Total Documents", DocumentState.documents.length(), "folder"
                ),
                stat_card(
                    "Completed Documents",
                    DocumentState.documents.length(),
                    "message_circle_check",
                ),
                class_name="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Recent Documents", class_name="text-xl font-semibold mb-4"
                        ),
                        rx.el.a(
                            "View All",
                            href="/documents",
                            class_name="text-sm text-[#0f62fe] hover:underline",
                        ),
                        class_name="flex justify-between items-center",
                    ),
                    rx.el.div(
                        "View your latest documents in the documents tab.",
                        class_name="text-[#525252] italic p-6 bg-white border border-[#e5e5e5] rounded-sm shadow-sm",
                    ),
                    class_name="col-span-2",
                ),
                rx.el.div(
                    rx.el.h2("Quick Actions", class_name="text-xl font-semibold mb-4"),
                    rx.el.div(
                        rx.el.a(
                            rx.el.div(
                                rx.icon(
                                    "plus", class_name="h-5 w-5 text-[#0f62fe] mb-2"
                                ),
                                rx.el.h3(
                                    "New Document",
                                    class_name="font-medium text-[#161616]",
                                ),
                                rx.el.p(
                                    "Create from a template",
                                    class_name="text-xs text-[#525252]",
                                ),
                            ),
                            href="/documents",
                            class_name="block p-4 bg-white border border-[#e5e5e5] hover:border-[#0f62fe] rounded-sm shadow-sm transition-colors",
                        ),
                        rx.el.a(
                            rx.el.div(
                                rx.icon(
                                    "file-plus",
                                    class_name="h-5 w-5 text-[#0f62fe] mb-2",
                                ),
                                rx.el.h3(
                                    "New Template",
                                    class_name="font-medium text-[#161616]",
                                ),
                                rx.el.p(
                                    "Design a new format",
                                    class_name="text-xs text-[#525252]",
                                ),
                            ),
                            href="/templates",
                            class_name="block p-4 bg-white border border-[#e5e5e5] hover:border-[#0f62fe] rounded-sm shadow-sm transition-colors",
                        ),
                        rx.el.a(
                            rx.el.div(
                                rx.icon(
                                    "bot", class_name="h-5 w-5 text-[#0f62fe] mb-2"
                                ),
                                rx.el.h3(
                                    "AI Assistant",
                                    class_name="font-medium text-[#161616]",
                                ),
                                rx.el.p(
                                    "Get help generating docs",
                                    class_name="text-xs text-[#525252]",
                                ),
                            ),
                            href="/ai-assistant",
                            class_name="block p-4 bg-white border border-[#e5e5e5] hover:border-[#0f62fe] rounded-sm shadow-sm transition-colors",
                        ),
                        rx.el.a(
                            rx.el.div(
                                rx.icon(
                                    "database", class_name="h-5 w-5 text-[#0f62fe] mb-2"
                                ),
                                rx.el.h3(
                                    "Manage Entities",
                                    class_name="font-medium text-[#161616]",
                                ),
                                rx.el.p(
                                    "Edit data models",
                                    class_name="text-xs text-[#525252]",
                                ),
                            ),
                            href="/entities",
                            class_name="block p-4 bg-white border border-[#e5e5e5] hover:border-[#0f62fe] rounded-sm shadow-sm transition-colors",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    class_name="col-span-1",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
            ),
            class_name="p-8 max-w-7xl mx-auto animate-fade-in",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Outfit:wght@300;400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.pages.documents import documents_page
from app.pages.ai_assistant import ai_assistant_page
from app.pages.landing import landing_page
from app.pages.login import login_page
from app.pages.users import users_page
from app.states.auth_state import AuthState
from app.states.user_state import UserState
import app.db as db

app.add_page(index, route="/", on_load=[AuthState.check_auth, AppState.load_data])
app.add_page(landing_page, route="/landing")
app.add_page(login_page, route="/login")
app.add_page(
    entities_page, route="/entities", on_load=[AuthState.check_auth, AppState.load_data]
)
app.add_page(
    templates_page,
    route="/templates",
    on_load=[AuthState.check_auth, AppState.load_data],
)
app.add_page(
    documents_page,
    route="/documents",
    on_load=[AuthState.check_auth, AppState.load_data, DocumentState.load_documents],
)
app.add_page(ai_assistant_page, route="/ai-assistant", on_load=AuthState.check_auth)
app.add_page(
    users_page, route="/users", on_load=[AuthState.check_auth, UserState.load_users]
)