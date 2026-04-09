import reflex as rx
from app.states.app_state import AppState, Template, EntityType
from app.states.template_builder_state import TemplateBuilderState
from app.components.sidebar import layout


def template_card(template: Template) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        template["category"],
                        class_name="text-xs font-medium bg-[#e0e8ff] text-[#0f62fe] px-2 py-1 rounded-sm mb-3 inline-block",
                    ),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.el.button(
                                rx.icon(
                                    "gallery_horizontal",
                                    class_name="h-5 w-5 text-[#525252]",
                                ),
                                class_name="p-1 hover:bg-[#e5e5e5] rounded-full",
                                on_click=rx.stop_propagation,
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(
                                "Edit",
                                on_click=lambda: TemplateBuilderState.open_builder_with_template(
                                    template
                                ),
                            ),
                            rx.menu.item(
                                "Duplicate",
                                on_click=lambda: AppState.duplicate_template(
                                    template["id"]
                                ),
                            ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Delete",
                                on_click=lambda: AppState.confirm_delete_template(
                                    template["id"]
                                ),
                                color="red",
                            ),
                        ),
                    ),
                    class_name="flex justify-between items-start",
                ),
                rx.el.h3(
                    template["name"],
                    class_name="text-lg font-semibold text-[#161616] mb-2",
                ),
                rx.el.p(
                    template["description"],
                    class_name="text-sm text-[#525252] h-10 line-clamp-2 mb-4",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    f"Updated {template['last_modified']}",
                    class_name="text-xs text-[#525252]",
                ),
                class_name="flex items-center justify-between border-t border-[#e5e5e5] pt-4 mt-2",
            ),
            class_name="flex flex-col h-full",
        ),
        on_click=lambda: TemplateBuilderState.open_builder_with_template(template),
        class_name="bg-white p-6 border border-[#e5e5e5] hover:border-[#0f62fe] hover:shadow-md cursor-pointer transition-all duration-200 rounded-sm focus:outline focus:outline-2 focus:outline-offset-2 focus:outline-[#0f62fe]",
        tabindex="0",
    )


def requirement_row(p_id: str, req: dict) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("Select Entity...", value="", disabled=True),
            rx.el.option("— Global —", value="global"),
            rx.foreach(
                TemplateBuilderState.template_entities,
                lambda e: rx.el.option(e["name"], value=e["id"]),
            ),
            value=req["entity_id"],
            on_change=lambda v: TemplateBuilderState.update_requirement_entity(
                p_id, req["id"], v
            ),
            class_name="w-1/3 h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-sm appearance-none",
        ),
        rx.el.select(
            rx.el.option("Select Attribute...", value="", disabled=True),
            rx.cond(
                req["entity_id"] == "global",
                rx.foreach(
                    TemplateBuilderState.global_requirements,
                    lambda g: rx.el.option(g["name"], value=g["name"]),
                ),
                rx.foreach(
                    TemplateBuilderState.template_entities,
                    lambda e: rx.cond(
                        e["id"] == req["entity_id"],
                        rx.fragment(
                            rx.foreach(
                                e["attributes"],
                                lambda a: rx.cond(
                                    a["name"] != "",
                                    rx.el.option(a["name"], value=a["name"]),
                                    rx.fragment(),
                                ),
                            )
                        ),
                        rx.fragment(),
                    ),
                ),
            ),
            value=req["attribute_name"],
            on_change=lambda v: TemplateBuilderState.update_requirement_attribute(
                p_id, req["id"], v
            ),
            class_name="w-1/3 h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-sm appearance-none",
        ),
        rx.el.label(
            rx.el.input(
                type="checkbox",
                checked=req["required"].to(bool),
                on_change=lambda v: TemplateBuilderState.update_requirement_required(
                    p_id, req["id"], v
                ),
                class_name="mr-2",
            ),
            "Required",
            class_name="flex items-center text-sm text-[#525252] w-1/4",
        ),
        rx.el.button(
            rx.icon("x", class_name="h-4 w-4"),
            on_click=lambda: TemplateBuilderState.remove_requirement(p_id, req["id"]),
            class_name="text-red-500 hover:text-red-700 p-2",
        ),
        class_name="flex items-center gap-4 mb-2",
    )


