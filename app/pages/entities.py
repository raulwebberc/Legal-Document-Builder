import reflex as rx
from app.states.app_state import AppState, EntityType, Attribute
from app.components.sidebar import layout


def type_badge(attr_type: str) -> rx.Component:
    colors = {
        "text": "bg-gray-100 text-gray-700",
        "number": "bg-purple-100 text-purple-700",
        "date": "bg-teal-100 text-teal-700",
        "email": "bg-blue-100 text-blue-700",
        "phone": "bg-green-100 text-green-700",
        "address": "bg-orange-100 text-orange-700",
    }
    return rx.match(
        attr_type,
        (
            "text",
            rx.el.span(
                attr_type,
                class_name=f"px-2 py-0.5 text-xs rounded-full {colors['text']}",
            ),
        ),
        (
            "number",
            rx.el.span(
                attr_type,
                class_name=f"px-2 py-0.5 text-xs rounded-full {colors['number']}",
            ),
        ),
        (
            "date",
            rx.el.span(
                attr_type,
                class_name=f"px-2 py-0.5 text-xs rounded-full {colors['date']}",
            ),
        ),
        (
            "email",
            rx.el.span(
                attr_type,
                class_name=f"px-2 py-0.5 text-xs rounded-full {colors['email']}",
            ),
        ),
        (
            "phone",
            rx.el.span(
                attr_type,
                class_name=f"px-2 py-0.5 text-xs rounded-full {colors['phone']}",
            ),
        ),
        (
            "address",
            rx.el.span(
                attr_type,
                class_name=f"px-2 py-0.5 text-xs rounded-full {colors['address']}",
            ),
        ),
        rx.el.span(
            attr_type,
            class_name="px-2 py-0.5 text-xs rounded-full bg-gray-100 text-gray-700",
        ),
    )


def attribute_row(attr: Attribute) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            attr["name"],
            class_name="text-sm font-medium text-[#161616] truncate flex-1",
        ),
        rx.el.div(type_badge(attr["type"]), class_name="flex items-center"),
        class_name="flex justify-between items-center py-2 border-b border-[#e5e5e5] last:border-0",
    )


def inline_add_form(entity_id: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                placeholder="Name",
                on_change=AppState.set_inline_attr_name,
                class_name="flex-1 h-8 px-2 text-sm bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe]",
                default_value=AppState.inline_attr_name,
            ),
            rx.el.select(
                rx.el.option("text", value="text"),
                rx.el.option("number", value="number"),
                rx.el.option("date", value="date"),
                rx.el.option("email", value="email"),
                rx.el.option("phone", value="phone"),
                rx.el.option("address", value="address"),
                value=AppState.inline_attr_type,
                on_change=AppState.set_inline_attr_type,
                class_name="w-24 h-8 px-1 text-xs bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe] ml-2 appearance-none",
            ),
            class_name="flex items-center mb-2",
        ),
        rx.el.div(
            rx.el.div(class_name="flex-1"),
            rx.el.div(
                rx.el.button(
                    rx.icon("check", class_name="h-4 w-4 text-green-600"),
                    on_click=lambda: AppState.save_inline_attribute(entity_id),
                    class_name="p-1 hover:bg-green-50 rounded",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-4 w-4 text-red-600"),
                    on_click=lambda: AppState.cancel_inline_add(entity_id),
                    class_name="p-1 hover:bg-red-50 rounded ml-1",
                ),
                class_name="flex",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="mt-2 p-2 bg-[#f4f4f4] rounded-sm",
    )


def entity_card(entity: EntityType) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(entity["icon"], class_name="h-6 w-6 text-[#0f62fe] mr-2"),
                    rx.el.h3(
                        entity["name"],
                        class_name="text-lg font-semibold text-[#161616]",
                    ),
                    class_name="flex items-center cursor-pointer",
                    on_click=lambda: AppState.open_edit_entity(entity["id"]),
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.el.button(
                            rx.icon(
                                "gallery_horizontal",
                                class_name="h-5 w-5 text-[#525252]",
                            ),
                            class_name="p-1 hover:bg-[#e5e5e5] rounded-full",
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Edit",
                            on_click=lambda: AppState.open_edit_entity(entity["id"]),
                        ),
                        rx.menu.item(
                            "Duplicate",
                            on_click=lambda: AppState.duplicate_entity(entity["id"]),
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Delete",
                            on_click=lambda: AppState.confirm_delete_entity(
                                entity["id"]
                            ),
                            color="red",
                        ),
                    ),
                ),
                class_name="flex justify-between items-center mb-2",
            ),
            rx.el.p(
                entity["description"],
                class_name="text-sm text-[#525252] mb-4 bg-[#f4f4f4] p-2 rounded-sm",
            ),
            rx.el.div(
                rx.el.span(
                    f"Attributes ({entity['attributes'].length()})",
                    class_name="text-xs font-semibold text-[#525252] uppercase tracking-wider",
                ),
                class_name="mb-2 pb-1 border-b border-[#e5e5e5]",
            ),
            rx.el.div(
                rx.foreach(entity["attributes"], attribute_row),
                class_name="flex-1 overflow-y-auto mb-2 max-h-48",
            ),
            rx.cond(
                AppState.is_adding_inline_attribute.contains(entity["id"])
                & AppState.is_adding_inline_attribute[entity["id"]],
                inline_add_form(entity["id"]),
                rx.el.button(
                    rx.icon("plus", class_name="h-4 w-4 mr-1"),
                    "Add Attribute",
                    on_click=lambda: AppState.start_inline_add(entity["id"]),
                    class_name="flex items-center text-[#0f62fe] text-xs font-medium hover:underline mt-2",
                ),
            ),
            class_name="flex flex-col h-full",
        ),
        rx.el.div(
            rx.el.span("Used in: 3 templates", class_name="text-xs text-[#525252]"),
            class_name="pt-3 mt-4 border-t border-[#e5e5e5] flex justify-between items-center",
        ),
        class_name="bg-white p-5 border border-[#e5e5e5] hover:border-[#0f62fe] hover:shadow-md transition-all duration-200 rounded-sm flex flex-col justify-between h-full min-h-[400px]",
    )


