class ClassInfo:
    def __init__(self, class_name: str, parent_class: str = None):
        self.class_name = class_name
        self.parent_class = parent_class
        self.instance_vars = {}
        self.constructor = None
        self.methods = None