def paragraph_card(p: dict, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    index + 1,
                    class_name="bg-[#0f62fe] text-white w-6 h-6 flex items-center justify-center rounded-full text-xs font-bold mr-3",
                ),
                rx.el.input(
                    placeholder="Section Title (Optional)",
                    on_change=lambda v: TemplateBuilderState.update_paragraph_title(
                        p["id"], v
                    ),
                    class_name="flex-1 h-10 px-3 bg-transparent border-b border-transparent focus:border-[#0f62fe] focus:outline-none font-medium text-[#161616]",
                    default_value=p["title"],
                ),
                class_name="flex items-center flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("arrow-up", class_name="h-4 w-4"),
                    on_click=lambda: TemplateBuilderState.move_paragraph_up(p["id"]),
                    class_name="p-2 text-[#525252] hover:text-[#0f62fe]",
                ),
                rx.el.button(
                    rx.icon("arrow-down", class_name="h-4 w-4"),
                    on_click=lambda: TemplateBuilderState.move_paragraph_down(p["id"]),
                    class_name="p-2 text-[#525252] hover:text-[#0f62fe]",
                ),
                rx.el.button(
                    rx.icon("trash", class_name="h-4 w-4"),
                    on_click=lambda: TemplateBuilderState.remove_paragraph(p["id"]),
                    class_name="p-2 text-red-500 hover:text-red-700 ml-2",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.textarea(
            placeholder="Paste example or reference text for this paragraph here. You can use {{Entity.Attribute}} placeholders.",
            on_change=lambda v: TemplateBuilderState.update_paragraph_text(p["id"], v),
            class_name="w-full min-h-[120px] p-3 bg-[#f4f4f4] border border-[#e5e5e5] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-sm mb-4 resize-y",
            default_value=p["example_text"],
        ),
        rx.el.div(
            rx.el.h4(
                "Requirements", class_name="text-sm font-semibold text-[#161616] mb-3"
            ),
            rx.foreach(p["requirements"], lambda req: requirement_row(p["id"], req)),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add Requirement",
                on_click=lambda: TemplateBuilderState.add_requirement(p["id"]),
                class_name="flex items-center text-[#0f62fe] text-sm font-medium hover:underline mt-2",
            ),
            class_name="bg-white border border-[#e5e5e5] p-4 rounded-sm",
        ),
        class_name="bg-white p-6 border border-[#e5e5e5] rounded-sm mb-6 shadow-sm",
    )


def new_entity_attribute_checklist_item(attr: dict) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            rx.el.input(
                type="checkbox",
                checked=attr["selected"].to(bool),
                on_change=lambda _: TemplateBuilderState.toggle_new_entity_attribute(
                    attr["name"]
                ),
                class_name="mr-3 h-4 w-4 text-[#0f62fe] focus:ring-[#0f62fe] border-gray-300 rounded",
            ),
            rx.el.span(attr["name"], class_name="text-sm text-[#161616] font-medium"),
            class_name="flex items-center flex-1 cursor-pointer",
        ),
        rx.el.span(
            attr["type"],
            class_name="text-[10px] uppercase font-bold text-[#525252] bg-[#f4f4f4] px-2 py-0.5 rounded-sm",
        ),
        class_name="flex items-center justify-between p-2 hover:bg-[#f4f4f4] rounded-sm transition-colors border-b border-[#e5e5e5] last:border-0",
    )


