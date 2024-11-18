import re
from collections import Counter
from tkinter import Tk, Label, Button, Text, filedialog

def processar_texto(texto):
    palavras = texto.split()
    num_palavras = len(palavras)

    # Divisão do texto em frases usando expressão regular
    frases = re.split(r'[.!?]', texto)
    num_frases = len([frase for frase in frases if frase.strip()])

    # Convertendo as palavras para minúsculas para uma contagem consistente
    palavras_lower = [palavra.lower() for palavra in palavras]
    freq_palavras = Counter(palavras_lower)

    # Verificar se o dicionário de palavras tem pelo menos uma palavra antes de tentar acessar
    if freq_palavras:
        palavra_mais_frequente, contagem_max = freq_palavras.most_common(1)[0]
    else:
        palavra_mais_frequente, contagem_max = ("Nenhuma", 0)

    # Contando os caracteres de cada tipo
    letras = sum(1 for char in texto if char.isalpha())
    numeros = sum(1 for char in texto if char.isdigit())
    pontuacao = sum(1 for char in texto if char in ",.!?;:'\"()[]{}-")
    outros = len(texto) - (letras + numeros + pontuacao)

    return {
        "num_palavras": num_palavras,
        "num_frases": num_frases,
        "freq_palavras": freq_palavras,
        "palavra_mais_frequente": (palavra_mais_frequente, contagem_max),
        "letras": letras,
        "numeros": numeros,
        "pontuacao": pontuacao,
        "outros": outros
    }

def exibir_resultados(analise):
    resultado = f'''
    Número de palavras: {analise["num_palavras"]}
    Número de frases: {analise["num_frases"]}
    Palavra mais frequente: {analise["palavra_mais_frequente"][0]} (ocorre {analise["palavra_mais_frequente"][1]} vezes)
    
    Frequência das palavras:
    '''
    for palavra, freq in analise["freq_palavras"].items():
        resultado += f"{palavra}: {freq}\n"
    
    resultado += f'''
    Caracteres:
    Letras: {analise["letras"]}
    Números: {analise["numeros"]}
    Pontuação: {analise["pontuacao"]}
    Outros: {analise["outros"]}
    '''
    
    texto_resultados.delete(1.0, "end")
    texto_resultados.insert("insert", resultado)

def carregar_arquivo():
    arquivo = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("Markdown files", "*.md")])
    if arquivo:
        with open(arquivo, 'r', encoding='utf-8') as file:
            texto = file.read()
            analise = processar_texto(texto)
            exibir_resultados(analise)

def analisar_texto():
    texto = campo_texto.get("1.0", "end-1c")
    analise = processar_texto(texto)
    exibir_resultados(analise)

# Interface gráfica
root = Tk()
root.title("Analisador de Texto")

# Estilização dos elementos
root.config(bg="#f0f0f0")  # Cor de fundo da janela
font_label = ("Arial", 12, "bold")
font_texto = ("Arial", 10)

# Label
Label(root, text="Digite ou cole seu texto abaixo:", bg="#f0f0f0", font=font_label).pack(pady=10)

# Campo de texto
campo_texto = Text(root, height=10, width=50, font=font_texto)
campo_texto.pack(pady=10)

# Botões com estilização
botao_estilo = {
    "bg": "#90EE90",  # Verde claro
    "fg": "black",  # Cor do texto
    "font": ("Arial", 12, "bold"),
    "bd": 10,  # Largura da borda
    "relief": "flat",  # Borda suave
    "width": 20,  # Largura do botão
    "height": 1,  # Altura do botão
    "padx": 10,
    "pady": 10
}

Button(root, text="Analisar Texto", command=analisar_texto, **botao_estilo).pack(pady=10)
Button(root, text="Carregar Arquivo", command=carregar_arquivo, **botao_estilo).pack(pady=10)

# Área de resultados
texto_resultados = Text(root, height=15, width=50, font=font_texto)
texto_resultados.pack(pady=10)

root.mainloop()