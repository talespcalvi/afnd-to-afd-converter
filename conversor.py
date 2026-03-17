import collections

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
        
        if simbolo != 'h':
            alfabeto.add(simbolo)
            
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
    estados_afd = {fecho_inicial: "Q0"}
    fila = collections.deque([fecho_inicial])
    transicoes_afd = []
    finais_afd = set()
    
    contador = 1
    while fila:
        T = fila.popleft()
        nome_origem = estados_afd[T]
        
        # Verificar se é estado final
        if any(e in estados_finais_afnd for e in T):
            finais_afd.add(nome_origem)
            
        for simbolo in alfabeto:
            U = e_closure(mover(T, simbolo, transicoes_afnd), transicoes_afnd)
            if not U: continue
            
            if U not in estados_afd:
                estados_afd[U] = f"Q{contador}"
                contador += 1
                fila.append(U)
            
            transicoes_afd.append(f"{nome_origem} {simbolo} {estados_afd[U]}")
            
    return estados_afd.values(), "Q0", finais_afd, transicoes_afd

def salvar_afd(nome_arquivo, estados, inicial, finais, transicoes):
    with open(nome_arquivo, 'w') as f:
        f.write(" ".join(sorted(list(estados))) + "\n")
        f.write(f"{inicial}\n")
        f.write(" ".join(sorted(list(finais))) + "\n")
        for t in transicoes:
            f.write(t + "\n")

# Execução principal
def main():
    # Carrega os dados conforme o formato da Linha 0 em diante [cite: 7, 9]
    estados, inicial, finais_afnd, transicoes, alfabeto = ler_afnd('entrada.txt')
    
    # Processa a conversão Parte 1 [cite: 3]
    est_afd, ini_afd, fin_afd, trans_afd = converter_para_afd(inicial, finais_afnd, transicoes, alfabeto)
    
    # Salva a saída 
    salvar_afd('saida_afd.txt', est_afd, ini_afd, fin_afd, trans_afd)
    print("Conversão concluída. Verifique 'saida_afd.txt'.")

if __name__ == "__main__":
    main()
