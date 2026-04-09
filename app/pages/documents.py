import reflex as rx
from app.states.app_state import AppState, Document, Template
from app.states.document_state import DocumentState
from app.components.sidebar import layout


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "completed",
            rx.el.span(
                "Completed",
                class_name="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-sm w-fit",
            ),
        ),
        (
            "in-progress",
            rx.el.span(
                "In Progress",
                class_name="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-sm w-fit",
            ),
        ),
        rx.el.span(
            "Draft",
            class_name="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-sm w-fit",
        ),
    )


def document_row(doc: Document) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            doc["name"], class_name="py-4 px-6 text-sm text-[#161616] font-medium"
        ),
        rx.el.td(doc["template_id"], class_name="py-4 px-6 text-sm text-[#525252]"),
        rx.el.td(status_badge(doc["status"]), class_name="py-4 px-6"),
        rx.el.td(doc["created_at"], class_name="py-4 px-6 text-sm text-[#525252]"),
        rx.el.td(
            rx.el.button(
                rx.icon("copy", class_name="h-4 w-4 text-[#0f62fe]"),
                class_name="p-2 hover:bg-[#e5e5e5] rounded-sm transition-colors",
            ),
            class_name="py-4 px-6",
        ),
        class_name="border-b border-[#e5e5e5] hover:bg-[#f4f4f4] transition-colors",
    )


def list_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Documents",
                    class_name="text-3xl font-normal text-[#161616] tracking-tight",
                ),
                rx.el.p(
                    "Manage and create your legal documents.",
                    class_name="text-[#525252] mt-2 text-sm",
                ),
            ),
            rx.el.button(
                "New Document",
                rx.icon("plus", class_name="ml-2 h-4 w-4"),
                on_click=DocumentState.open_builder,
                class_name="flex items-center bg-[#0f62fe] text-white h-[48px] px-4 font-medium hover:bg-[#0353e9] transition-colors rounded-sm shadow-sm",
            ),
            class_name="flex justify-between items-start mb-8",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Name",
                            class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Template",
                            class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Created",
                            class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                        ),
                        class_name="bg-[#f4f4f4] border-b border-[#e5e5e5]",
                    )
                ),
                rx.el.tbody(rx.foreach(DocumentState.documents, document_row)),
                class_name="w-full table-auto",
            ),
            class_name="bg-white border border-[#e5e5e5] rounded-sm overflow-hidden shadow-sm",
        ),
    )


def template_selector(template: Template) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            template["name"], class_name="text-lg font-semibold text-[#161616] mb-2"
        ),
        rx.el.p(template["description"], class_name="text-sm text-[#525252] mb-4"),
        rx.el.button(
            "Use Template",
            on_click=lambda: DocumentState.select_template(template["id"]),
            class_name="w-full bg-[#f4f4f4] text-[#0f62fe] hover:bg-[#e5e5e5] py-2 text-sm font-medium rounded-sm transition-colors",
        ),
        class_name="p-6 border border-[#e5e5e5] rounded-sm hover:border-[#0f62fe] transition-colors bg-white",
    )


