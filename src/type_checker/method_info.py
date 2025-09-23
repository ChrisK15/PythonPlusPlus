class MethodInfo:
    def __init__(self, method_name: str, method_type: str, params: dict = None):
        self.method_name = method_name
        self.method_type = method_type
        self.params = params
