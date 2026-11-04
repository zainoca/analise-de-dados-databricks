# Análise de Dados do Marketplace — Databricks

Projeto de Engenharia e Análise de Dados desenvolvido no Databricks, com foco na limpeza, organização, transformação e análise de dados de um marketplace. O projeto transforma dados brutos de produtos e vendedores em informações úteis para apoiar a tomada de decisão por meio de um dashboard executivo.

# Objetivo

Construir um pipeline de dados organizado em camadas e produzir indicadores estratégicos sobre o catálogo, os vendedores, as margens por categoria, a distribuição geográfica do estoque e a qualidade dos cadastros.

# Arquitetura

O projeto utiliza a arquitetura Medallion:

• Bronze: ingestão e armazenamento dos dados de origem.
• Silver: limpeza, padronização, organização e validação dos dados.
• Gold: preparação de dados analíticos para indicadores e visualizações.

# Tecnologias

• Databricks
• Python
• SQL
• PySpark
• Delta Lake
• Dashboard e visualização de dados

Remova da lista qualquer tecnologia que não tenha sido efetivamente utilizada.

# Dashboard Executivo

O dashboard reúne análises para responder a perguntas de negócio, como:

1. Quais vendedores concentram o nosso catálogo?
2. Qual a margem estimada por categoria?
3. Quanto temos em estoque, por estado?
4. Quanto do nosso cadastro é confiável? 

# Etapas do projeto

1. Ingestão das bases de produtos e vendedores.
2. Exploração inicial e identificação de inconsistências.
3. Limpeza, padronização e organização dos dados.
4. Construção das camadas de processamento.
5. Preparação dos dados analíticos.
6. Criação de indicadores e visualizações.
7. Análise dos resultados para apoiar decisões de negócio.

# Aprendizados

O desenvolvimento do projeto permitiu praticar conceitos de processamento e organização de dados, qualidade de dados, arquitetura Medallion e construção de análises orientadas a indicadores. Também reforçou a importância de manter a lógica de transformação organizada e rastreável ao longo do pipeline.

# Como visualizar

• Consulte o notebook pipeline_marketplace.ipynb para acompanhar o código e as etapas do processamento.
• Consulte os arquivos CSV para conhecer as bases utilizadas.
• Veja o dashboard no Databricks ou na imagem incluída no repositório, se disponível.

# Autoria

Projeto desenvolvido por Zaine Sousa Silveira como prática de Engenharia e Análise de Dados com Databricks.
