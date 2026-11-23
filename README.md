# Controle de Logística Portuária

Projeto final de Estruturas de Dados (Tema 4). Sistema em Python, executado pelo terminal, que usa **Lista, Fila, Pilha e Árvore** para controlar a operação de um porto, com persistência em arquivo texto.

## Como executar

1. Instale o **Python 3.8 ou superior** (https://www.python.org/downloads/). Nenhuma biblioteca externa é necessária.
2. Baixe `main.py` e `README.md` e abra o terminal na pasta dos arquivos.
3. Execute:

```bash
python main.py
```

(em alguns sistemas, `python3 main.py`)

O sistema inicia **vazio**. Use o menu numérico para cadastrar dados. Use **5 - Salvar dados** para gravar em `dados_sistema.txt` (criado automaticamente na mesma pasta) e **6 - Carregar dados** para reconstruir tudo a partir do arquivo.

## Menu

| Opção | Estrutura | Operações |
|---|---|---|
| 1 | Lista | Cadastrar, listar, atualizar e remover (por ID) |
| 2 | Fila | Registrar chegada, listar, atualizar e liberar o primeiro |
| 3 | Pilha | Empilhar, listar, atualizar o topo e desempilhar |
| 4 | Árvore | Adicionar nó, listar, renomear e remover |
| 5 | Persistência | Salvar dados |
| 6 | Persistência | Carregar dados |
| 0 | - | Sair |

Na árvore, os caminhos são digitados separados por `>`, por exemplo `Santos>Lisboa`. Para criar um porto de origem, deixe o caminho do pai vazio.

## Justificativa técnica das estruturas

### Fila (`collections.deque`): chegada de caminhões
Os caminhões devem ser liberados na **ordem de chegada** (FIFO: o primeiro a entrar é o primeiro a sair). A inserção ocorre no fim (`append`) e a remoção no início (`popleft`). O `deque` faz as duas operações em tempo O(1), enquanto remover do início de uma `list` custa O(n).

### Pilha (`list`): empilhamento de contêineres
O empilhamento físico segue **LIFO**: o último contêiner colocado é o primeiro a ser retirado, pois os de baixo ficam bloqueados. `append` insere no topo e `pop` remove do topo, ambos em O(1). Por isso só o topo pode ser consultado para alteração ou remoção.

### Lista (`list` de dicionários): frota e transportadoras
O cadastro da frota é um conjunto geral, sem regra de ordem de saída, que precisa ser **consultado e alterado por posição ou por chave** (o ID). A lista permite acesso por índice, percurso completo e remoção de qualquer elemento, o que filas e pilhas não permitem.

### Árvore (dicionários aninhados): rotas marítimas
As rotas formam uma **hierarquia**: porto de origem, portos intermediários e destino final, com ramificações. Um dicionário aninhado representa isso de forma natural, em que cada chave é um porto e o valor é outro dicionário com seus destinos seguintes. A listagem usa recursão para percorrer os níveis.

```python
{"Santos": {"Lisboa": {"Roterda": {}}, "Algeciras": {}}}
```

## Formato do arquivo `dados_sistema.txt`

Um único arquivo texto, uma linha por registro, com o identificador da estrutura e campos separados por `|`:

```
LISTA|101|Transportadora Alfa|Carreta
FILA|ABC1234|Joao Silva|Aguardando
PILHA|CONT-001|Soja|Roterda
ARVORE|Santos|Lisboa|Roterda
```

- **FILA**: gravada do primeiro ao último, preservando a ordem de chegada.
- **PILHA**: gravada da base ao topo, e ao carregar o último registro volta a ser o topo.
- **ARVORE**: cada linha é o caminho da raiz até uma folha; ao carregar, os dicionários aninhados são reconstruídos.
- O caractere `|` digitado pelo usuário é substituído por `-` para não corromper o arquivo.
