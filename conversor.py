import collections

# --- FUNÇÕES DA PARTE 1 ---

def ler_afnd(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = [line.strip() for line in f if line.strip()]
    estados = linhas[0].split()
    estado_inicial = linhas[1]
    estados_finais_afnd = set(linhas[2].split())
    transicoes = {}
    alfabeto = set()
    for linha in linhas[3:]:
        partes = linha.split()
        if len(partes) < 3: continue
        origem, simbolo, destino = partes[0], partes[1], partes[2]
        if (origem, simbolo) not in transicoes:
            transicoes[(origem, simbolo)] = set()
        transicoes[(origem, simbolo)].add(destino)
        if simbolo != 'h': alfabeto.add(simbolo)
    return estados, estado_inicial, estados_finais_afnd, transicoes, sorted(list(alfabeto))

def e_closure(estados, transicoes):
    stack = list(estados)
    closure = set(estados)
    while stack:
        u = stack.pop()
        if (u, 'h') in transicoes:
            for v in transicoes[(u, 'h')]:
                if v not in closure:
                    closure.add(v)
                    stack.append(v)
    return frozenset(closure)

def mover(estados, simbolo, transicoes):
    resultado = set()
    for estado in estados:
        if (estado, simbolo) in transicoes:
            resultado.update(transicoes[(estado, simbolo)])
    return frozenset(resultado)

def converter_para_afd(estado_inicial_afnd, estados_finais_afnd, transicoes_afnd, alfabeto):
    fecho_inicial = e_closure([estado_inicial_afnd], transicoes_afnd)
    estados_afd_map = {fecho_inicial: "Q0"}
    fila = collections.deque([fecho_inicial])
    
    # Estrutura para o simulador da Parte 2
    dic_transicoes_afd = {} 
    finais_afd = set()
    
    contador = 1
    while fila:
        T = fila.popleft()
        nome_origem = estados_afd_map[T]
        if any(e in estados_finais_afnd for e in T):
            finais_afd.add(nome_origem)
            
        for simbolo in alfabeto:
            U = e_closure(mover(T, simbolo, transicoes_afnd), transicoes_afnd)
            if not U: continue
            if U not in estados_afd_map:
                estados_afd_map[U] = f"Q{contador}"
                contador += 1
                fila.append(U)
            
            nome_destino = estados_afd_map[U]
            dic_transicoes_afd[(nome_origem, simbolo)] = nome_destino
            
    return estados_afd_map.values(), "Q0", finais_afd, dic_transicoes_afd

# --- FUNÇÕES DA PARTE 2 ---

def testar_palavra(palavra, inicial, finais, transicoes):
    estado_atual = inicial
    for simbolo in palavra:
        # Se não houver transição para o símbolo, a palavra não é aceita
        if (estado_atual, simbolo) in transicoes:
            estado_atual = transicoes[(estado_atual, simbolo)]
        else:
            return False
    return estado_atual in finais

def processar_palavras(arquivo_entrada, arquivo_saida, inicial, finais, transicoes):
    with open(arquivo_entrada, 'r') as f:
        palavras = [line.strip() for line in f] # Lê uma palavra por linha [cite: 18]
    
    with open(arquivo_saida, 'w') as f_out:
        for p in palavras:
            # Verifica aceitação 
            resultado = "aceito" if testar_palavra(p, inicial, finais, transicoes) else "não aceito"
            f_out.write(f"{p} {resultado}\n") # Formato exigido [cite: 19, 21, 22]

# --- EXECUÇÃO ---

def main():
    # Parte 1: Conversão
    est, ini, fins_afnd, trans_afnd, alf = ler_afnd('entrada.txt')
    est_afd, ini_afd, fins_afd, trans_afd = converter_para_afd(ini, fins_afnd, trans_afnd, alf)
    
    # Salva o AFD (Opcional, mas útil para o JFLAP)
    # Aqui formatamos as transições para o arquivo de saída
    lista_trans_saida = [f"{k[0]} {k[1]} {v}" for k, v in trans_afd.items()]
    with open('saida_afd.txt', 'w') as f:
        f.write(" ".join(sorted(list(est_afd))) + "\n")
        f.write(f"{ini_afd}\n")
        f.write(" ".join(sorted(list(fins_afd))) + "\n")
        for t in lista_trans_saida: f.write(t + "\n")

    # Parte 2: Reconhecimento 
    # Certifique-se de que 'palavras.txt' existe no laboratório
    try:
        processar_palavras('palavras.txt', 'resultado_palavras.txt', ini_afd, fins_afd, trans_afd)
        print("Parte 1 e 2 concluídas com sucesso!")
    except FileNotFoundError:
        print("Aviso: 'palavras.txt' não encontrado. Parte 1 gerada em 'saida_afd.txt'.")

if __name__ == "__main__":
    main()
