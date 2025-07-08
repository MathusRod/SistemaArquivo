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


class SistemaArquivos:
    def __init__(self):
        self.raiz = {}
        self.caminho_atual = []
        self.diretorio_atual = self.raiz

    def criar(self, nome, tipo):
        if nome in self.diretorio_atual:
            print("Já existe um item com esse nome.")
            return

        inode = Inode(nome, tipo)
        if tipo == 'diretorio':
            self.diretorio_atual[nome] = {'inode': inode, 'conteudo': {}}
        else:
            self.diretorio_atual[nome] = {'inode': inode}
        print(f"{tipo.capitalize()} '{nome}' criado com sucesso.")

    def listar(self):
        for nome, dado in self.diretorio_atual.items():
            tipo = dado['inode'].tipo
            print(f"{tipo.upper()}: {nome}")

    def entrar(self, nome):
        if nome == "..":
            if self.caminho_atual:
                self.caminho_atual.pop()
                self.diretorio_atual = self.raiz
                for p in self.caminho_atual:
                    self.diretorio_atual = self.diretorio_atual[p]['conteudo']
        elif nome in self.diretorio_atual and self.diretorio_atual[nome]['inode'].tipo == 'diretorio':
            self.caminho_atual.append(nome)
            self.diretorio_atual = self.diretorio_atual[nome]['conteudo']
        else:
            print("Diretório não encontrado.")

    def mostrar_caminho(self):
        print("/" + "/".join(self.caminho_atual))


if __name__ == "__main__":
    fs = SistemaArquivos()

    # Teste básico
    fs.criar("docs", "diretorio")
    fs.entrar("docs")
    fs.criar("arquivo1.txt", "arquivo")
    fs.listar()
    fs.mostrar_caminho()
    fs.entrar("..")
    fs.mostrar_caminho()

