**Questão 1: \[10 pontos]**

Implemente um programa em linguagem de sua escolha (C, Python, Java, etc.) que simule o funcionamento básico de um sistema de arquivos baseado em i-nodes. O sistema deve suportar as seguintes operações:

1. **Criação de Arquivos e Diretórios:**
   • Simule a criação de arquivos e diretórios. Para cada novo arquivo ou diretório, um inode deve ser criado e associado a ele.
   • Cada inode deve armazenar metadados como nome, tamanho e ponteiros para blocos de dados (usem endereços fictícios ou índices).

2. **Navegação pelo Sistema de Arquivos:**
   • Implemente a navegação entre diretórios, permitindo ao usuário listar os arquivos e subdiretórios em um diretório específico.
   • Permita que o usuário navegue para o diretório pai (`..`) e para o diretório atual (`.`).

3. **Movimentação de Arquivos:**
   • Implemente a funcionalidade para mover arquivos entre diretórios dentro do sistema de arquivos.
   • Ao mover um arquivo, o inode associado deve permanecer o mesmo, mas a entrada de diretório deve ser atualizada para refletir a nova localização.

4. **Leitura e Escrita de Arquivos:**
   • Simule a leitura e escrita em arquivos. Ao escrever, atualize o tamanho do arquivo e a lista de blocos de dados no inode.
   • Ao ler, exiba os dados armazenados nos blocos associados ao inode do arquivo.

5. **Exclusão de Arquivos e Diretórios:**
   • Permita a exclusão de arquivos e diretórios. Ao excluir, libere o inode e os blocos de dados associados.

Além disso, implemente uma versão alternativa do sistema de arquivos utilizando alocação por lista encadeada para os blocos de dados. Compare o desempenho das duas abordagens (i-nodes vs. lista encadeada) em termos de:
• Facilidade de navegação e acesso aleatório;
• Eficiência nas operações de leitura, escrita e movimentação de arquivos;
• Simplicidade e clareza da implementação.

**Critérios para Avaliação:**
• Implementação e aderência aos requisitos.
• Apresentação e discussão em sala.