def global_requirement_card(req: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                placeholder="Requirement Name",
                on_change=lambda v: TemplateBuilderState.update_global_requirement(
                    req["id"], "name", v
                ),
                class_name="flex-1 h-9 px-2 text-sm bg-transparent border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none",
                default_value=req["name"],
            ),
            rx.el.button(
                rx.icon("x", class_name="h-4 w-4"),
                on_click=lambda: TemplateBuilderState.remove_global_requirement(
                    req["id"]
                ),
                class_name="text-[#8d8d8d] hover:text-red-500 transition-colors ml-2",
            ),
            class_name="flex items-center mb-2",
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option("text", value="text"),
                rx.el.option("number", value="number"),
                rx.el.option("date", value="date"),
                rx.el.option("list", value="list"),
                rx.el.option("currency", value="currency"),
                value=req["type"],
                on_change=lambda v: TemplateBuilderState.update_global_requirement(
                    req["id"], "type", v
                ),
                class_name="w-full h-8 px-2 text-xs bg-[#f4f4f4] border-b border-[#e5e5e5] rounded-sm appearance-none",
            ),
            class_name="relative mb-2",
        ),
        rx.el.input(
            placeholder="Description / Placeholder hint",
            on_change=lambda v: TemplateBuilderState.update_global_requirement(
                req["id"], "description", v
            ),
            class_name="w-full h-8 px-2 text-xs bg-[#f4f4f4] border-b border-[#e5e5e5] rounded-sm focus:outline-none",
            default_value=req["description"],
        ),
        class_name="bg-white p-3 border-l-4 border-l-[#0f62fe] border-y border-r border-[#e5e5e5] rounded-sm mb-3 shadow-sm transition-all hover:shadow-md",
    )


def new_entity_modal() -> rx.Component:
    return rx.cond(
        TemplateBuilderState.is_creating_entity,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "New Template Entity", class_name="text-lg font-semibold mb-4"
                ),
                rx.el.div(
                    rx.el.label(
                        "Local Label",
                        class_name="block text-xs font-semibold text-[#525252] uppercase mb-1",
                    ),
                    rx.el.input(
                        placeholder="e.g., The Buyer, The Seller",
                        on_change=TemplateBuilderState.set_new_entity_name,
                        class_name="w-full h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-sm mb-4",
                        default_value=TemplateBuilderState.new_entity_name,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Entity Type",
                        class_name="block text-xs font-semibold text-[#525252] uppercase mb-1",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                TemplateBuilderState.available_entity_types,
                                lambda t: rx.el.option(t, value=t),
                            ),
                            value=TemplateBuilderState.new_entity_type,
                            on_change=TemplateBuilderState.set_new_entity_type,
                            class_name="w-full h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-sm appearance-none",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#525252] pointer-events-none",
                        ),
                        class_name="relative mb-6",
                    ),
                ),
                rx.el.h4(
                    "Select Attributes",
                    class_name="text-sm font-semibold mb-2 text-[#161616]",
                ),
                rx.el.div(
                    rx.foreach(
                        TemplateBuilderState.selected_entity_type_attributes,
                        new_entity_attribute_checklist_item,
                    ),
                    class_name="max-h-60 overflow-y-auto bg-white border border-[#e5e5e5] rounded-sm mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=TemplateBuilderState.cancel_new_entity,
                        class_name="px-4 py-2 text-sm text-[#525252] hover:bg-[#e5e5e5] rounded-sm mr-2 transition-colors",
                    ),
                    rx.el.button(
                        "Save Entity",
                        on_click=TemplateBuilderState.save_entity,
                        class_name="px-4 py-2 text-sm bg-[#0f62fe] text-white hover:bg-[#0353e9] rounded-sm transition-colors",
                    ),
                    class_name="flex justify-end pt-4 border-t border-[#e5e5e5]",
                ),
                class_name="bg-white p-6 rounded-sm w-full max-w-md shadow-2xl border border-[#e5e5e5]",
            ),
            class_name="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4",
        ),
        rx.fragment(),
    )


