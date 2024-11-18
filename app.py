import streamlit as st  # Importa o módulo streamlit para criar a interface de usuário.
import requests  # Importa o módulo requests para fazer requisições HTTP.
import matplotlib.pyplot as plt  # Importa o matplotlib para criar gráficos.

# Função para obter dados do CEP usando a API ViaCEP
def obter_dados_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"  # Define a URL da API ViaCEP para consultar o CEP.
    resposta = requests.get(url)  # Faz uma requisição GET para a URL da API.
    return resposta.json()  # Retorna a resposta da API como um dicionário JSON.

# Função para exibir gráficos de despesas
def grafico_financas(salario, despesas):
    categorias = list(despesas.keys())  # Cria uma lista com as categorias de despesas.
    valores = list(despesas.values())  # Cria uma lista com os valores das despesas.

    fig, ax = plt.subplots()  # Cria uma figura e um eixo para o gráfico.
    ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90)  # Cria o gráfico de pizza com os dados de despesas.
    ax.axis('equal')  # Garante que o gráfico de pizza tenha formato circular.

    ax.set_title('Distribuição de Despesas')  # Define o título do gráfico.

    st.pyplot(fig)  # Exibe o gráfico gerado pelo matplotlib na interface Streamlit.

# Interface Streamlit
st.title("Aplicativo de Controle de Finanças Pessoais")  # Define o título principal da aplicação.

# Entrada do perfil do usuário
st.header("Perfil do Usuário")  # Exibe um cabeçalho para a seção de perfil do usuário.
nome = st.text_input("Nome", "")  # Solicita ao usuário que insira seu nome.
email = st.text_input("Email", "")  # Solicita ao usuário que insira seu email.

# Verificação simples de preenchimento
if nome and email:  # Verifica se tanto o nome quanto o email foram preenchidos.
    st.write(f"Perfil de usuário: **{nome}** | **{email}**")  # Exibe o perfil do usuário.
else:
    st.warning("Por favor, preencha o nome e o email.")  # Exibe um aviso caso o nome ou email não tenha sido preenchido.

# Entrada de CEP para obter o endereço
st.header("Consulta de Endereço pelo CEP")  # Exibe um cabeçalho para a seção de consulta de endereço.
cep = st.text_input("Digite o CEP (somente números):")  # Solicita ao usuário que insira um CEP.

if cep:  # Se o CEP foi inserido...
    dados = obter_dados_cep(cep)  # Chama a função obter_dados_cep para obter os dados do endereço a partir do CEP.
    if 'erro' not in dados:  # Se não houver erro na resposta da API (ou seja, CEP válido).
        st.write(f"**Endereço**: {dados['logradouro']}")  # Exibe o logradouro.
        st.write(f"**Bairro**: {dados['bairro']}")  # Exibe o bairro.
        st.write(f"**Cidade**: {dados['localidade']}")  # Exibe a cidade.
        st.write(f"**Estado**: {dados['uf']}")  # Exibe o estado.
    else:
        st.error("CEP não encontrado ou inválido.")  # Exibe uma mensagem de erro caso o CEP seja inválido.

# Inicializando a variável total_despesas com 0 antes de usá-la
total_despesas = 0.0

# Entrada de finanças
st.header("Controle de Finanças Pessoais")  # Exibe um cabeçalho para a seção de controle de finanças pessoais.
salario = st.number_input("Salário Mensal", min_value=0.0, step=1000.0)  # Solicita ao usuário o salário mensal, com valores mínimos de 0.0 e incremento de 1000.0.
gastos = st.text_area("Despesas Mensais (em formato 'categoria: valor')", "")  # Solicita ao usuário que insira as despesas mensais no formato "categoria: valor".

# Processando as despesas
if gastos:  # Se o campo de despesas não estiver vazio...
    despesas = {}  # Inicializa um dicionário vazio para armazenar as despesas.
    try:
        for item in gastos.splitlines():  # Separa as linhas das despesas inseridas.
            categoria, valor = item.split(":")  # Divide cada linha em categoria e valor.
            despesas[categoria.strip()] = float(valor.strip())  # Adiciona a categoria e o valor no dicionário de despesas.
    except ValueError:  # Se houver erro ao tentar processar o formato...
        st.error("Formato incorreto. Use o formato 'categoria: valor'.")  # Exibe uma mensagem de erro.

    # Mostrando total de despesas
    total_despesas = sum(despesas.values())  # Soma todos os valores das despesas.
    st.write(f"**Total de Despesas:** R${total_despesas:.2f}")  # Exibe o total das despesas.

    # Exibindo gráfico de despesas
    if despesas:  # Se houver despesas a serem exibidas...
        grafico_financas(salario, despesas)  # Exibe o gráfico de distribuição de despesas.

# Exibindo um resumo financeiro
if salario > 0 and total_despesas > 0:  # Se o salário e o total de despesas forem maiores que zero...
    saldo = salario - total_despesas  # Calcula o saldo restante (salário - total de despesas).
    st.write(f"**Saldo Restante:** R${saldo:.2f}")  # Exibe o saldo restante.
else:
    st.write("Digite o salário e as despesas para calcular o saldo restante.")  # Exibe uma mensagem caso o salário ou as despesas não tenham sido inseridos.