def builder_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                "Back to Documents",
                on_click=DocumentState.close_builder,
                class_name="flex items-center text-[#0f62fe] text-sm font-medium hover:underline mb-4",
            ),
            rx.el.h2(
                "Document Builder", class_name="text-2xl font-normal text-[#161616]"
            ),
            class_name="mb-6 border-b border-[#e5e5e5] pb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "1",
                        class_name=rx.cond(
                            DocumentState.document_step >= 1,
                            "bg-[#0f62fe] text-white flex items-center justify-center w-8 h-8 rounded-full text-sm",
                            "bg-[#e5e5e5] text-[#525252] flex items-center justify-center w-8 h-8 rounded-full text-sm",
                        ),
                    ),
                    rx.el.span(
                        "Select Template", class_name="ml-3 text-sm font-medium"
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(class_name="h-[2px] w-12 mx-4 bg-[#e5e5e5]"),
                rx.el.div(
                    rx.el.span(
                        "2",
                        class_name=rx.cond(
                            DocumentState.document_step >= 2,
                            "bg-[#0f62fe] text-white flex items-center justify-center w-8 h-8 rounded-full text-sm",
                            "bg-[#e5e5e5] text-[#525252] flex items-center justify-center w-8 h-8 rounded-full text-sm",
                        ),
                    ),
                    rx.el.span("Fill Details", class_name="ml-3 text-sm font-medium"),
                    class_name="flex items-center",
                ),
                rx.el.div(class_name="h-[2px] w-12 mx-4 bg-[#e5e5e5]"),
                rx.el.div(
                    rx.el.span(
                        "3",
                        class_name=rx.cond(
                            DocumentState.document_step >= 3,
                            "bg-[#0f62fe] text-white flex items-center justify-center w-8 h-8 rounded-full text-sm",
                            "bg-[#e5e5e5] text-[#525252] flex items-center justify-center w-8 h-8 rounded-full text-sm",
                        ),
                    ),
                    rx.el.span("Preview", class_name="ml-3 text-sm font-medium"),
                    class_name="flex items-center",
                ),
                class_name="flex items-center mb-8",
            ),
            rx.match(
                DocumentState.document_step,
                (
                    1,
                    rx.el.div(
                        rx.foreach(AppState.templates, template_selector),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                    ),
                ),
                (
                    2,
                    rx.el.div(
                        rx.el.p(
                            "Please fill in the required fields to generate the document.",
                            class_name="text-[#525252] mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Person Full Name",
                                class_name="block text-sm font-medium text-[#161616] mb-2",
                            ),
                            rx.el.input(
                                on_change=lambda v: DocumentState.update_field(
                                    "Person.Full Name", v
                                ),
                                class_name="w-full h-10 px-4 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none rounded-sm mb-6",
                            ),
                            rx.el.label(
                                "Company Legal Name",
                                class_name="block text-sm font-medium text-[#161616] mb-2",
                            ),
                            rx.el.input(
                                on_change=lambda v: DocumentState.update_field(
                                    "Company.Legal Name", v
                                ),
                                class_name="w-full h-10 px-4 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none rounded-sm mb-6",
                            ),
                            class_name="bg-white p-6 border border-[#e5e5e5] rounded-sm max-w-2xl",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Back",
                                on_click=lambda: DocumentState.set_step(1),
                                class_name="px-4 py-2 bg-[#e5e5e5] hover:bg-[#d1d1d1] text-[#161616] rounded-sm mr-4 transition-colors",
                            ),
                            rx.el.button(
                                "Continue to Preview",
                                on_click=lambda: DocumentState.set_step(3),
                                class_name="px-4 py-2 bg-[#0f62fe] hover:bg-[#0353e9] text-white rounded-sm transition-colors",
                            ),
                            class_name="mt-8",
                        ),
                    ),
                ),
                (
                    3,
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Document Preview",
                                class_name="text-xl font-medium mb-6 font-serif",
                            ),
                            rx.el.p(
                                "This Non-Disclosure Agreement is entered into by and between ",
                                rx.el.span(
                                    DocumentState.entity_field_values[
                                        "Person.Full Name"
                                    ],
                                    class_name="bg-yellow-100",
                                ),
                                " and ",
                                rx.el.span(
                                    DocumentState.entity_field_values[
                                        "Company.Legal Name"
                                    ],
                                    class_name="bg-yellow-100",
                                ),
                                "...",
                                class_name="font-serif text-lg leading-relaxed text-[#161616]",
                            ),
                            class_name="bg-white p-12 border border-[#e5e5e5] rounded-sm shadow-md max-w-4xl mx-auto min-h-[600px]",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Back to Edit",
                                on_click=lambda: DocumentState.set_step(2),
                                class_name="px-4 py-2 bg-[#e5e5e5] hover:bg-[#d1d1d1] text-[#161616] rounded-sm mr-4 transition-colors",
                            ),
                            rx.el.button(
                                "Save as Draft",
                                on_click=lambda: DocumentState.save_document("draft"),
                                class_name="px-4 py-2 bg-[#393939] hover:bg-[#161616] text-white rounded-sm mr-4 transition-colors",
                            ),
                            rx.el.button(
                                "Mark as Complete",
                                on_click=lambda: DocumentState.save_document(
                                    "completed"
                                ),
                                class_name="px-4 py-2 bg-[#198038] hover:bg-[#24a148] text-white rounded-sm transition-colors",
                            ),
                            class_name="mt-8 flex justify-end max-w-4xl mx-auto",
                        ),
                    ),
                ),
                rx.el.div(),
            ),
        ),
    )


def documents_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.cond(DocumentState.is_builder_open, builder_view(), list_view()),
            class_name="p-8 max-w-[1400px] mx-auto animate-fade-in",
        )
    )