def template_builder_view() -> rx.Component:
    return rx.el.div(
        new_entity_modal(),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                    "Back to Templates",
                    on_click=TemplateBuilderState.close_builder,
                    class_name="flex items-center text-[#0f62fe] text-sm font-medium hover:underline mb-4",
                ),
                rx.el.h2(
                    "Template Creator", class_name="text-2xl font-normal text-[#161616]"
                ),
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Template Name",
                    on_change=TemplateBuilderState.set_template_name,
                    class_name="w-1/3 h-12 px-4 bg-white border-b-2 border-[#8d8d8d] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-lg font-medium shadow-sm",
                    default_value=TemplateBuilderState.template_name,
                ),
                rx.el.select(
                    rx.el.option("Contract", value="Contract"),
                    rx.el.option("Agreement", value="Agreement"),
                    rx.el.option("Legal Notice", value="Legal Notice"),
                    rx.el.option("Certificate", value="Certificate"),
                    rx.el.option("Authorization", value="Authorization"),
                    rx.el.option("Other", value="Other"),
                    value=TemplateBuilderState.template_category,
                    on_change=TemplateBuilderState.set_template_category,
                    class_name="w-48 h-12 px-4 bg-white border-b-2 border-[#8d8d8d] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-base shadow-sm appearance-none",
                ),
                class_name="flex gap-6 mt-6",
            ),
            rx.el.textarea(
                placeholder="Template Description (optional)",
                on_change=TemplateBuilderState.set_template_description,
                class_name="w-full mt-4 h-20 p-3 bg-white border border-[#e5e5e5] focus:outline focus:outline-2 focus:outline-[#0f62fe] rounded-sm text-sm resize-none shadow-sm",
                default_value=TemplateBuilderState.template_description,
            ),
            class_name="mb-8",
        ),
        rx.cond(
            TemplateBuilderState.show_preview,
            rx.el.div(
                rx.el.h3("Template Preview", class_name="text-xl font-semibold mb-4"),
                rx.el.div(
                    TemplateBuilderState.preview_content,
                    class_name="bg-white p-8 border border-[#e5e5e5] shadow-sm min-h-[500px] whitespace-pre-wrap font-serif",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        TemplateBuilderState.paragraphs,
                        lambda p, i: paragraph_card(p, i),
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="h-5 w-5 mr-2"),
                        "Add Paragraph",
                        on_click=TemplateBuilderState.add_paragraph,
                        class_name="flex items-center justify-center w-full py-4 border-2 border-dashed border-[#c6c6c6] text-[#525252] hover:border-[#0f62fe] hover:text-[#0f62fe] rounded-sm transition-colors",
                    ),
                    class_name="w-[65%]",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3(
                                        "Global Requirements",
                                        class_name="text-lg font-semibold text-[#161616]",
                                    ),
                                    rx.el.span(
                                        TemplateBuilderState.global_requirements.length(),
                                        class_name="ml-2 bg-[#0f62fe] text-white text-[10px] px-1.5 py-0.5 rounded-full",
                                    ),
                                    class_name="flex items-center mb-1",
                                ),
                                rx.el.p(
                                    "Key information not tied to any entity (dates, lists, amounts, etc.)",
                                    class_name="text-xs text-[#525252] mb-4",
                                ),
                                rx.foreach(
                                    TemplateBuilderState.global_requirements,
                                    global_requirement_card,
                                ),
                                rx.el.button(
                                    rx.icon("plus", class_name="h-4 w-4 mr-2"),
                                    "Add Global Requirement",
                                    on_click=TemplateBuilderState.add_global_requirement,
                                    class_name="flex items-center text-[#0f62fe] text-sm font-medium hover:underline mt-2",
                                ),
                                class_name="mb-8 pb-6 border-b border-[#e5e5e5]",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    f"Template Entities ({TemplateBuilderState.template_entities.length()})",
                                    class_name="text-lg font-semibold text-[#161616] mb-4",
                                ),
                                rx.foreach(
                                    TemplateBuilderState.template_entities,
                                    lambda e: rx.el.div(
                                        rx.el.div(
                                            rx.el.input(
                                                default_value=e["name"],
                                                on_change=lambda v: TemplateBuilderState.update_entity_name(
                                                    e["id"], v
                                                ),
                                                class_name="font-medium text-[#161616] bg-transparent border-b border-transparent hover:border-[#e5e5e5] focus:border-[#0f62fe] focus:outline-none flex-1 text-sm mr-2 py-1 px-1",
                                            ),
                                            rx.el.button(
                                                rx.icon(
                                                    "trash",
                                                    class_name="h-4 w-4 text-red-500 hover:text-red-700",
                                                ),
                                                on_click=lambda: TemplateBuilderState.remove_entity(
                                                    e["id"]
                                                ),
                                                class_name="p-1",
                                            ),
                                            class_name="flex justify-between items-center mb-1",
                                        ),
                                        rx.el.div(
                                            rx.el.span(
                                                e["type"],
                                                class_name="text-xs bg-[#e0e8ff] text-[#0f62fe] px-2 py-0.5 rounded-sm inline-block",
                                            ),
                                            class_name="mb-3 px-1",
                                        ),
                                        rx.el.div(
                                            rx.foreach(
                                                e["attributes"],
                                                lambda a, idx: rx.el.div(
                                                    rx.el.input(
                                                        default_value=a["name"],
                                                        placeholder="Name",
                                                        on_change=lambda v: TemplateBuilderState.update_entity_attribute(
                                                            e["id"], idx, "name", v
                                                        ),
                                                        class_name="w-[40%] text-xs h-7 px-2 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe]",
                                                    ),
                                                    rx.el.select(
                                                        rx.el.option(
                                                            "text", value="text"
                                                        ),
                                                        rx.el.option(
                                                            "number", value="number"
                                                        ),
                                                        rx.el.option(
                                                            "date", value="date"
                                                        ),
                                                        rx.el.option(
                                                            "email", value="email"
                                                        ),
                                                        rx.el.option(
                                                            "phone", value="phone"
                                                        ),
                                                        rx.el.option(
                                                            "address", value="address"
                                                        ),
                                                        value=a["type"],
                                                        on_change=lambda v: TemplateBuilderState.update_entity_attribute(
                                                            e["id"], idx, "type", v
                                                        ),
                                                        class_name="w-[30%] text-xs h-7 px-1 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe] appearance-none",
                                                    ),
                                                    rx.el.label(
                                                        rx.el.input(
                                                            type="checkbox",
                                                            checked=a["required"].to(
                                                                bool
                                                            ),
                                                            on_change=lambda v: TemplateBuilderState.update_entity_attribute(
                                                                e["id"],
                                                                idx,
                                                                "required",
                                                                v,
                                                            ),
                                                            class_name="mr-1 scale-90",
                                                        ),
                                                        "Req",
                                                        class_name="flex items-center text-[10px] text-[#525252] w-[15%]",
                                                    ),
                                                    rx.el.button(
                                                        rx.icon(
                                                            "x", class_name="h-3 w-3"
                                                        ),
                                                        on_click=lambda: TemplateBuilderState.remove_attribute_from_entity(
                                                            e["id"], idx
                                                        ),
                                                        class_name="text-red-500 hover:text-red-700 w-[10%] flex justify-center",
                                                    ),
                                                    class_name="flex items-center justify-between gap-1 mb-2",
                                                ),
                                            ),
                                            class_name="px-1",
                                        ),
                                        rx.el.button(
                                            rx.icon("plus", class_name="h-3 w-3 mr-1"),
                                            "Add Attribute",
                                            on_click=lambda: TemplateBuilderState.add_attribute_to_entity(
                                                e["id"]
                                            ),
                                            class_name="flex items-center text-[#0f62fe] text-xs font-medium hover:underline mt-2 px-1",
                                        ),
                                        class_name="bg-white p-4 border border-[#e5e5e5] rounded-sm mb-4 shadow-sm",
                                    ),
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.button(
                                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                                "New Entity",
                                on_click=TemplateBuilderState.start_new_entity,
                                class_name="flex items-center justify-center w-full py-3 bg-white border border-[#e5e5e5] text-[#0f62fe] text-sm font-medium hover:border-[#0f62fe] rounded-sm transition-colors shadow-sm",
                            ),
                            class_name="bg-[#f4f4f4] p-6 border border-[#e5e5e5] rounded-sm max-h-[calc(100vh-200px)] overflow-y-auto",
                        ),
                        class_name="sticky top-6",
                    ),
                    class_name="w-[35%]",
                ),
                class_name="flex gap-8 mb-24",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=TemplateBuilderState.close_builder,
                    class_name="px-6 py-3 text-sm font-medium text-[#525252] hover:bg-[#e5e5e5] rounded-sm transition-colors",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(TemplateBuilderState.show_preview, "Edit", "Preview"),
                        on_click=TemplateBuilderState.toggle_preview,
                        class_name="px-6 py-3 text-sm font-medium border border-[#c6c6c6] text-[#161616] hover:bg-[#e5e5e5] rounded-sm transition-colors mr-3",
                    ),
                    rx.el.button(
                        "Save as Draft",
                        on_click=lambda: TemplateBuilderState.save_template("draft"),
                        class_name="px-6 py-3 text-sm font-medium bg-[#393939] text-white hover:bg-[#161616] rounded-sm transition-colors mr-3",
                    ),
                    rx.el.button(
                        "Save Template",
                        on_click=lambda: TemplateBuilderState.save_template("active"),
                        class_name="px-6 py-3 text-sm font-medium bg-[#0f62fe] text-white hover:bg-[#0353e9] rounded-sm transition-colors",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center max-w-[1400px] mx-auto w-full",
            ),
            class_name="fixed bottom-0 left-64 right-0 bg-white border-t border-[#e5e5e5] p-4 z-40 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]",
        ),
        class_name="pb-16",
    )


