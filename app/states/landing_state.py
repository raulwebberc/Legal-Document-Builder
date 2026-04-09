import reflex as rx


class LandingState(rx.State):
    waitlist_email: str = ""

    @rx.event
    def set_waitlist_email(self, val: str):
        self.waitlist_email = val

    @rx.event
    def submit_waitlist(self):
        if not self.waitlist_email.strip():
            return rx.toast("Please enter a valid email.", type="error")
        email = self.waitlist_email
        self.waitlist_email = ""
        return rx.toast(
            f"Request received for {email}! We'll contact you soon.",
            duration=5000,
            close_button=True,
        )