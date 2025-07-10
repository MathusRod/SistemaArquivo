from implementacoes_lista.bloco import Bloco

class ArquivoEncadeado:
    def __init__(self, nome, tamanho=0):
        self.nome = nome
        self.tipo = "arquivo"
        self.tamanho = 0
        self.inicio = None

        if tamanho > 0:
            self.escrever("0" * tamanho)

    def escrever(self, dados):
        partes = [dados[i:i+512] for i in range(0, len(dados), 512)]
        for parte in partes:
            novo = Bloco(parte)
            self.tamanho += len(parte)
            if not self.inicio:
                self.inicio = novo
            else:
                atual = self.inicio
                while atual.proximo:
                    atual = atual.proximo
                atual.proximo = novo

    def ler(self):
        atual = self.inicio
        dados = []
        while atual:
            dados.append(atual.dados)
            atual = atual.proximo
        return dados


class SistemaArquivosEncadeado:
    def __init__(self):
        self.raiz = {}
        self.atual = self.raiz
        self.caminho = []

    def obter_caminho(self):
        return "/" + "/".join(self.caminho) if self.caminho else "/"

    def listar(self):
        print(f"\nConteúdo de {self.obter_caminho()}:")
        for nome in self.atual:
            item = self.atual[nome]
            tipo = "DIR" if item["tipo"] == "diretorio" else "ARQ"
            tam = item["obj"].tamanho if item["tipo"] == "arquivo" else "-"
            print(f"{tipo}\t{nome}\t{tam} bytes")

    def criar(self, nome, tipo, tamanho=0):
        if nome in self.atual:
            print("Já existe.")
            return

        if tipo == "diretorio":
            self.atual[nome] = {"tipo": "diretorio", "obj": {}}
        else:
            self.atual[nome] = {"tipo": "arquivo", "obj": ArquivoEncadeado(nome, tamanho)}
        print(f"{tipo.capitalize()} '{nome}' criado.")

    def entrar(self, nome):
        if nome == "..":
            if self.caminho:
                self.caminho.pop()
                atual = self.raiz
                for p in self.caminho:
                    atual = atual[p]["obj"]
                self.atual = atual
        elif nome in self.atual and self.atual[nome]["tipo"] == "diretorio":
            self.caminho.append(nome)
            self.atual = self.atual[nome]["obj"]
        else:
            print("Diretório não encontrado.")
    
    def mover(self, origem, caminho_destino):
      if origem not in self.atual:
          print("Origem não encontrada.")
          return

      partes = caminho_destino.strip("/").split("/")
      nome_destino = partes[-1]
      destino_diretorio = self.raiz

      for parte in partes[:-1]:
          if parte not in destino_diretorio or destino_diretorio[parte]["tipo"] != "diretorio":
              print(f"Diretório '{parte}' não encontrado no caminho.")
              return
          destino_diretorio = destino_diretorio[parte]["obj"]

      if nome_destino in destino_diretorio:
          print("Destino já existe.")
          return

      destino_diretorio[nome_destino] = self.atual[origem]
      del self.atual[origem]
      print(f"'{origem}' movido para '{caminho_destino}'.")

    def escrever_arquivo(self, nome, dados):
        if nome not in self.atual or self.atual[nome]["tipo"] != "arquivo":
            print("Arquivo inválido.")
            return
        self.atual[nome]["obj"].escrever(dados)
        print("Escrita realizada.")

    def ler_arquivo(self, nome):
        if nome not in self.atual or self.atual[nome]["tipo"] != "arquivo":
            print("Arquivo inválido.")
            return
        dados = self.atual[nome]["obj"].ler()
        print(f"Conteúdo de {nome}:")
        print(">>", dados[-1] if dados else "Arquivo vazio.")

    def excluir(self, nome):
        if nome not in self.atual:
            print("Não encontrado.")
            return

        if self.atual[nome]["tipo"] == "diretorio" and self.atual[nome]["obj"]:
            print("Diretório não está vazio.")
            return

        del self.atual[nome]
        print(f"'{nome}' excluído.")
