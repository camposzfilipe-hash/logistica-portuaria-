"""
Projeto Final - Estruturas de Dados
Tema 4: Controle de Logística Portuária

Estruturas utilizadas:
  - Lista  (list)         -> frota de veículos e transportadoras credenciadas
  - Fila   (deque)        -> caminhões aguardando liberação no pátio (FIFO)
  - Pilha  (list)         -> contêineres empilhados no navio/pátio (LIFO)
  - Árvore (dict aninhado)-> rotas marítimas, portos intermediários e destinos

Persistência: um único arquivo texto chamado dados_sistema.txt
"""

from collections import deque

ARQUIVO = "dados_sistema.txt"
SEP = "|"  # delimitador do arquivo texto

# ---------------------------------------------------------------------------
# ESTRUTURAS EM MEMÓRIA (o sistema começa totalmente vazio)
# ---------------------------------------------------------------------------
frota = []        # LISTA: cada item é um dict {"id", "nome", "tipo"}
fila_patio = deque()  # FILA: cada item é um dict {"placa", "motorista", "status"}
pilha_conteineres = []  # PILHA: cada item é um dict {"codigo", "carga", "destino"}; o topo é o último
arvore_rotas = {}  # ÁRVORE: dicionários aninhados {"Santos": {"Lisboa": {"Roterda": {}}}}


# ---------------------------------------------------------------------------
# FUNÇÕES AUXILIARES DE ENTRADA
# ---------------------------------------------------------------------------
def ler_texto(mensagem):
    """Lê um texto não vazio. Troca '|' por '-' para não quebrar o arquivo."""
    while True:
        valor = input(mensagem).strip().replace(SEP, "-")
        if valor:
            return valor
        print("Valor obrigatório. Tente novamente.")


# ---------------------------------------------------------------------------
# LISTA: frota e transportadoras (acesso por chave = id)
# ---------------------------------------------------------------------------
def buscar_veiculo(id_veiculo):
    """Percorre a lista procurando o id. Retorna o registro ou None."""
    for veiculo in frota:
        if veiculo["id"] == id_veiculo:
            return veiculo
    return None


def criar_veiculo():
    id_veiculo = ler_texto("ID do veículo/transportadora: ")
    if buscar_veiculo(id_veiculo):
        print("Já existe um registro com esse ID.")
        return
    nome = ler_texto("Nome da transportadora/veículo: ")
    tipo = ler_texto("Tipo (ex: Carreta, Truck): ")
    frota.append({"id": id_veiculo, "nome": nome, "tipo": tipo})  # insere no fim da lista
    print("Registro cadastrado.")


def listar_frota():
    if not frota:
        print("Frota vazia.")
        return
    for i, v in enumerate(frota):
        print(f"[{i}] ID: {v['id']} | Nome: {v['nome']} | Tipo: {v['tipo']}")


def atualizar_veiculo():
    veiculo = buscar_veiculo(ler_texto("ID do registro a atualizar: "))
    if not veiculo:
        print("Registro não encontrado.")
        return
    veiculo["nome"] = ler_texto(f"Novo nome (atual: {veiculo['nome']}): ")
    veiculo["tipo"] = ler_texto(f"Novo tipo (atual: {veiculo['tipo']}): ")
    print("Registro atualizado.")


def remover_veiculo():
    veiculo = buscar_veiculo(ler_texto("ID do registro a remover: "))
    if not veiculo:
        print("Registro não encontrado.")
        return
    frota.remove(veiculo)
    print("Registro removido.")


# ---------------------------------------------------------------------------
# FILA: caminhões no pátio (entra no FIM, sai do INÍCIO)
# ---------------------------------------------------------------------------
def chegada_caminhao():
    placa = ler_texto("Placa do caminhão: ")
    motorista = ler_texto("Motorista: ")
    fila_patio.append({"placa": placa, "motorista": motorista, "status": "Aguardando"})  # enqueue
    print(f"Caminhão {placa} entrou na fila (posição {len(fila_patio)}).")


def listar_fila():
    if not fila_patio:
        print("Fila vazia.")
        return
    for pos, c in enumerate(fila_patio, start=1):
        print(f"{pos}º | Placa: {c['placa']} | Motorista: {c['motorista']} | Status: {c['status']}")


def atualizar_caminhao():
    placa = ler_texto("Placa do caminhão a atualizar: ")
    for c in fila_patio:
        if c["placa"] == placa:
            c["motorista"] = ler_texto(f"Novo motorista (atual: {c['motorista']}): ")
            c["status"] = ler_texto(f"Novo status (atual: {c['status']}): ")
            print("Caminhão atualizado (a posição na fila não muda).")
            return
    print("Caminhão não encontrado na fila.")


