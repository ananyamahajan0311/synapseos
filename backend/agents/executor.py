from tools.router import ToolRouter


class Executor:
    def __init__(self):
        self.router = ToolRouter()

    def execute(self, plan):
        return self.router.run(plan)
    