from no import NO

class AVL:
    def __init__(self):
        self.__raiz = None
        self.total_rotacoes = 0
        self.palavras_descartadas = 0 # Para palavras repetidas na mesma linha

    def __altura(self, no):
        if(no == None):
            return -1
        else:
            return no.altura

    def __fatorBalanceamento(self, no):
        return self.__altura(no.esq) - self.__altura(no.dir)

    def __maior(self, x, y):
        if(x > y):
            return x
        else:
            return y

    def __RotacaoLL(self, A):
        # print('RotacaoLL: ', A.palavra) # Comentado para não poluir a saída
        self.total_rotacoes += 1
        B = A.esq
        A.esq = B.dir
        B.dir = A
        A.altura = self.__maior(self.__altura(A.esq), self.__altura(A.dir)) + 1
        B.altura = self.__maior(self.__altura(B.esq), A.altura) + 1
        return B

    def __RotacaoRR(self, A):
        # print('RotacaoRR: ', A.palavra)
        self.total_rotacoes += 1
        B = A.dir
        A.dir = B.esq
        B.esq = A
        A.altura = self.__maior(self.__altura(A.esq), self.__altura(A.dir)) + 1
        B.altura = self.__maior(self.__altura(B.dir), A.altura) + 1
        return B

    def __RotacaoLR(self, A):
        A.esq = self.__RotacaoRR(A.esq)
        A = self.__RotacaoLL(A)
        return A

    def __RotacaoRL(self, A):
        A.dir = self.__RotacaoLL(A.dir)
        A = self.__RotacaoRR(A)
        return A

    def __insereValor(self, atual, palavra, linha):
        if(atual == None): # árvore vazia ou nó folha
            novo = NO(palavra, linha)
            return novo
        else:
            if(palavra < atual.palavra):
                atual.esq = self.__insereValor(atual.esq, palavra, linha)
                if(abs(self.__fatorBalanceamento(atual)) >= 2):
                    if(palavra < atual.esq.palavra):
                        atual = self.__RotacaoLL(atual)
                    else:
                        atual = self.__RotacaoLR(atual)
            elif(palavra > atual.palavra):
                atual.dir = self.__insereValor(atual.dir, palavra, linha)
                if(abs(self.__fatorBalanceamento(atual)) >= 2):
                    if(palavra > atual.dir.palavra):
                        atual = self.__RotacaoRR(atual)
                    else:
                        atual = self.__RotacaoRL(atual)
            else:
                # Palavra já existe, adiciona a linha se não estiver na lista
                if linha not in atual.linhas:
                    atual.linhas.append(linha)
                else:
                    self.palavras_descartadas += 1
                return atual # Retorna o próprio nó sem balancear pois não mudou altura

            atual.altura = self.__maior(self.__altura(atual.esq), self.__altura(atual.dir)) + 1
            return atual

    def insere(self, palavra, linha):
        self.__raiz = self.__insereValor(self.__raiz, palavra, linha)
        return True

    def __procuraMenor(self, atual):
        no1 = atual
        no2 = atual.esq
        while(no2 != None):
            no1 = no2
            no2 = no2.esq
        return no1

    # Função estrutural de remover o NÓ da árvore
    def __removeNoEstrutural(self, atual, palavra):
        if(atual.palavra == palavra): # achou o nó a ser removido
            if(atual.esq == None or atual.dir == None): # nó tem 1 filho ou nenhum
                if(atual.esq != None):
                    atual = atual.esq
                else:
                    atual = atual.dir # Pode ser None
            else: # nó tem 2 filhos
                temp = self.__procuraMenor(atual.dir)
                atual.palavra = temp.palavra
                atual.linhas = temp.linhas # Importante copiar a lista
                atual.dir = self.__removeNoEstrutural(atual.dir, temp.palavra)
                if(abs(self.__fatorBalanceamento(atual)) >= 2):
                    if(self.__altura(atual.esq.dir) <= self.__altura(atual.esq.esq)):
                        atual = self.__RotacaoLL(atual)
                    else:
                        atual = self.__RotacaoLR(atual)

            if(atual != None):
                atual.altura = self.__maior(self.__altura(atual.esq), self.__altura(atual.dir)) + 1

        else: # procura o nó a ser removido
            if(palavra < atual.palavra):
                atual.esq = self.__removeNoEstrutural(atual.esq, palavra)
                if(abs(self.__fatorBalanceamento(atual)) >= 2):
                    if(self.__altura(atual.dir.esq) <= self.__altura(atual.dir.dir)):
                        atual = self.__RotacaoRR(atual)
                    else:
                        atual = self.__RotacaoRL(atual)
            else:
                atual.dir = self.__removeNoEstrutural(atual.dir, palavra)
                if(abs(self.__fatorBalanceamento(atual)) >= 2):
                    if(self.__altura(atual.esq.dir) <= self.__altura(atual.esq.esq)):
                        atual = self.__RotacaoLL(atual)
                    else:
                        atual = self.__RotacaoLR(atual)

            atual.altura = self.__maior(self.__altura(atual.esq), self.__altura(atual.dir)) + 1

        return atual

    # Função pública (Chamar ma main)
    def remove(self, palavra, linha):
        node = self.__buscaNo(self.__raiz, palavra)
        if not node:
            return False # Palavra não existe
        
        # Se a linha existe, remove.
        if linha in node.linhas:
            node.linhas.remove(linha)
            
            # Se a lista ficar vazia, remove o nó estruturalmente da árvore
            if len(node.linhas) == 0:
                self.__raiz = self.__removeNoEstrutural(self.__raiz, palavra)
            return True
        return False # Linha não encontrada para esta palavra

    def __buscaNo(self, atual, valor):
        if atual == None:
            return None
        if valor == atual.palavra:
            return atual
        if valor < atual.palavra:
            return self.__buscaNo(atual.esq, valor)
        else:
            return self.__buscaNo(atual.dir, valor)

    # --- Funções Extras Solicitadas ---

    # Busca Aproximada (Prefixo)
    def busca_aproximada(self, prefixo):
        resultados = []
        self.__buscaPrefixo(self.__raiz, prefixo, resultados)
        return resultados

    def __buscaPrefixo(self, no, prefixo, lista):
        if no is None:
            return
        
        # Otimização: Se o nó atual é maior que o prefixo, não precisamos ir pra direita se o começo já passou
        # Mas para simplificar e garantir, faremos varredura otimizada
        
        if no.palavra.startswith(prefixo):
            lista.append(no.palavra)
        
        if prefixo < no.palavra:
            self.__buscaPrefixo(no.esq, prefixo, lista)
        
        # Só vai para a direita se o prefixo for "maior" ou se o nó atual for prefixo
        if no.palavra[:len(prefixo)] <= prefixo:
            self.__buscaPrefixo(no.dir, prefixo, lista)

    # Medidor de Equilíbrio (ME) - Diferença de contagem de NÓS (não altura)
    def busca_me(self, palavra):
        no = self.__buscaNo(self.__raiz, palavra)
        if no is None:
            return -1 # Não encontrada
        
        qtd_esq = self.__contaNos(no.esq)
        qtd_dir = self.__contaNos(no.dir)
        me = qtd_esq - qtd_dir
        
        if me == 0:
            return 0
        
        print(f"Valor de ME: {me}")
        return 1

    def __contaNos(self, no):
        if no is None:
            return 0
        return 1 + self.__contaNos(no.esq) + self.__contaNos(no.dir)

    # Palavra mais frequente
    def palavra_mais_frequente(self):
        return self.__buscaMaisFrequente(self.__raiz)

    def __buscaMaisFrequente(self, no):
        if no is None:
            return None, 0
        
        atual_p, atual_freq = no.palavra, len(no.linhas)
        
        esq_p, esq_freq = self.__buscaMaisFrequente(no.esq)
        dir_p, dir_freq = self.__buscaMaisFrequente(no.dir)
        
        # Compara quem é maior
        melhor_p, melhor_freq = atual_p, atual_freq
        
        if esq_freq > melhor_freq:
            melhor_p, melhor_freq = esq_p, esq_freq
        
        if dir_freq > melhor_freq:
            melhor_p, melhor_freq = dir_p, dir_freq
            
        return melhor_p, melhor_freq

    # Geração do Arquivo de Índice
    def get_raiz(self):
        return self.__raiz

    def __emOrdemSalvar(self, raiz, lista_resultados):
        if(raiz != None):
            self.__emOrdemSalvar(raiz.esq, lista_resultados)
            # Formata: palavra 1, 2, 3
            linhas_str = ",".join(map(str, raiz.linhas))
            lista_resultados.append(f"{raiz.palavra} {linhas_str}")
            self.__emOrdemSalvar(raiz.dir, lista_resultados)

    def gerar_lista_ordenada(self):
        lista = []
        self.__emOrdemSalvar(self.__raiz, lista)
        return lista