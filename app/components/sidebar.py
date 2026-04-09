import reflex as rx
from app.states.app_state import AppState
from app.states.auth_state import AuthState


def nav_item(label: str, icon_name: str, path: str) -> rx.Component:
    is_active = AppState.current_path == path
    return rx.el.a(
        rx.icon(
            icon_name,
            class_name=rx.cond(
                is_active, "text-white h-5 w-5", "text-[#c6c6c6] h-5 w-5"
            ),
        ),
        rx.cond(
            AppState.sidebar_collapsed,
            rx.fragment(),
            rx.el.span(
                label,
                class_name=rx.cond(is_active, "text-white ml-3", "text-[#c6c6c6] ml-3"),
            ),
        ),
        href=path,
        class_name=rx.cond(
            is_active,
            "flex items-center px-4 py-3 bg-[#0f62fe] border-l-4 border-white transition-colors duration-200 cursor-pointer",
            "flex items-center px-4 py-3 border-l-4 border-transparent hover:bg-[#393939] transition-colors duration-200 cursor-pointer",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("scale", class_name="h-6 w-6 text-white min-w-6"),
                rx.cond(
                    AppState.sidebar_collapsed,
                    rx.fragment(),
                    rx.el.span(
                        "LegalDoc IDE",
                        class_name="text-white font-semibold text-lg ml-3 tracking-wide whitespace-nowrap",
                    ),
                ),
                class_name="flex items-center px-4 h-16 border-b border-[#393939]",
            ),
            rx.el.nav(
                nav_item("Dashboard", "layout-dashboard", "/"),
                nav_item("Entities", "database", "/entities"),
                nav_item("Templates", "file-text", "/templates"),
                nav_item("Documents", "folder", "/documents"),
                nav_item("AI Assistant", "bot", "/ai-assistant"),
                rx.cond(
                    AuthState.is_admin,
                    nav_item("Users", "users", "/users"),
                    rx.fragment(),
                ),
                class_name="flex flex-col py-4 gap-1 flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "chevron-left",
                        class_name=rx.cond(
                            AppState.sidebar_collapsed,
                            "rotate-180 transition-transform h-5 w-5 text-white",
                            "transition-transform h-5 w-5 text-white",
                        ),
                    ),
                    on_click=AppState.toggle_sidebar,
                    class_name="w-full flex items-center justify-center h-12 border-t border-[#393939] hover:bg-[#393939] cursor-pointer",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("user", class_name="h-6 w-6 text-[#c6c6c6] min-w-6"),
                        rx.cond(
                            AppState.sidebar_collapsed,
                            rx.fragment(),
                            rx.el.div(
                                rx.el.p(
                                    AuthState.display_name,
                                    class_name="text-sm text-white font-medium capitalize",
                                ),
                                rx.el.p(
                                    AuthState.current_user["role"],
                                    class_name="text-xs text-[#c6c6c6] truncate",
                                ),
                                class_name="ml-3 overflow-hidden flex-1",
                            ),
                        ),
                        rx.cond(
                            AppState.sidebar_collapsed,
                            rx.fragment(),
                            rx.el.button(
                                rx.icon(
                                    "log-out",
                                    class_name="h-4 w-4 text-[#c6c6c6] hover:text-white transition-colors",
                                ),
                                on_click=AuthState.logout,
                                class_name="p-2 ml-auto",
                            ),
                        ),
                        class_name="flex items-center w-full",
                    ),
                    rx.cond(
                        AppState.sidebar_collapsed,
                        rx.el.button(
                            rx.icon(
                                "log-out",
                                class_name="h-4 w-4 text-[#c6c6c6] hover:text-white transition-colors mx-auto mt-2",
                            ),
                            on_click=AuthState.logout,
                            class_name="w-full flex justify-center py-2",
                        ),
                        rx.fragment(),
                    ),
                    class_name="px-4 py-4 border-t border-[#393939] flex flex-col",
                ),
                class_name="mt-auto",
            ),
            class_name="flex flex-col h-full bg-[#161616]",
        ),
        class_name=rx.cond(
            AppState.sidebar_collapsed,
            "w-16 flex-shrink-0 transition-all duration-300 h-screen sticky top-0 font-['IBM_Plex_Sans']",
            "w-64 flex-shrink-0 transition-all duration-300 h-screen sticky top-0 font-['IBM_Plex_Sans']",
        ),
    )


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            content,
            class_name="flex-1 bg-[#f4f4f4] min-h-screen font-['IBM_Plex_Sans']",
        ),
        class_name="flex w-full min-h-screen overflow-x-hidden",
    )