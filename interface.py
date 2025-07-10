from implementacoes_inodes.sistema_arquivos import SistemaArquivos

def main():
    fs = SistemaArquivos()
    
    # Cria estrutura inicial de exemplo
    fs.criar("documentos", "diretorio")
    fs.criar("imagens", "diretorio")
    fs.criar("arquivo.txt", "arquivo", 1024)
    
    while True:
        caminho = fs.obter_caminho()
        comando = input(f"\n[{caminho}] $ ").strip().split()
        
        if not comando:
            continue
            
        cmd = comando[0].lower()
        args = comando[1:]
        
        if cmd == "ls":
            fs.listar()
            
        elif cmd == "cd":
            if not args:
                print("Uso: cd <diretório>")
            else:
                fs.entrar(args[0])
                
        elif cmd == "mkdir":
            if not args:
                print("Uso: mkdir <nome>")
            else:
                fs.criar(args[0], "diretorio")
                
        elif cmd == "touch":
            if not args:
                print("Uso: touch <nome> <tamanho>")
            else:
                tamanho = int(args[1]) if len(args) > 1 else 0
                fs.criar(args[0], "arquivo", tamanho)
                
        elif cmd == "pwd":
            fs.mostrar_caminho()
            
        elif cmd == "mv":
            if len(args) < 2:
                print("Uso: mv <origem> <destino>")
            else:
                fs.mover(args[0], args[1])

        elif cmd == "write":
            if len(args) < 2:
                print("Uso: write <arquivo> <dados>")
            else:
                fs.escrever_arquivo(args[0], " ".join(args[1:]))

        elif cmd == "read":
            if not args:
                print("Uso: read <arquivo>")
            else:
                fs.ler_arquivo(args[0])

        elif cmd == "rm":
            if not args:
                print("Uso: rm <nome>")
            else:
                fs.excluir(args[0])
            
        elif cmd == "exit":
            print("Saindo do sistema de arquivos...")
            break
            
        else:
            print("Comandos disponíveis: ls, cd, mkdir, touch, mv, pwd, exit")
            print("Exemplos:")
            print("  ls                  - Lista diretório atual")
            print("  cd documentos       - Entra no diretório 'documentos'")
            print("  mkdir fotos         - Cria novo diretório")
            print("  touch relatorio.pdf 2048 - Cria arquivo com tamanho")
            print("  mv arquivo.txt backup - Move arquivo para diretório")
            print("  pwd                 - Mostra caminho atual")

if __name__ == "__main__":
    main()
