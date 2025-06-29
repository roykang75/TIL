from contextvars import ContextVar

user_context: dict | None = ContextVar("user_context", default=None)