def edit_entity_modal() -> rx.Component:
    return rx.cond(
        AppState.is_creating_entity,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            AppState.editing_entity_id != "",
                            "Edit Entity Type",
                            "New Entity Type",
                        ),
                        class_name="text-xl font-semibold",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=AppState.close_entity_modal,
                        class_name="text-[#525252] hover:text-[#161616]",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Entity Name",
                        class_name="block text-sm font-medium text-[#161616] mb-1",
                    ),
                    rx.el.input(
                        on_change=AppState.set_edit_entity_name,
                        class_name="w-full h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe]",
                        default_value=AppState.edit_entity_name,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Icon",
                        class_name="block text-sm font-medium text-[#161616] mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("User (Person)", value="user"),
                        rx.el.option("Building (Company)", value="building"),
                        rx.el.option("Home (Property)", value="home"),
                        rx.el.option("Car (Vehicle)", value="car"),
                        rx.el.option("File (Document)", value="file-text"),
                        value=AppState.edit_entity_icon,
                        on_change=AppState.set_edit_entity_icon,
                        class_name="w-full h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe] appearance-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Description",
                        class_name="block text-sm font-medium text-[#161616] mb-1",
                    ),
                    rx.el.textarea(
                        on_change=AppState.set_edit_entity_description,
                        class_name="w-full p-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe] resize-none h-20",
                        default_value=AppState.edit_entity_description,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Attributes",
                        class_name="text-base font-semibold mb-3 pb-2 border-b border-[#e5e5e5]",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AppState.edit_entity_attributes,
                            lambda attr, i: rx.el.div(
                                rx.el.input(
                                    placeholder="Attribute Name",
                                    on_change=lambda v: AppState.update_edit_attribute_name(
                                        i, v
                                    ),
                                    class_name="flex-1 h-9 px-2 text-sm bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe]",
                                    default_value=attr["name"],
                                ),
                                rx.el.select(
                                    rx.el.option("text", value="text"),
                                    rx.el.option("number", value="number"),
                                    rx.el.option("date", value="date"),
                                    rx.el.option("email", value="email"),
                                    rx.el.option("phone", value="phone"),
                                    rx.el.option("address", value="address"),
                                    value=attr["type"],
                                    on_change=lambda v: AppState.update_edit_attribute_type(
                                        i, v
                                    ),
                                    class_name="w-24 h-9 px-1 text-xs bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe] ml-2 appearance-none",
                                ),
                                rx.el.button(
                                    rx.icon("trash", class_name="h-4 w-4"),
                                    on_click=lambda: AppState.remove_edit_attribute(i),
                                    class_name="p-2 text-red-500 hover:bg-red-50 rounded",
                                ),
                                class_name="flex items-center mb-2",
                            ),
                        ),
                        class_name="max-h-60 overflow-y-auto pr-2",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="h-4 w-4 mr-2"),
                        "Add Attribute",
                        on_click=AppState.add_edit_attribute,
                        class_name="flex items-center text-[#0f62fe] text-sm font-medium hover:underline mt-3",
                    ),
                ),
                rx.el.div(
                    rx.cond(
                        AppState.editing_entity_id != "",
                        rx.el.button(
                            "Delete Entity",
                            on_click=lambda: AppState.confirm_delete_entity(
                                AppState.editing_entity_id
                            ),
                            class_name="text-red-600 hover:text-red-800 text-sm font-medium",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=AppState.close_entity_modal,
                            class_name="px-4 py-2 text-[#525252] hover:bg-[#e5e5e5] rounded-sm mr-2",
                        ),
                        rx.el.button(
                            "Save Changes",
                            on_click=AppState.save_entity,
                            class_name="px-4 py-2 bg-[#0f62fe] text-white hover:bg-[#0353e9] rounded-sm",
                        ),
                        class_name="flex",
                    ),
                    class_name="flex justify-between items-center mt-8 pt-4 border-t border-[#e5e5e5]",
                ),
                class_name="bg-white w-full max-w-[600px] p-6 rounded-sm shadow-xl",
            ),
            class_name="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4",
        ),
        rx.fragment(),
    )


