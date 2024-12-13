from pulp import LpMaximize, LpProblem, LpVariable
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

# Configuração da interface com Streamlit
st.title("Otimização de Produção e Lucro")
st.write("Este aplicativo calcula a produção ideal de dois produtos para maximizar o lucro.")

# Entrada de dados pelo usuário
lucro_p1 = st.number_input("Digite o lucro por unidade do produto P1:", value=1000.0)
lucro_p2 = st.number_input("Digite o lucro por unidade do produto P2:", value=1800.0)
tempo_p1 = st.number_input("Digite o tempo necessário para produzir uma unidade de P1:", value=20.0)
tempo_p2 = st.number_input("Digite o tempo necessário para produzir uma unidade de P2:", value=30.0)
tempo_disponivel = st.number_input("Digite o tempo total disponível para produção:", value=1200.0)
demanda_p1 = st.number_input("Digite a demanda máxima para o produto P1:", value=40.0)
demanda_p2 = st.number_input("Digite a demanda máxima para o produto P2:", value=30.0)

if st.button("Calcular Produção e Lucro"):
    # Criação do problema de maximização
    modelo = LpProblem(name="maximizacao-lucro", sense=LpMaximize)

    # Definição das variáveis de decisão
    x1 = LpVariable(name="x1", lowBound=0, cat="Continuous")  # Quantidade de P1 a produzir
    x2 = LpVariable(name="x2", lowBound=0, cat="Continuous")  # Quantidade de P2 a produzir

    # Função objetivo
    modelo += lucro_p1 * x1 + lucro_p2 * x2, "Lucro Total"

    # Restrições
    modelo += tempo_p1 * x1 + tempo_p2 * x2 <= tempo_disponivel, "Disponibilidade de Horas"
    modelo += x1 <= demanda_p1, "Demanda de P1"
    modelo += x2 <= demanda_p2, "Demanda de P2"

    # Resolução do problema
    modelo.solve()

    # Resultados
    lucro_maximo = modelo.objective.value()
    quantidade_p1 = x1.value()
    quantidade_p2 = x2.value()

    st.success("Cálculo concluído com sucesso!")
    st.write(f"Lucro Máximo: {lucro_maximo}")
    st.write(f"Quantidade de P1 a produzir: {quantidade_p1}")
    st.write(f"Quantidade de P2 a produzir: {quantidade_p2}")

    # Gráfico de barras para visualização dos resultados
    labels = ['Produto P1', 'Produto P2']
    quantidades = [quantidade_p1, quantidade_p2]
    lucros = [lucro_p1 * quantidade_p1, lucro_p2 * quantidade_p2]

    fig, ax1 = plt.subplots()

    # Gráfico de quantidades
    color = 'tab:blue'
    ax1.set_xlabel('Produtos')
    ax1.set_ylabel('Quantidades', color=color)
    ax1.bar(labels, quantidades, color=color, alpha=0.7, label='Quantidades Produzidas')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    # Gráfico de lucros
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Lucros', color=color)
    ax2.plot(labels, lucros, color=color, marker='o', label='Lucros Obtidos')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper right')

    # Título e exibição do gráfico
    plt.title('Resultados de Produção e Lucro')
    fig.tight_layout()

    # Mostrar o gráfico no Streamlit
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    st.image(buf)
    buf.close()
