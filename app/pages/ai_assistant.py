import reflex as rx
from app.states.chat_state import ChatState
from app.components.sidebar import layout


def chat_bubble(message: dict) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                message["content"],
                class_name=rx.cond(
                    is_user,
                    "bg-[#0f62fe] text-white p-3 rounded-t-xl rounded-bl-xl text-sm max-w-[85%] inline-block",
                    "bg-[#e5e5e5] text-[#161616] p-3 rounded-t-xl rounded-br-xl text-sm max-w-[85%] inline-block",
                ),
            ),
            rx.el.div(
                message["timestamp"],
                class_name=rx.cond(
                    is_user,
                    "text-xs text-[#8d8d8d] mt-1 text-right",
                    "text-xs text-[#8d8d8d] mt-1 text-left",
                ),
            ),
            class_name=rx.cond(is_user, "text-right w-full", "text-left w-full"),
        ),
        class_name="mb-6 w-full",
    )


def ai_assistant_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "AI Assistant",
                        class_name="text-xl font-semibold text-[#161616]",
                    ),
                    rx.el.button(
                        "Clear Chat",
                        on_click=ChatState.clear_chat,
                        class_name="text-sm text-[#0f62fe] hover:underline",
                    ),
                    class_name="flex justify-between items-center p-4 border-b border-[#e5e5e5] bg-white",
                ),
                rx.scroll_area(
                    rx.el.div(
                        rx.foreach(ChatState.messages, chat_bubble),
                        rx.cond(
                            ChatState.is_typing,
                            rx.el.div(
                                rx.el.div(
                                    "AI is typing...",
                                    class_name="bg-[#e5e5e5] text-[#525252] p-3 rounded-t-xl rounded-br-xl text-sm inline-block animate-pulse",
                                ),
                                class_name="mb-6 w-full",
                            ),
                            rx.fragment(),
                        ),
                        class_name="p-6",
                    ),
                    type="always",
                    scrollbars="vertical",
                    class_name="flex-1 bg-[#f4f4f4]",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.button(
                            "Fill a template",
                            on_click=lambda: ChatState.set_input("I want to fill NDA"),
                            class_name="text-xs bg-[#e5e5e5] text-[#161616] px-3 py-1.5 rounded-full hover:bg-[#d1d1d1] transition-colors",
                        ),
                        rx.el.button(
                            "Suggest changes",
                            on_click=lambda: ChatState.set_input(
                                "Can you suggest changes to this?"
                            ),
                            class_name="text-xs bg-[#e5e5e5] text-[#161616] px-3 py-1.5 rounded-full hover:bg-[#d1d1d1] transition-colors",
                        ),
                        class_name="flex gap-2 mb-3",
                    ),
                    rx.el.div(
                        rx.el.input(
                            placeholder="Type your message...",
                            on_change=ChatState.set_input,
                            class_name="flex-1 h-12 px-4 bg-[#f4f4f4] border border-[#e5e5e5] rounded-l-sm focus:outline-none focus:border-[#0f62fe]",
                            default_value=ChatState.current_input,
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="h-5 w-5"),
                            on_click=ChatState.send_message,
                            class_name="h-12 px-6 bg-[#0f62fe] text-white hover:bg-[#0353e9] transition-colors rounded-r-sm flex items-center justify-center",
                        ),
                        class_name="flex",
                    ),
                    class_name="p-4 border-t border-[#e5e5e5] bg-white",
                ),
                class_name="flex flex-col h-[calc(100vh-64px)] w-[60%] border-r border-[#e5e5e5]",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Document Context",
                        class_name="text-lg font-medium text-[#161616]",
                    ),
                    class_name="p-4 border-b border-[#e5e5e5] bg-white",
                ),
                rx.el.div(
                    rx.cond(
                        ChatState.demo_document_content != "",
                        rx.el.div(
                            rx.el.h3(
                                "Live Preview",
                                class_name="text-sm font-semibold text-[#525252] mb-4 uppercase tracking-wider",
                            ),
                            rx.el.div(
                                ChatState.demo_document_content,
                                class_name="p-8 bg-white border border-[#e5e5e5] shadow-sm min-h-[500px] font-serif text-[#161616] whitespace-pre-wrap",
                            ),
                            class_name="p-6",
                        ),
                        rx.el.div(
                            rx.icon(
                                "file-text",
                                class_name="h-12 w-12 text-[#c6c6c6] mx-auto mb-4",
                            ),
                            rx.el.p(
                                "No document currently selected.",
                                class_name="text-[#525252]",
                            ),
                            class_name="flex flex-col items-center justify-center h-full",
                        ),
                    ),
                    class_name="flex-1 bg-[#f4f4f4] overflow-y-auto",
                ),
                class_name="flex flex-col h-[calc(100vh-64px)] w-[40%]",
            ),
            class_name="flex w-full",
        )
    )