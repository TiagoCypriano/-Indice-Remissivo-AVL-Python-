# Índice Remissivo com Árvore AVL

Implementação de um índice remissivo em Python utilizando Árvore AVL. O sistema mapeia palavras de um arquivo de texto para as linhas onde ocorrem, garantindo buscas e inserções em tempo logarítmico através do balanceamento automático.

## Introdução e Estrutura

### O Problema
O objetivo é indexar todas as palavras de um texto (ignorando *case* e pontuação). Diferente de uma árvore binária comum, a AVL evita a degeneração da estrutura, mantendo a altura controlada para otimizar a performance em textos longos.

### A Solução
* **Estrutura de Dados:** Árvore Binária de Busca Balanceada (AVL).
* **Lógica de Nó:** Cada nó representa uma palavra única (`chave`) e contém uma lista de inteiros (`valor`) representando as linhas.
* **Tratamento de Duplicatas:** Se a palavra já existe na árvore, não se cria um novo nó; apenas adiciona-se o número da nova linha à lista existente.
* **Armazenamento:** Arquivos modulares (`no.py`, `avl.py`, `main.py`).

---

## Documentação do Código

### 1. `no.py`
Define a classe **`NO`**.
* **Atributos:**
    * `palavra`: String (chave de ordenação).
    * `linhas`: Lista de inteiros (ocorrências no texto).
    * `altura`: Inteiro para cálculo do fator de balanceamento.
    * `esq` / `dir`: Referências para os filhos.

### 2. `avl.py`
Núcleo da lógica de dados. Principais métodos:
* **`insere(palavra, linha)`**: Insere recursivamente. Se a palavra já existe, apenas dá *append* na lista de linhas. Atualiza a altura e aplica rotações (`LL`, `RR`, `LR`, `RL`) se o fator de balanceamento $|fb| > 1$.
* **`remove(palavra, linha)`**: Remove a linha específica da lista do nó. Se a lista ficar vazia, remove o nó fisicamente da árvore e rebalanceia.
* **`busca_aproximada(prefixo)`**: Retorna lista de palavras que começam com o prefixo informado. Otimiza a busca podando subárvores irrelevantes.
* **`busca_me(palavra)`**: Calcula o **Medidor de Equilíbrio (ME)** baseado na *quantidade de nós* (não altura). Retorna:
    * `0`: Subárvores com mesmo número de nós.
    * Valor do ME: Diferença entre nós da esquerda e direita.
    * `-1`: Palavra não encontrada.
* **`gerar_lista_ordenada()`**: Percurso *in-order* para gerar a saída alfabética.

### 3. `main.py`
Controlador da aplicação.
* **Processamento:** Lê `texto_origem.txt`, sanitiza strings (remove pontuação/lower case) e povoa a árvore.
* **Menu CLI:** Loop interativo para operações de busca exata, busca por prefixo, estatísticas e remoção.
* **Relatório:** Gera `indice.txt` contendo as palavras ordenadas e metadados (tempo de execução, nº de rotações, palavras distintas).

---

## Exemplos de Uso

### 1. Entrada de Dados
Arquivo: `texto_origem.txt`
```text
O rato roeu a roupa do rei.
O rei riu.
```

### 2. Execução e Interação (Menu)
Ao executar o programa, o texto é carregado e um menu interativo é exibido. Abaixo, um exemplo de busca por prefixo ("r") e consulta de palavra mais frequente:
Carregando arquivo 'texto_origem.txt'...
Árvore carregada! (0.0005s)
```text
========================================
      SISTEMA DE ÍNDICE REMISSIVO (AVL)
========================================
1. Buscar Palavra (Verificar ME e Linhas)
2. Busca Aproximada (Por Prefixo)
3. Remover Linha de uma Palavra
4. Ver Palavra Mais Frequente
5. Sair e Salvar Índice
----------------------------------------
Escolha uma opção: 2

Digite o prefixo (ex: 'alg'): r

Palavras iniciadas com 'r':
rato, rei, riu, roeu, roupa
```

### 3. Saída Final (indice.txt)
O arquivo é gerado no início e atualizado ao selecionar a opção 5 (Sair e Salvar Alterações).

Baseado no texto de exemplo acima, o conteúdo do arquivo gerado será:

```text
O rato roeu a roupa do rei.
O rei riu.

a 1.
do 1.
o 1,2
rato 1
rei 1,2
riu 2
roeu 1
roupa 1

------------------------------
Número total de palavras: 10
Número de palavras distintas: 8
Número de palavras descartadas (repetidas na linha): 0
Tempo de construção do índice: 0.0005s
Total de rotações executadas: 4

```
### Como Executar
Certifique-se de ter o Python 3 instalado.

Mantenha os arquivos avl.py, no.py, main.py e texto_origem.txt no mesmo diretório.

Execute no terminal:
Bash
python main.py
