from implementacoes_lista.sistema_arquivo_encadeado import SistemaArquivosEncadeado

def main():
    fs = SistemaArquivosEncadeado()

    while True:
        cmd = input(f"\n[{fs.obter_caminho()}] $ ").strip().split()
        if not cmd:
            continue

        c = cmd[0]
        args = cmd[1:]

        if c == "ls":
            fs.listar()
        elif c == "cd":
            fs.entrar(args[0] if args else "")
        elif c == "mkdir":
            fs.criar(args[0], "diretorio")
        elif c == "touch":
            nome = args[0]
            tamanho = int(args[1]) if len(args) > 1 else 0
            fs.criar(nome, "arquivo", tamanho)
        elif c == "move":
            if len(args) < 2:
                print("Uso: move <origem> <destino>")
            else:
                fs.mover(args[0], args[1])
        elif c == "write":
            fs.escrever_arquivo(args[0], " ".join(args[1:]))
        elif c == "read":
            fs.ler_arquivo(args[0])
        elif c == "rm":
            fs.excluir(args[0])
        elif c == "exit":
            break
        else:
            print("Comandos: ls, cd, mkdir, touch, write, read, rm, exit")

if __name__ == "__main__":
    main()
