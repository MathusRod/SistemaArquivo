import uuid
from implementacoes_inode.inode import Inode

class SistemaArquivos:
    def __init__(self):
        self.raiz = {}
        self.caminho_atual = []
        self.diretorio_atual = self.raiz
        self._criar_raiz()
    
    def _criar_raiz(self):
        raiz_inode = Inode("/", "diretorio")
        self.raiz = {
            'inode': raiz_inode,
            'conteudo': {
                '.': {'inode': raiz_inode},
                '..': {'inode': raiz_inode}
            }
        }
        self.diretorio_atual = self.raiz['conteudo']

    def criar(self, nome, tipo, tamanho=0):
        if nome in self.diretorio_atual:
            print("Já existe um item com esse nome.")
            return None

        inode = Inode(nome, tipo)
        inode.tamanho = tamanho
        
        if tipo == 'arquivo' and tamanho > 0:
            num_blocos = (tamanho + 511) // 512
            inode.blocos = [f"bloco_{i}_{uuid.uuid4().hex[:4]}" for i in range(num_blocos)]
        
        if tipo == 'diretorio':
            self.diretorio_atual[nome] = {
                'inode': inode,
                'conteudo': {
                    '.': {'inode': inode},
                    '..': {'inode': self.diretorio_atual['.']['inode']}
                }
            }
        else:
            self.diretorio_atual[nome] = {'inode': inode}
        
        print(f"{tipo.capitalize()} '{nome}' criado com sucesso.")
        return inode

    def listar(self):
        print(f"\nConteúdo de {self.obter_caminho()}:")
        print("Tipo\tNome\t\tTamanho\tBlocos")
        print("----\t----\t\t-------\t------")
        
        for nome, item in self.diretorio_atual.items():
            if nome in ['.', '..']:
                continue
            inode = item['inode']
            tipo = 'DIR' if inode.tipo == 'diretorio' else 'ARQ'
            blocos = len(inode.blocos) if inode.tipo == 'arquivo' else '-'
            print(f"{tipo}\t{nome.ljust(10)}\t{inode.tamanho}\t{blocos}")

    def entrar(self, nome):
        if nome == ".":
            return True
            
        if nome == "..":
            if not self.caminho_atual:
                print("Já está na raiz")
                return True
            self.caminho_atual.pop()
            atual = self.raiz['conteudo']
            for dir_nome in self.caminho_atual:
                atual = atual[dir_nome]['conteudo']
            self.diretorio_atual = atual
            return True
            
        if nome not in self.diretorio_atual:
            print(f"Erro: '{nome}' não encontrado")
            return False
            
        item = self.diretorio_atual[nome]
        if item['inode'].tipo != 'diretorio':
            print(f"Erro: '{nome}' não é um diretório")
            return False
            
        self.caminho_atual.append(nome)
        self.diretorio_atual = item['conteudo']
        return True

    def obter_caminho(self):
        return '/' + '/'.join(self.caminho_atual) if self.caminho_atual else '/'

    def mostrar_caminho(self):
        print(self.obter_caminho())
        
    def mover(self, origem, destino_nome):
        """
        Move um arquivo ou diretório para outro diretório
        :param origem: Nome do item a ser movido
        :param destino_nome: Nome do diretório de destino
        """
        # Verifica se o item de origem existe
        if origem not in self.diretorio_atual:
            print(f"Erro: '{origem}' não encontrado")
            return False
            
        item = self.diretorio_atual[origem]
        
        # Verifica se o destino é um diretório válido
        if destino_nome not in self.diretorio_atual:
            print(f"Erro: '{destino_nome}' não encontrado")
            return False
            
        destino_item = self.diretorio_atual[destino_nome]
        if destino_item['inode'].tipo != 'diretorio':
            print(f"Erro: '{destino_nome}' não é um diretório")
            return False
            
        destino_conteudo = destino_item['conteudo']
        
        # Verifica se já existe item com mesmo nome no destino
        if origem in destino_conteudo:
            print(f"Erro: '{origem}' já existe no destino")
            return False
            
        # Move o item mantendo o mesmo inode
        destino_conteudo[origem] = item
        del self.diretorio_atual[origem]
        
        # Atualiza o '..' se for um diretório
        if item['inode'].tipo == 'diretorio':
            item['conteudo']['..'] = {'inode': destino_item['inode']}
            
        print(f"'{origem}' movido para '{destino_nome}' com sucesso")

    def _resolve_path(self, path: str):
        if path.startswith('/'):
            atual = self.raiz['conteudo']
            partes = [p for p in path.split('/') if p]
        else:
            atual = self.diretorio_atual
            partes = [p for p in path.split('/') if p]

        for p in partes[:-1]:
            if p not in atual or atual[p]['inode'].tipo != 'diretorio':
                raise FileNotFoundError(f"Diretório '{p}' não encontrado em caminho '{path}'")
            atual = atual[p]['conteudo']

        return atual, partes[-1]

    def mover(self, origem_path, destino_path):
        # resolve origem
        src_dir, src_name = self._resolve_path(origem_path)
        if src_name not in src_dir:
            print(f"Erro: origem '{origem_path}' não encontrado")
            return False
        item = src_dir[src_name]

        # resolve destino
        dst_dir, dst_name = self._resolve_path(destino_path)
        # se o destino apontar para um diretório, usamos o mesmo nome_src
        if dst_name in dst_dir and dst_dir[dst_name]['inode'].tipo == 'diretorio':
            destino_conteudo = dst_dir[dst_name]['conteudo']
            final_name = src_name
        else:
            # caso queira renomear ao mover
            destino_conteudo = dst_dir
            final_name = dst_name

        if final_name in destino_conteudo:
            print(f"Erro: '{final_name}' já existe no destino")
            return False

        # faz a movimentação
        destino_conteudo[final_name] = item
        del src_dir[src_name]

        # se for diretório, atualiza o '..'
        if item['inode'].tipo == 'diretorio':
            parent_inode = dst_dir[dst_name]['inode'] if dst_name in dst_dir else dst_dir['.']['inode']
            item['conteudo']['..'] = {'inode': parent_inode}

        print(f"'{origem_path}' movido para '{destino_path}' com sucesso")
        return True