def delete_template_confirmation_modal() -> rx.Component:
    return rx.cond(
        AppState.confirm_delete_template_id != "",
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Delete Template?",
                    class_name="text-lg font-semibold text-[#161616] mb-3",
                ),
                rx.el.p(
                    "Are you sure you want to delete this template? This action cannot be undone and may affect existing document generation workflows.",
                    class_name="text-sm text-[#525252] mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=AppState.cancel_delete_template,
                        class_name="px-4 py-2 text-[#525252] hover:bg-[#e5e5e5] rounded-sm mr-3 transition-colors",
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=AppState.delete_template,
                        class_name="px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded-sm transition-colors",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="bg-white w-full max-w-md p-6 rounded-sm shadow-xl",
            ),
            class_name="fixed inset-0 bg-black/50 z-[60] flex items-center justify-center p-4",
        ),
        rx.fragment(),
    )


def templates_page() -> rx.Component:
    return layout(
        rx.cond(
            TemplateBuilderState.is_builder_active,
            rx.el.div(
                template_builder_view(),
                class_name="p-8 max-w-[1400px] mx-auto animate-fade-in",
            ),
            rx.el.div(
                delete_template_confirmation_modal(),
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Document Templates",
                            class_name="text-3xl font-normal text-[#161616] tracking-tight",
                        ),
                        rx.el.p(
                            "Manage reusable document templates with dynamic data bindings.",
                            class_name="text-[#525252] mt-2 text-sm",
                        ),
                    ),
                    rx.el.button(
                        "New Template",
                        rx.icon("plus", class_name="ml-2 h-4 w-4"),
                        on_click=TemplateBuilderState.open_builder,
                        class_name="flex items-center bg-[#0f62fe] text-white h-[48px] px-4 font-medium hover:bg-[#0353e9] transition-colors rounded-sm shadow-sm",
                    ),
                    class_name="flex justify-between items-start mb-8",
                ),
                rx.el.div(
                    rx.foreach(AppState.templates, template_card),
                    class_name="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6",
                ),
                class_name="p-8 max-w-7xl mx-auto animate-fade-in",
            ),
        )
    )