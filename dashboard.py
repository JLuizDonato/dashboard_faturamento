import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar a página para exibição em modo wide
st.set_page_config(layout="wide")

# Carregar os dados da planilha
file_path =  r'clientes_v2.xlsx'
clientes_df = pd.read_excel(file_path)

# Remover NaNs das colunas que serão usadas como filtros
clientes_df['Nome Prestador'].fillna('Desconhecido', inplace=True)
clientes_df['Status Mediçao'].fillna('Desconhecido', inplace=True)
clientes_df['Período'].fillna('Desconhecido', inplace=True)
clientes_df['Status Faturamento'].fillna('Desconhecido', inplace=True)
clientes_df['Objeto'].fillna('Desconhecido', inplace=True)
clientes_df['Razão Social do Tomador'].fillna('Desconhecido', inplace=True)

# Converter as colunas de valores para o formato de moeda brasileira
clientes_df['Valor Mensal'] = clientes_df['Valor Mensal'].apply(lambda x: f"R$ {x:,.2f}")
clientes_df['Valor'] = clientes_df['Valor'].apply(lambda x: f"R$ {x:,.2f}")
clientes_df['Faturar Após Medição'] = clientes_df['Faturar Após Medição'].apply(lambda x: f"R$ {x:,.2f}")

# Configurar o título do dashboard
st.title('Dashboard de Faturamento')

# Filtros
st.sidebar.header('Filtros')

# Filtro por Prestador
prestador = st.sidebar.multiselect(
    'Nome Prestador',
    options=sorted(clientes_df['Nome Prestador'].unique()),
    default=sorted(clientes_df['Nome Prestador'].unique())
)

# Filtro por Status Mediçao
medicao = st.sidebar.multiselect(
    'Status Mediçao',
    options=sorted(clientes_df['Status Mediçao'].unique()),
    default=sorted(clientes_df['Status Mediçao'].unique())
)

# Filtro por Período
periodo = st.sidebar.multiselect(
    'Período',
    options=sorted(clientes_df['Período'].unique()),
    default=sorted(clientes_df['Período'].unique())
)

# Filtro por Status Faturamento
status_faturamento = st.sidebar.multiselect(
    'Status Faturamento',
    options=sorted(clientes_df['Status Faturamento'].unique()),
    default=sorted(clientes_df['Status Faturamento'].unique())
)

# Filtro por Objeto
objeto = st.sidebar.multiselect(
    'Objeto',
    options=sorted(clientes_df['Objeto'].unique()),
    default=sorted(clientes_df['Objeto'].unique())
)

# Filtro por Tomador
tomador = st.sidebar.multiselect(
    'Tomador',
    options=sorted(clientes_df['Razão Social do Tomador'].unique()),
    default=sorted(clientes_df['Razão Social do Tomador'].unique())
)

# Filtrar os dados com base nos filtros selecionados
filtered_data = clientes_df[
    (clientes_df['Razão Social do Tomador'].isin(tomador)) &
    (clientes_df['Nome Prestador'].isin(prestador)) &
    (clientes_df['Status Mediçao'].isin(medicao)) &
    (clientes_df['Status Faturamento'].isin(status_faturamento)) &
    (clientes_df['Período'].isin(periodo)) &
    (clientes_df['Objeto'].isin(objeto))
]

# Exibir os dados filtrados
st.subheader('Dados Filtrados')
st.dataframe(filtered_data)

# Gráfico de pizza: Contagem de registros por Prestador
fig_pizza_prestador = px.pie(filtered_data, names='Nome Prestador')

# Gráfico de barras: Valor total por Prestador (convertendo valores de volta para números)
valor_por_prestador = filtered_data.copy()
valor_por_prestador['Valor'] = valor_por_prestador['Valor'].replace('[R$,]', '', regex=True).astype(float)
valor_por_prestador = valor_por_prestador.groupby('Nome Prestador')['Valor'].sum().reset_index()
fig_valor_por_prestador = px.bar(valor_por_prestador, x='Valor', y='Nome Prestador', orientation='h')

# Gráfico de pizza: Valor por Medição
fig_pizza_valor_por_medicao = px.pie(filtered_data, names='Status Mediçao')

# Gráfico de pizza: Valor por Faturamento
fig_pizza_valor_por_faturamento = px.pie(filtered_data, names='Status Faturamento')

# Display the two main plots side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader('Distribuição por Prestador')
    st.plotly_chart(fig_pizza_prestador)

with col2:
    st.subheader('Distribuição por Medição')
    st.plotly_chart(fig_pizza_valor_por_medicao)

# Display the additional plots below
col3, col4 = st.columns(2)

with col3:
    st.subheader('Valor Total por Prestador')
    st.plotly_chart(fig_valor_por_prestador)

with col4:
    st.subheader('Distribuição por Faturamento')
    st.plotly_chart(fig_pizza_valor_por_faturamento)