def liberar_caminhao():
    if not fila_patio:
        print("Fila vazia, ninguém para liberar.")
        return
    c = fila_patio.popleft()  # dequeue: sempre remove o primeiro que chegou
    print(f"Caminhão {c['placa']} ({c['motorista']}) liberado para embarque.")


# ---------------------------------------------------------------------------
# PILHA: contêineres (push/pop SOMENTE no topo)
# ---------------------------------------------------------------------------
def empilhar_conteiner():
    codigo = ler_texto("Código do contêiner: ")
    carga = ler_texto("Carga: ")
    destino = ler_texto("Destino: ")
    pilha_conteineres.append({"codigo": codigo, "carga": carga, "destino": destino})  # push
    print(f"Contêiner {codigo} empilhado no topo.")


def listar_pilha():
    if not pilha_conteineres:
        print("Pilha vazia.")
        return
    print("(topo primeiro)")
    for pos, c in enumerate(reversed(pilha_conteineres)):
        marca = " <- TOPO" if pos == 0 else ""
        print(f"Código: {c['codigo']} | Carga: {c['carga']} | Destino: {c['destino']}{marca}")


def atualizar_topo():
    if not pilha_conteineres:
        print("Pilha vazia.")
        return
    topo = pilha_conteineres[-1]  # só o topo pode ser alterado (regra da pilha)
    topo["carga"] = ler_texto(f"Nova carga (atual: {topo['carga']}): ")
    topo["destino"] = ler_texto(f"Novo destino (atual: {topo['destino']}): ")
    print("Contêiner do topo atualizado.")


def desempilhar_conteiner():
    if not pilha_conteineres:
        print("Pilha vazia.")
        return
    c = pilha_conteineres.pop()  # pop: remove o último que entrou
    print(f"Contêiner {c['codigo']} removido do topo.")


# ---------------------------------------------------------------------------
# ÁRVORE: rotas marítimas (dicionários aninhados)
# Os caminhos são digitados separados por '>' (ex: Santos>Lisboa)
# ---------------------------------------------------------------------------
def separar_caminho(texto):
    """Transforma 'Santos > Lisboa' em ['Santos', 'Lisboa']. Texto vazio = raiz."""
    return [parte.strip() for parte in texto.split(">") if parte.strip()]


def navegar(partes):
    """Desce na árvore seguindo a lista de nomes. Retorna o dict do nó ou None."""
    no = arvore_rotas
    for nome in partes:
        if nome not in no:
            return None
        no = no[nome]
    return no


def adicionar_no():
    print("Deixe o caminho do pai vazio para criar um porto de origem (raiz).")
    caminho_pai = separar_caminho(input("Caminho do pai (ex: Santos>Lisboa): ").replace(SEP, "-"))
    pai = navegar(caminho_pai)
    if pai is None:
        print("Caminho do pai não encontrado.")
        return
    nome = ler_texto("Nome do novo porto/destino: ")
    if nome in pai:
        print("Esse nó já existe nesse nível.")
        return
    pai[nome] = {}  # novo nó começa sem filhos
    print("Nó adicionado.")


def imprimir_arvore(no, nivel=0):
    """Impressão recursiva com recuo proporcional à profundidade."""
    for nome, filhos in no.items():
        print("    " * nivel + ("└── " if nivel else "") + nome)
        imprimir_arvore(filhos, nivel + 1)


def listar_arvore():
    if not arvore_rotas:
        print("Nenhuma rota cadastrada.")
        return
    imprimir_arvore(arvore_rotas)


def atualizar_no():
    partes = separar_caminho(input("Caminho completo do nó a renomear (ex: Santos>Lisboa): "))
    if not partes:
        print("Caminho inválido.")
        return
    pai = navegar(partes[:-1])
    if pai is None or partes[-1] not in pai:
        print("Nó não encontrado.")
        return
    novo = ler_texto("Novo nome: ")
    if novo in pai and novo != partes[-1]:
        print("Já existe um nó com esse nome nesse nível.")
        return
    # reconstrói o dict do pai para manter a ordem dos filhos
    novo_pai = {(novo if chave == partes[-1] else chave): valor for chave, valor in pai.items()}
    pai.clear()
    pai.update(novo_pai)
    print("Nó renomeado.")


def remover_no():
    partes = separar_caminho(input("Caminho completo do nó a remover (ex: Santos>Lisboa): "))
    if not partes:
        print("Caminho inválido.")
        return
    pai = navegar(partes[:-1])
    if pai is None or partes[-1] not in pai:
        print("Nó não encontrado.")
        return
    del pai[partes[-1]]  # remove o nó e toda a subárvore dele
    print("Nó (e seus descendentes) removido.")


