class Inode:
    def __init__(self, inode_number, name, is_directory=False, size=0):
        self.inode_number = inode_number
        self.name = name
        self.is_directory = is_directory
        self.size = size
        self.pointers = []  # Índices para blocos de dados
        self.children = {}  # Filhos (apenas para diretórios): nome -> inode
        self.parent = None   # Referência ao diretório pai

    def __repr__(self):
        tipo = "DIR" if self.is_directory else "ARQ"
        return f"Inode {self.inode_number} [{tipo}]: {self.name} ({self.size} bytes) | Blocos: {self.pointers}"

class FileSystem:
    def __init__(self):
        self.inode_table = {}       # Tabela de i-nodes
        self.data_blocks = []       # Blocos de dados simulados
        self.next_inode_number = 0  # Contador para novos i-nodes
        self.next_block_index = 0   # Contador para novos blocos
        self.root = self.create_node("/", True)  # Cria diretório raiz
        self.current_dir = self.root  # Diretório atual inicia na raiz
        
        # Configura diretório raiz
        self.root.parent = self.root  # Raiz aponta para si mesma como pai
        self.root.children["."] = self.root
        self.root.children[".."] = self.root

    def create_node(self, name, is_directory, size=0):
        # Cria novo i-node
        inode_number = self.next_inode_number
        self.next_inode_number += 1
        
        # Aloca blocos se necessário
        pointers = []
        if size > 0:
            num_blocks = (size + 4095) // 4096  # Calcula blocos necessários (4KB cada)
            pointers = self._allocate_blocks(num_blocks)
        
        # Cria e registra o i-node
        inode = Inode(inode_number, name, is_directory, size)
        inode.pointers = pointers
        self.inode_table[inode_number] = inode
        return inode

    def _allocate_blocks(self, num_blocks):
        # Aloca novos blocos de dados
        pointers = []
        for _ in range(num_blocks):
            pointers.append(self.next_block_index)
            self.data_blocks.append(f"Conteúdo do bloco {self.next_block_index}")
            self.next_block_index += 1
        return pointers

    def create_file(self, name, size, parent_inode=None):
        if parent_inode is None:
            parent_inode = self.current_dir
            
        # Valida se o pai é diretório
        if not parent_inode.is_directory:
            raise ValueError("O i-node pai deve ser um diretório")
        
        # Cria novo arquivo
        new_file = self.create_node(name, False, size)
        new_file.parent = parent_inode
        parent_inode.children[name] = new_file
        return new_file

    def create_directory(self, name, parent_inode=None):
        if parent_inode is None:
            parent_inode = self.current_dir
            
        # Valida se o pai é diretório
        if not parent_inode.is_directory:
            raise ValueError("O i-node pai deve ser um diretório")
        
        # Cria novo diretório
        new_dir = self.create_node(name, True)
        new_dir.parent = parent_inode
        
        # Configura entradas especiais
        new_dir.children["."] = new_dir
        new_dir.children[".."] = parent_inode
        
        # Adiciona ao pai
        parent_inode.children[name] = new_dir
        return new_dir

    def list_directory(self, inode=None):
        # Lista conteúdo do diretório atual por padrão
        if inode is None:
            inode = self.current_dir
            
        if not inode.is_directory:
            print(f"Erro: '{inode.name}' não é um diretório")
            return
            
        print(f"\nConteúdo de '{inode.name}':")
        for name, child in inode.children.items():
            if name == "." or name == "..":
                continue  # Oculta entradas especiais na listagem normal
            tipo = "DIR" if child.is_directory else "ARQ"
            print(f"{tipo}\t{name}\t{child.size} bytes")

    def change_directory(self, target):
        # Casos especiais
        if target == ".":
            return  # Permanece no mesmo diretório
            
        if target == "..":
            self.current_dir = self.current_dir.children[".."]
            return
            
        # Busca por nome no diretório atual
        if target in self.current_dir.children:
            target_inode = self.current_dir.children[target]
            if target_inode.is_directory:
                self.current_dir = target_inode
            else:
                print(f"Erro: '{target}' não é um diretório")
        else:
            print(f"Erro: Diretório '{target}' não encontrado")

    def get_current_path(self):
        # Reconstroi o caminho completo
        path_parts = []
        current = self.current_dir
        
        # Percorre até a raiz
        while current != current.parent:  # Condição de parada na raiz
            path_parts.append(current.name)
            current = current.parent
            
        path_parts.append("/")  # Adiciona raiz
        return "/".join(reversed(path_parts))

    def list_inodes(self):
        # Lista todos os i-nodes do sistema
        print("\nTabela de i-nodes:")
        for inode in self.inode_table.values():
            print(inode)

# Exemplo de uso com interface interativa
if __name__ == "__main__":
    fs = FileSystem()
    
    # Cria estrutura de exemplo
    fs.create_directory("docs")
    fs.create_directory("imagens")
    fs.create_file("leia.txt", 1200)
    
    fs.change_directory("docs")
    fs.create_file("relatorio.pdf", 4500)
    fs.create_directory("projetos")
    
    fs.change_directory("projetos")
    fs.create_file("main.py", 800)
    
    # Interface simples de navegação
    while True:
        path = fs.get_current_path()
        print(f"\n[{path}] > ", end="")
        command = input().strip().split()
        
        if not command:
            continue
            
        cmd = command[0].lower()
        args = command[1:]
        
        if cmd == "ls":
            fs.list_directory()
        elif cmd == "cd":
            if not args:
                print("Uso: cd <diretório>")
            else:
                fs.change_directory(args[0])
        elif cmd == "mkdir":
            if not args:
                print("Uso: mkdir <nome>")
            else:
                fs.create_directory(args[0])
        elif cmd == "touch":
            if not args:
                print("Uso: touch <nome> <tamanho>")
            else:
                size = int(args[1]) if len(args) > 1 else 0
                fs.create_file(args[0], size)
        elif cmd == "inodes":
            fs.list_inodes()
        elif cmd == "pwd":
            print(path)
        elif cmd == "exit":
            break
        else:
            print("Comandos disponíveis: ls, cd, mkdir, touch, inodes, pwd, exit")
