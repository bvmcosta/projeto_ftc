# 1) Problema de negócio

O problema apresentado pelo novo CEO da companhia Fome Zero é conhecer os principais indicadores da empresa. 
O modelo de negócio dessa empresa é o *marketplace*, conectando restaurantes e clientes através de aplicativo próprio distribuído gratuitamente pelas plataformas de aplicativo.
O problema apresentado pelo CEO pode ser resumido em três perguntas principais:

##### 1.1) Quais são os restaurantes cadastrados no aplicativo e em quais cidades/países estão localizados?
##### 1.2) Como varia o preço médio de prato para 2 pessoas entre os países e cidades?
##### 1.2) Quais são os tipos culinários dos restaurantes cadastrados e suas respectivas avaliações?

# 2) Premissas da Análise

##### 2.1) Cada restaurante tem um identificador (ID) único, atribuído no momento do cadastro no aplicativo. Logo, IDs duplicados devem ser removidos antes da análise do conjunto de dados.
##### 2.2) **Hipótese**: O preço médio de prato para 2 pessoas está diretamente relacionado com a classificação econômica (*lower middle income*, *upper middle income*, *high income*) dos países onde estão os restaurantes estão localizados.
##### 2.3) Os dados binários (0 e 1) nas colunas 'has_online_delivery' e 'has_table_booking' equivalem a Não e Sim, respectivamente.

# 3) Estratégia de Análise

##### 3.1) Converter os nomes das colunas para o formato snake_case, facilitando o acesso aos dados pelo nome das colunas.
##### 3.2) Remover valores iguais a zero e o valor de *outlier* muito elevado [US$ 15565010.58 (cidade de Adelaide - Austrália)] antes do cálculo da mediana dos preços.
##### 3.3) Converter o preço médio de prato para 2 pessoas para a moeda dólar dos Estados Unidos da América (USD) utilizando o fator de conversão disponibilizado pelo Banco Central do Brasil (https://www.bcb.gov.br/conversao).
##### 3.4) Agrupar os restaurantes por país, cidade e classificação econômica dos países para posterior contagem de IDs e cáculo das medianas dos preços médios de prato para 2 pessoas dos restaurantes.
##### 3.5) Construir gráficos para visualização dos resultados após agrupamentos.

# 4) *Insight* da Análise

##### 4.1) O desenvolvimento do serviço de reserva de mesa tem o potencial de aumentar a quantidade de vendas e o valor do preço médio de prato para 2 pessoas dos restaurantes.

# 5) Produto final

O produto final deste projeto de análise está hospedado na *Cloud* do Streamlit e pode ser acessado pelo link
https://bvmcosta-ftc.streamlit.app/.
  
# 6) Conclusão

A empresa Fome Zero está bem distribuída entre diferentes países, porém ainda há potencial grande para cadastro de novos restaurantes em mais cidades de cada país. 

# 7) Perspectiva

Avaliar para cada tipo culinário dos restaurantes, o impacto dos fatores 'has_online_delivery' e 'has_table_booking' sobre o preço médio de prato para 2 pessoas. 



