import uuid

class Bloco:
    def __init__(self, dados):
        self.id = f"bloco_{uuid.uuid4().hex[:6]}"
        self.dados = dados
        self.proximo = None

    def __repr__(self):
        return f"{self.id}"
