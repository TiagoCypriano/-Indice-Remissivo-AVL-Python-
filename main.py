import time
import string
import sys
import os
from avl import AVL


# --- Funções Auxiliares de Leitura e Escrita ---

def processar_texto(nome_arquivo):
    """
    Lê o arquivo, processa as palavras e insere na AVL.
    Retorna a árvore, total de palavras processadas e o tempo de execução.
    """
    arvore = AVL()
    total_palavras = 0
    inicio = time.time()

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            tabela_traducao = str.maketrans('', '', string.punctuation)

            for i, linha in enumerate(f, 1):
                # Remove pontuação e coloca em minúsculo
                linha_limpa = linha.translate(tabela_traducao).lower()

                # Separa palavras
                palavras = linha_limpa.split()

                for p in palavras:
                    if p.strip():
                        total_palavras += 1
                        arvore.insere(p, i)

    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{nome_arquivo}' não foi encontrado.")
        print("Certifique-se de que o arquivo está na mesma pasta do script.")
        return None, 0, 0

    fim = time.time()
    return arvore, total_palavras, (fim - inicio)


def salvar_indice(arvore, total_palavras, tempo_construcao, nome_saida="indice.txt"):
    """
    Gera o arquivo final com o índice remissivo e as estatísticas.
    """
    lista_ordenada = arvore.gerar_lista_ordenada()
    total_distintas = len(lista_ordenada)

    try:
        # Salva o índice na mesma pasta do script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        caminho_saida = os.path.join(BASE_DIR, nome_saida)

        with open(caminho_saida, "w", encoding='utf-8') as f:
            f.write("\n".join(lista_ordenada))
            f.write("\n" + "-" * 30 + "\n")
            f.write(f"Número total de palavras: {total_palavras}\n")
            f.write(f"Número de palavras distintas: {total_distintas}\n")
            f.write(f"Número de palavras descartadas (repetidas na linha): {arvore.palavras_descartadas}\n")
            f.write(f"Tempo de construção do índice: {tempo_construcao:.4f}s\n")
            f.write(f"Total de rotações executadas: {arvore.total_rotacoes}\n")

        print(f"[ARQUIVO] '{nome_saida}' atualizado com sucesso.")

    except Exception as e:
        print(f"\n[ERRO] Não foi possível salvar o arquivo: {e}")


# --- Menu Interativo ---

def exibir_menu():
    print("\n" + "=" * 40)
    print("      SISTEMA DE ÍNDICE REMISSIVO (AVL)")
    print("=" * 40)
    print("1. Buscar Palavra (Verificar ME e Linhas)")
    print("2. Busca Aproximada (Por Prefixo)")
    print("3. Remover Linha de uma Palavra")
    print("4. Ver Palavra Mais Frequente")
    print("5. Sair e Salvar Alterações")
    print("-" * 40)


def main():
    # Caminho absoluto da pasta onde o main.py está
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    nome_arquivo = os.path.join(BASE_DIR, "texto_origem.txt")

    print(f"Carregando arquivo '{nome_arquivo}'...")

    # 1. Carrega a árvore inicial
    arvore, total_palavras, tempo = processar_texto(nome_arquivo)

    if not arvore:
        sys.exit(1)

    print(f"Árvore carregada! ({tempo:.4f}s)")

    # Gera índice inicial
    print("Gerando índice inicial em disco...")
    salvar_indice(arvore, total_palavras, tempo)
    print("-" * 40)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            palavra = input("\nDigite a palavra para buscar: ").lower().strip()
            print(f"--- Resultado para '{palavra}' ---")

            res_me = arvore.busca_me(palavra)

            if res_me == -1:
                print(">> Palavra NÃO encontrada no texto.")
            elif res_me == 0:
                print(">> Palavra encontrada. ME = 0 (Subárvores equilibradas).")
            else:
                print(">> Palavra encontrada. (Valor do ME impresso acima).")

        elif opcao == '2':
            prefixo = input("\nDigite o prefixo (ex: 'alg'): ").lower().strip()
            resultados = arvore.busca_aproximada(prefixo)

            if resultados:
                print(f"\nPalavras iniciadas com '{prefixo}':")
                print(", ".join(resultados))
            else:
                print(f"\nNenhuma palavra encontrada com o prefixo '{prefixo}'.")

        elif opcao == '3':
            palavra = input("\nDigite a palavra: ").lower().strip()
            try:
                linha = int(input("Digite o número da linha a remover: "))

                sucesso = arvore.remove(palavra, linha)

                if sucesso:
                    print(f"\n[SUCESSO] Linha {linha} removida da palavra '{palavra}'.")
                    print("Nota: O arquivo 'indice.txt' será atualizado ao sair.")
                else:
                    print("\n[FALHA] Palavra ou linha inexistente.")

            except ValueError:
                print("\n[ERRO] Digite um número inteiro válido.")

        elif opcao == '4':
            p_freq, qtd = arvore.palavra_mais_frequente()

            if p_freq:
                print(f"\nA palavra mais frequente é: '{p_freq}'")
                print(f"Ela aparece em {qtd} linhas diferentes.")
            else:
                print("\nA árvore está vazia.")

        elif opcao == '5':
            print("\nAtualizando arquivo de índice final com as alterações...")
            salvar_indice(arvore, total_palavras, tempo)
            print("Encerrando programa. Até logo!")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()