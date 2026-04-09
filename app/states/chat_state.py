import reflex as rx
from typing import TypedDict
import asyncio
from datetime import datetime


class ChatMessage(TypedDict):
    role: str
    content: str
    timestamp: str


class ChatState(rx.State):
    messages: list[ChatMessage] = [
        {
            "role": "ai",
            "content": "Hello! I'm your LegalDoc AI assistant. How can I help you today? You can ask me to 'fill NDA' to see a demo.",
            "timestamp": "Just now",
        }
    ]
    current_input: str = ""
    is_typing: bool = False
    demo_document_content: str = "Please select a template or ask me to fill one."

    @rx.event
    def set_input(self, value: str):
        self.current_input = value

    @rx.event
    def clear_chat(self):
        self.messages = [
            {
                "role": "ai",
                "content": "Chat cleared. How can I help?",
                "timestamp": "Just now",
            }
        ]
        self.demo_document_content = ""

    @rx.event
    def send_message(self):
        if not self.current_input.strip():
            return
        user_msg = self.current_input
        self.messages.append(
            {
                "role": "user",
                "content": user_msg,
                "timestamp": datetime.now().strftime("%I:%M %p"),
            }
        )
        self.current_input = ""
        yield ChatState.process_ai_response(user_msg)

    @rx.event(background=True)
    async def process_ai_response(self, user_msg: str):
        async with self:
            self.is_typing = True
        await asyncio.sleep(1.5)
        async with self:
            self.is_typing = False
            if "fill" in user_msg.lower() and "nda" in user_msg.lower():
                ai_resp = "I can help with that. I've loaded the NDA template. What is the name of the Person and the Company?"
                self.demo_document_content = "This Non-Disclosure Agreement is entered into by and between [Person Name] and [Company Name]..."
            elif (
                "person" in user_msg.lower()
                or "company" in user_msg.lower()
                or "acme" in user_msg.lower()
            ):
                ai_resp = "Great, I've updated the document with those details. Does this look correct?"
                self.demo_document_content = "This Non-Disclosure Agreement is entered into by and between John Doe and Acme Corp..."
            else:
                ai_resp = "I'm currently in demo mode! Try asking me to 'fill NDA' or provide a Person/Company name."
            self.messages.append(
                {
                    "role": "ai",
                    "content": ai_resp,
                    "timestamp": datetime.now().strftime("%I:%M %p"),
                }
            )
            yield rx.toast("Demo Mode: AI responses are pre-programmed.", duration=3000)