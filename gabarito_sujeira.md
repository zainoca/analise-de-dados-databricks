# Gabarito do instrutor — sujeira proposital nas bases

Arquivos: `vendedores.csv` (2.067 linhas) e `produtos.csv` (2.081 linhas), UTF-8, separador vírgula.
Chave de relação: `produtos.seller_id` → `vendedores.seller_id`. Há 2.000 vendedores e 2.000 produtos reais; o resto é duplicata ou lixo.

## vendedores.csv

| Coluna | Problema | Tratamento na Silver |
|---|---|---|
| seller_id | `vnd-00042`, ` VND-00042 `, `VND00042`; 1 linha vazia e 1 "Loja Teste" sem ID | `upper(trim())` e recolocar o hífen; descartar sem ID |
| (linha inteira) | 25 duplicatas exatas + 40 versões antigas do mesmo vendedor | `row_number()` por seller_id ordenando `updated_at desc`, ficar com 1 |
| nome_fantasia | MAIÚSCULAS, minúsculas, espaços nas pontas | `trim` + `initcap` |
| cnpj | com e sem máscara, máscara parcial, dígito verificador errado, vazio | só dígitos; validar 14 dígitos (bônus: validar DV) |
| email | sem `@`, vazio, MAIÚSCULO | `lower`; flag `email_valido` |
| telefone | 5 formatos diferentes, vazio | só dígitos, remover `55` inicial |
| cidade | sem acento, MAIÚSCULA, espaço, vazio | `trim` + `initcap` (acento perdido não volta: bom gancho de discussão) |
| uf | minúscula, nome por extenso (`São Paulo`, `Distrito Federal`), vazio | `upper` + tabela de-para nome → sigla |
| categoria_principal | variações (`eletronicos`, `Casa & Cozinha`, `Vestuário`, `Pets`...) | tabela de-para para as 7 categorias canônicas |
| data_cadastro | `yyyy-MM-dd`, `dd/MM/yyyy`, `yyyy/MM/dd`, `dd-MM-yyyy` | `coalesce(try_to_date(x, fmt1), try_to_date(x, fmt2), ...)` |
| status | `ativo`, `ATIVO`, `Ativo `, `A`/`I`/`S`, vazio | normalizar para ativo / inativo / suspenso |
| avaliacao_media | vírgula decimal, vazio, `6.2`, `-1`, `N/A` | trocar vírgula, `try_cast`, aceitar só 0–5 |

## produtos.csv

| Coluna | Problema | Tratamento na Silver |
|---|---|---|
| product_id | mesmas sujeiras do seller_id; 1 linha vazia | igual ao seller_id |
| (linha inteira) | 30 duplicatas exatas + 50 versões antigas (com preço diferente) | dedup por `updated_at desc` |
| seller_id | ~3% apontam para vendedores inexistentes (`VND-020xx`), ~2% vazios | após padronizar, `left anti join` com vendedores → tabela de quarentena |
| nome_produto | MAIÚSCULO, sem acento, espaços, vazio | `trim` + `initcap` |
| categoria | variações + vazio | mesmo de-para dos vendedores |
| marca | MAIÚSCULA, vazia | `initcap`; vazio → `Sem marca` |
| preco | `1234.56`, `1234,56`, `R$ 1.234,56`, `R$1234.56`, negativo, vazio | remover `R$`, tratar milhar/decimal, `try_cast`; negativo ou nulo → rejeitado |
| custo | vírgula decimal, vazio, **custo maior que o preço** | `try_cast`; flag `custo_suspeito` (fica fora da margem) |
| estoque | vazio, negativo, `N/A`, `sem estoque`, `12.0` | `try_cast` para double → int; negativo → nulo |
| peso | `1.5`, `1,5`, `1500g`, `1.5 kg`, vazio | converter tudo para `peso_kg` (g ÷ 1000) |
| ativo | `true/S/1/Sim/TRUE` e `false/N/0/Não/FALSE` | mapear para boolean |
| data_cadastro | 4 formatos + ~2% datas em 2027 (futuro) | parse multi-formato; data futura → nulo + flag |

## Correlações que aparecem na Gold
- ~80% dos produtos são da categoria principal do vendedor.
- Distribuição de cauda longa: poucos vendedores têm muitos produtos e a maioria tem 0 ou 1 (pergunta 01 da diretoria).
- Vendedores `suspenso` quase não têm produtos; produtos de vendedor não ativo vêm quase sempre com `ativo = false`.
- Faixas de preço por categoria (Livros e Pet baratos, Eletrônicos e Esporte caros), o que dá margem e valor em estoque diferentes por categoria.
- UF ponderada: SP concentra ~30% dos vendedores (pergunta 03).

## Quatro perguntas da diretoria (do vídeo) → tabelas Gold
1. Concentração: `% de produtos ativos dos 10 maiores vendedores`.
2. Margem: `avg((preco - custo) / preco)` por categoria, sem `custo_suspeito`.
3. Estoque: `sum(preco * estoque)` por UF do vendedor.
4. Confiabilidade: linhas aprovadas na Silver ÷ linhas da Bronze, por tabela e por motivo de rejeição.
