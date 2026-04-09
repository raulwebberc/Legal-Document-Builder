import reflex as rx
from app.states.user_state import UserState
from app.states.auth_state import AuthState
from app.components.sidebar import layout


def user_row(user: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            user["username"], class_name="py-4 px-6 text-sm text-[#161616] font-medium"
        ),
        rx.el.td(
            rx.match(
                user["role"],
                (
                    "admin",
                    rx.el.span(
                        "Admin",
                        class_name="px-2 py-1 text-xs font-medium bg-[#e0e8ff] text-[#0f62fe] rounded-sm w-fit",
                    ),
                ),
                rx.el.span(
                    "User",
                    class_name="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-sm w-fit",
                ),
            ),
            class_name="py-4 px-6",
        ),
        rx.el.td(user["created_at"], class_name="py-4 px-6 text-sm text-[#525252]"),
        rx.el.td(
            rx.el.button(
                rx.icon("pencil", class_name="h-4 w-4 text-[#0f62fe]"),
                on_click=lambda: UserState.open_edit_user(user["id"]),
                class_name="p-2 hover:bg-[#e5e5e5] rounded-sm transition-colors",
            ),
            rx.cond(
                user["id"] != AuthState.current_user["id"],
                rx.el.button(
                    rx.icon("trash", class_name="h-4 w-4 text-red-600"),
                    on_click=lambda: UserState.confirm_delete_user(user["id"]),
                    class_name="p-2 hover:bg-red-50 rounded-sm transition-colors",
                ),
                rx.fragment(),
            ),
            class_name="py-4 px-6 flex gap-2",
        ),
        class_name="border-b border-[#e5e5e5] hover:bg-[#f4f4f4] transition-colors",
    )


def edit_user_modal() -> rx.Component:
    return rx.cond(
        UserState.is_creating_user,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            UserState.editing_user_id != "", "Edit User", "New User"
                        ),
                        class_name="text-xl font-semibold",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=UserState.close_user_modal,
                        class_name="text-[#525252] hover:text-[#161616]",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Username",
                        class_name="block text-sm font-medium text-[#161616] mb-1",
                    ),
                    rx.el.input(
                        on_change=UserState.set_edit_username,
                        class_name="w-full h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe]",
                        default_value=UserState.edit_username,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        rx.cond(
                            UserState.editing_user_id != "",
                            "Password (leave blank to keep existing)",
                            "Password",
                        ),
                        class_name="block text-sm font-medium text-[#161616] mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        on_change=UserState.set_edit_password,
                        class_name="w-full h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe]",
                        default_value=UserState.edit_password,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Role",
                        class_name="block text-sm font-medium text-[#161616] mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("User", value="user"),
                        rx.el.option("Admin", value="admin"),
                        value=UserState.edit_role,
                        on_change=UserState.set_edit_role,
                        class_name="w-full h-10 px-3 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:outline-none focus:border-[#0f62fe] appearance-none",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=UserState.close_user_modal,
                        class_name="px-4 py-2 text-[#525252] hover:bg-[#e5e5e5] rounded-sm mr-2",
                    ),
                    rx.el.button(
                        "Save Changes",
                        on_click=UserState.save_user,
                        class_name="px-4 py-2 bg-[#0f62fe] text-white hover:bg-[#0353e9] rounded-sm",
                    ),
                    class_name="flex justify-end pt-4 border-t border-[#e5e5e5]",
                ),
                class_name="bg-white w-full max-w-[500px] p-6 rounded-sm shadow-xl",
            ),
            class_name="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4",
        ),
        rx.fragment(),
    )


def delete_user_modal() -> rx.Component:
    return rx.cond(
        UserState.confirm_delete_user_id != "",
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Delete User?",
                    class_name="text-lg font-semibold text-[#161616] mb-3",
                ),
                rx.el.p(
                    "Are you sure you want to delete this user? This action cannot be undone.",
                    class_name="text-sm text-[#525252] mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=UserState.cancel_delete,
                        class_name="px-4 py-2 text-[#525252] hover:bg-[#e5e5e5] rounded-sm mr-3",
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=UserState.delete_user,
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


def change_password_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Change My Password", class_name="text-xl font-semibold mb-4"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Current Password",
                    class_name="block text-sm font-medium text-[#161616] mb-2",
                ),
                rx.el.input(
                    type="password",
                    on_change=UserState.set_current_password,
                    class_name="w-full h-10 px-4 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none rounded-sm",
                    default_value=UserState.current_password,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "New Password",
                    class_name="block text-sm font-medium text-[#161616] mb-2",
                ),
                rx.el.input(
                    type="password",
                    on_change=UserState.set_new_password,
                    class_name="w-full h-10 px-4 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none rounded-sm",
                    default_value=UserState.new_password,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Confirm New Password",
                    class_name="block text-sm font-medium text-[#161616] mb-2",
                ),
                rx.el.input(
                    type="password",
                    on_change=UserState.set_confirm_new_password,
                    class_name="w-full h-10 px-4 bg-[#f4f4f4] border-b border-[#8d8d8d] focus:border-[#0f62fe] focus:outline-none rounded-sm",
                    default_value=UserState.confirm_new_password,
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Update Password",
                on_click=UserState.change_password,
                class_name="px-4 py-2 bg-[#0f62fe] text-white font-medium hover:bg-[#0353e9] transition-colors rounded-sm",
            ),
            class_name="max-w-md bg-white border border-[#e5e5e5] p-6 rounded-sm shadow-sm",
        ),
        class_name="mt-12",
    )


def users_page() -> rx.Component:
    return layout(
        rx.el.div(
            edit_user_modal(),
            delete_user_modal(),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "User Management",
                        class_name="text-3xl font-normal text-[#161616] tracking-tight",
                    ),
                    rx.el.p(
                        "Manage system access and roles.",
                        class_name="text-[#525252] mt-2 text-sm",
                    ),
                ),
                rx.el.button(
                    "Add User",
                    rx.icon("plus", class_name="ml-2 h-4 w-4"),
                    on_click=UserState.open_create_user,
                    class_name="flex items-center bg-[#0f62fe] text-white h-[48px] px-4 font-medium hover:bg-[#0353e9] transition-colors rounded-sm shadow-sm",
                ),
                class_name="flex justify-between items-start mb-8",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Username",
                                class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Role",
                                class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Created At",
                                class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="py-3 px-6 text-left text-xs font-semibold text-[#525252] uppercase tracking-wider",
                            ),
                            class_name="bg-[#f4f4f4] border-b border-[#e5e5e5]",
                        )
                    ),
                    rx.el.tbody(rx.foreach(UserState.users, user_row)),
                    class_name="w-full table-auto",
                ),
                class_name="bg-white border border-[#e5e5e5] rounded-sm overflow-hidden shadow-sm",
            ),
            change_password_section(),
            class_name="p-8 max-w-[1400px] mx-auto animate-fade-in",
        )
    )