from collections import deque


class Memory:

    def __init__(self, max_messages=20):
        self.history = deque(maxlen=max_messages)

    def add(self, role, message):
        self.history.append({
            "role": role,
            "message": message
        })

    def get_context(self):
        if not self.history:
            return ""

        context = ""

        for item in self.history:
            context += f'{item["role"]}: {item["message"]}\n'

        return context

    def clear(self):
        self.history.clear()