def delete_confirmation_modal() -> rx.Component:
    return rx.cond(
        AppState.confirm_delete_entity_id != "",
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Delete Entity Type?",
                    class_name="text-lg font-semibold text-[#161616] mb-3",
                ),
                rx.el.p(
                    "Are you sure you want to delete this entity? This action cannot be undone and may affect templates that reference it.",
                    class_name="text-sm text-[#525252] mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=AppState.cancel_delete,
                        class_name="px-4 py-2 text-[#525252] hover:bg-[#e5e5e5] rounded-sm mr-3",
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=AppState.delete_entity,
                        class_name="px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded-sm",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="bg-white w-full max-w-md p-6 rounded-sm shadow-xl",
            ),
            class_name="fixed inset-0 bg-black/50 z-[60] flex items-center justify-center p-4",
        ),
        rx.fragment(),
    )


def entities_page() -> rx.Component:
    return layout(
        rx.el.div(
            edit_entity_modal(),
            delete_confirmation_modal(),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Entity Types",
                        class_name="text-3xl font-normal text-[#161616] tracking-tight",
                    ),
                    rx.el.p(
                        "Define and manage data models used across your document templates.",
                        class_name="text-[#525252] mt-2 text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="h-4 w-4 text-[#8d8d8d] absolute left-3 top-1/2 transform -translate-y-1/2",
                        ),
                        rx.el.input(
                            placeholder="Search entities...",
                            on_change=AppState.set_entity_search,
                            class_name="w-64 h-10 pl-10 pr-4 bg-white border border-[#e5e5e5] focus:outline-none focus:border-[#0f62fe] rounded-sm text-sm",
                            default_value=AppState.entity_search,
                        ),
                        class_name="relative mr-4",
                    ),
                    rx.el.button(
                        "New Entity Type",
                        rx.icon("plus", class_name="ml-2 h-4 w-4"),
                        on_click=AppState.open_create_entity,
                        class_name="flex items-center bg-[#0f62fe] text-white h-[48px] px-4 font-medium hover:bg-[#0353e9] transition-colors rounded-sm shadow-sm",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex flex-col md:flex-row md:justify-between md:items-center mb-8 gap-4",
            ),
            rx.cond(
                AppState.filtered_entities.length() > 0,
                rx.el.div(
                    rx.foreach(AppState.filtered_entities, entity_card),
                    class_name="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                ),
                rx.el.div(
                    rx.icon("database", class_name="h-12 w-12 text-[#c6c6c6] mb-4"),
                    rx.el.h3(
                        "No entities found",
                        class_name="text-lg font-medium text-[#161616]",
                    ),
                    rx.el.p(
                        "Try adjusting your search or create a new entity type.",
                        class_name="text-[#525252]",
                    ),
                    class_name="flex flex-col items-center justify-center p-12 bg-white border border-[#e5e5e5] border-dashed rounded-sm",
                ),
            ),
            class_name="p-8 max-w-[1400px] mx-auto animate-fade-in",
        )
    )