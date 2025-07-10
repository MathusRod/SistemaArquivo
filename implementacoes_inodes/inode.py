import uuid

class Inode:
    def __init__(self, nome, tipo):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.tipo = tipo  # 'arquivo' ou 'diretorio'
        self.tamanho = 0
        self.blocos = []

    def __repr__(self):
        return f"<Inode {self.nome} ({self.tipo})>"
