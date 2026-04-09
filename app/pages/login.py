import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("scale", class_name="h-8 w-8 text-[#0f62fe] mb-4"),
                rx.el.h1(
                    "LegalDoc IDE",
                    class_name="text-2xl font-semibold text-[#161616] mb-1",
                ),
                rx.el.p("Sign In", class_name="text-[#525252] text-sm"),
                class_name="flex flex-col items-center mb-8",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.login_error != "",
                    rx.el.div(
                        AuthState.login_error,
                        class_name="bg-red-50 text-red-600 text-sm p-3 rounded-sm border border-red-200 mb-4",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.label(
                        "Username",
                        class_name="block text-sm font-medium text-[#161616] mb-2",
                    ),
                    rx.el.input(
                        on_change=AuthState.set_username,
                        class_name="w-full h-10 px-4 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none rounded-sm",
                        default_value=AuthState.username,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-sm font-medium text-[#161616] mb-2",
                    ),
                    rx.el.input(
                        type="password",
                        on_change=AuthState.set_password,
                        class_name="w-full h-10 px-4 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none rounded-sm",
                    ),
                    class_name="mb-8",
                ),
                rx.el.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.icon("loader", class_name="h-5 w-5 animate-spin mx-auto"),
                        "Sign In",
                    ),
                    on_click=AuthState.login,
                    disabled=AuthState.is_loading,
                    class_name="w-full h-12 bg-[#0f62fe] text-white font-medium hover:bg-[#0353e9] transition-colors rounded-sm flex items-center justify-center disabled:opacity-50",
                ),
                class_name="w-full",
            ),
            rx.el.p(
                "Default: admin / admin123",
                class_name="text-xs text-[#8d8d8d] mt-8 text-center",
            ),
            class_name="bg-white p-8 sm:p-12 border border-[#e5e5e5] rounded-sm shadow-sm w-full max-w-[400px] font-['IBM_Plex_Sans']",
        ),
        class_name="min-h-screen bg-[#f4f4f4] flex items-center justify-center p-4 font-['IBM_Plex_Sans']",
    )