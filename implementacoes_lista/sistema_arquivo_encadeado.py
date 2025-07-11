from .bloco import Bloco

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
    
    def _resolve_path(self, path: str):
        if path.startswith('/'):
            base = []                  
            partes = [p for p in path.split('/') if p]
        else:
            base = list(self.caminho)  
            partes = [p for p in path.split('/') if p]

        stack = []
        for p in base + partes:
            if p == '.' or p == '':
                continue
            if p == '..':
                if stack:
                    stack.pop()
            else:
                stack.append(p)

        if not stack:
            return self.raiz, ''
        pai_partes = stack[:-1]
        nome_final = stack[-1]

        atual = self.raiz
        for p in pai_partes:
            if p in atual and atual[p]['tipo'] == 'diretorio':
                atual = atual[p]['obj']
            else:
                raise FileNotFoundError(f"Diretório '{p}' não encontrado em '{path}'")

        return atual, nome_final

    def mover(self, origem_path: str, destino_path: str) -> bool:
        try:
            src_dir, src_name = self._resolve_path(origem_path)
        except FileNotFoundError as e:
            print("Erro:", e)
            return False

        if src_name not in src_dir:
            print(f"Erro: origem '{origem_path}' não encontrada")
            return False
        item = src_dir[src_name]

        try:
            dst_dir, dst_name = self._resolve_path(destino_path)
        except FileNotFoundError as e:
            print("Erro:", e)
            return False

        if dst_name in dst_dir and dst_dir[dst_name]['tipo'] == 'diretorio':
            final_dir = dst_dir[dst_name]['obj']
            final_name = src_name
        else:
            final_dir = dst_dir
            final_name = dst_name

        if final_name in final_dir:
            print(f"Erro: '{final_name}' já existe em '{destino_path}'")
            return False

        final_dir[final_name] = item
        del src_dir[src_name]
        print(f"'{origem_path}' movido para '{destino_path}' com sucesso")
        return True

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
