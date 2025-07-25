class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None

    def next_token(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            return # Would return our results here