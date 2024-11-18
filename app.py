import streamlit as st
import requests
import matplotlib.pyplot as plt

# Função para obter dados do CEP usando a API ViaCEP
def obter_dados_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)
    return resposta.json()

# Função para exibir gráficos de despesas
def grafico_financas(salario, despesas):
    categorias = list(despesas.keys())
    valores = list(despesas.values())

    fig, ax = plt.subplots()
    ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Garantir que o gráfico seja circular

    ax.set_title('Distribuição de Despesas')

    st.pyplot(fig)

# Interface Streamlit
st.title("Aplicativo de Controle de Finanças Pessoais")

# Entrada do perfil do usuário
st.header("Perfil do Usuário")
nome = st.text_input("Nome", "")
email = st.text_input("Email", "")

# Verificação simples de preenchimento
if nome and email:
    st.write(f"Perfil de usuário: **{nome}** | **{email}**")
else:
    st.warning("Por favor, preencha o nome e o email.")

# Entrada de CEP para obter o endereço
st.header("Consulta de Endereço pelo CEP")
cep = st.text_input("Digite o CEP (somente números):")

if cep:
    dados = obter_dados_cep(cep)
    if 'erro' not in dados:
        st.write(f"**Endereço**: {dados['logradouro']}")
        st.write(f"**Bairro**: {dados['bairro']}")
        st.write(f"**Cidade**: {dados['localidade']}")
        st.write(f"**Estado**: {dados['uf']}")
    else:
        st.error("CEP não encontrado ou inválido.")

# Entrada de finanças
st.header("Controle de Finanças Pessoais")
salario = st.number_input("Salário Mensal", min_value=0.0, step=1000.0)
gastos = st.text_area("Despesas Mensais (em formato 'categoria: valor')", "")

# Processando as despesas
if gastos:
    despesas = {}
    try:
        for item in gastos.splitlines():
            categoria, valor = item.split(":")
            despesas[categoria.strip()] = float(valor.strip())
    except ValueError:
        st.error("Formato incorreto. Use o formato 'categoria: valor'.")
    
    # Mostrando total de despesas
    total_despesas = sum(despesas.values())
    st.write(f"**Total de Despesas:** R${total_despesas:.2f}")
    
    # Exibindo gráfico de despesas
    if despesas:
        grafico_financas(salario, despesas)

# Exibindo um resumo financeiro
if salario > 0 and total_despesas > 0:
    saldo = salario - total_despesas
    st.write(f"**Saldo Restante:** R${saldo:.2f}")
else:
    st.write("Digite o salário e as despesas para calcular o saldo restante.")