# ---------------------------------------------------------------------------
# PERSISTÊNCIA: arquivo texto único (dados_sistema.txt)
# ---------------------------------------------------------------------------
def caminhos_da_arvore(no, prefixo=()):
    """Gera todos os caminhos da raiz até cada folha (um por linha do arquivo)."""
    for nome, filhos in no.items():
        caminho = prefixo + (nome,)
        if filhos:
            yield from caminhos_da_arvore(filhos, caminho)
        else:
            yield caminho  # folha: grava o caminho completo


def salvar_dados():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arq:
            for v in frota:
                arq.write(SEP.join(["LISTA", v["id"], v["nome"], v["tipo"]]) + "\n")
            for c in fila_patio:  # do primeiro ao último da fila
                arq.write(SEP.join(["FILA", c["placa"], c["motorista"], c["status"]]) + "\n")
            for c in pilha_conteineres:  # da base ao topo (o topo fica por último)
                arq.write(SEP.join(["PILHA", c["codigo"], c["carga"], c["destino"]]) + "\n")
            for caminho in caminhos_da_arvore(arvore_rotas):
                arq.write(SEP.join(["ARVORE", *caminho]) + "\n")
        print(f"Dados salvos em {ARQUIVO}.")
    except OSError as erro:
        print(f"Erro ao salvar: {erro}")


def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arq:
            linhas = arq.read().splitlines()
    except FileNotFoundError:
        print("Arquivo ainda não existe. Salve os dados primeiro.")
        return
    except OSError as erro:
        print(f"Erro ao carregar: {erro}")
        return

    # limpa a memória antes de reconstruir
    frota.clear()
    fila_patio.clear()
    pilha_conteineres.clear()
    arvore_rotas.clear()

    for linha in linhas:
        campos = linha.split(SEP)
        tipo = campos[0]
        if tipo == "LISTA" and len(campos) == 4:
            frota.append({"id": campos[1], "nome": campos[2], "tipo": campos[3]})
        elif tipo == "FILA" and len(campos) == 4:
            fila_patio.append({"placa": campos[1], "motorista": campos[2], "status": campos[3]})
        elif tipo == "PILHA" and len(campos) == 4:
            pilha_conteineres.append({"codigo": campos[1], "carga": campos[2], "destino": campos[3]})
        elif tipo == "ARVORE" and len(campos) >= 2:
            no = arvore_rotas
            for nome in campos[1:]:
                no = no.setdefault(nome, {})  # cria o nó se não existir e desce
        # linhas inválidas são ignoradas
    print("Dados carregados.")


# ---------------------------------------------------------------------------
# MENUS
# ---------------------------------------------------------------------------
def submenu(titulo, opcoes):
    """Mostra um submenu genérico. opcoes: lista de (texto, função)."""
    while True:
        print(f"\n--- {titulo} ---")
        for i, (texto, _) in enumerate(opcoes, start=1):
            print(f"{i} - {texto}")
        print("0 - Voltar")
        escolha = input("Escolha: ").strip()
        if escolha == "0":
            return
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            opcoes[int(escolha) - 1][1]()
        else:
            print("Opção inválida.")


def menu_principal():
    while True:
        print("\n===== LOGÍSTICA PORTUÁRIA =====")
        print("1 - Frota e transportadoras (Lista)")
        print("2 - Pátio de caminhões (Fila)")
        print("3 - Contêineres (Pilha)")
        print("4 - Rotas marítimas (Árvore)")
        print("5 - Salvar dados")
        print("6 - Carregar dados")
        print("0 - Sair")
        escolha = input("Escolha: ").strip()

        if escolha == "1":
            submenu("FROTA (LISTA)", [
                ("Cadastrar", criar_veiculo), ("Listar", listar_frota),
                ("Atualizar", atualizar_veiculo), ("Remover", remover_veiculo)])
        elif escolha == "2":
            submenu("PÁTIO (FILA)", [
                ("Registrar chegada (entra no fim)", chegada_caminhao), ("Listar fila", listar_fila),
                ("Atualizar caminhão", atualizar_caminhao), ("Liberar o primeiro (sai do início)", liberar_caminhao)])
        elif escolha == "3":
            submenu("CONTÊINERES (PILHA)", [
                ("Empilhar no topo", empilhar_conteiner), ("Listar pilha", listar_pilha),
                ("Atualizar o topo", atualizar_topo), ("Desempilhar o topo", desempilhar_conteiner)])
        elif escolha == "4":
            submenu("ROTAS (ÁRVORE)", [
                ("Adicionar porto/destino", adicionar_no), ("Listar árvore", listar_arvore),
                ("Renomear nó", atualizar_no), ("Remover nó", remover_no)])
        elif escolha == "5":
            salvar_dados()
        elif escolha == "6":
            carregar_dados()
        elif escolha == "0":
            print("Encerrando. Dados não salvos serão perdidos.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()
