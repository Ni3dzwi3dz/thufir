class DatabaseModelNotSet(Exception):
    template = "Database model not set for class: {class_name}"

    def __init__(self, class_name: str):
        super().__init__(self.template.format(class_name=class_name))
