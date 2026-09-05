# Relatório de Triple Check nº 1: recebimento das bases e definição visual

**Data:** 05/09/2026
**Escopo auditado:** os três arquivos recebidos, o mapa de equivalência entre edições e a paleta proposta para o material executivo.
**Método:** cada afirmação foi reverificada por caminho independente do que a produziu. Nenhuma verificação foi declarada sem execução.

## Camada 1: conformidade com o enunciado

| Item | Verificação | Resultado |
|------|-------------|-----------|
| R01, três últimas pesquisas | Nova consulta ao catálogo oficial do Kaggle, com ordenação por data de atualização | Confirmado. As três mais recentes são 2025-2026, de 09/07/2026, 2024-2025, de 09/05/2025, e 2023-2024, de 20/06/2024. São exatamente as três recebidas |
| R04, origem dos dados | Conferência de nome de arquivo e volumetria contra o dataset de origem | Confirmado, um arquivo por edição, nenhum repetido |
| R34, sem dashboard | Decisão registrada de gerar gráficos em Python | Sem pendência |

## Camada 2: correção técnica

| Item | Verificação independente | Resultado |
|------|--------------------------|-----------|
| Volumetria | Releitura completa com pandas, motor diferente do usado na primeira contagem | Aprovado. 5.293 por 399, 5.217 por 403 e 3.495 por 388, idêntico à primeira medição |
| Codificação | Leitura integral em UTF-8 estrito, do primeiro ao último byte | Aprovado nos três arquivos |
| Duplicatas | Comparação de linha inteira, não apenas do identificador | Confirmado e qualificado: as 2 ocorrências de 2024-2025 e a 1 de 2025-2026 são linhas integralmente idênticas, portanto duplicação real de registro, removível com segurança |
| Modelo de trabalho comparável | Extração das categorias observadas nas três edições e comparação de conjuntos | Aprovado. As quatro categorias são idênticas nas três edições, o que valida a série histórica |
| Armadilha do código `2.q` | Leitura dos valores reais da coluna em cada edição | Confirmada. Em 2023-2024 e 2024-2025 a coluna trata de layoffs. Em 2025-2026 trata de modelo de trabalho |
| Contagens do mapa de equivalência | Recontagem com implementação independente, sem expressão regular de captura | **Reprovado na primeira medição.** Ver correção abaixo |

### Erro encontrado e corrigido

A recontagem divergiu da primeira medição em uma unidade, e a investigação da diferença revelou um erro maior do que o número sugeria: existe um terceiro padrão de nomenclatura de coluna, com espaço no lugar do sublinhado, por exemplo `3.f.1 Colaboradores usando AI generativa`. O leitor original cortava o código em `3.f` e agrupava oito colunas distintas sob o mesmo identificador. O bloco afetado é justamente o de inteligência artificial generativa, que responde a uma das sete perguntas obrigatórias do enunciado. Havia ainda um cabeçalho malformado em 2023-2024, descartado silenciosamente.

Leitor reescrito e reexecutado. Prova objetiva de correção: o número de códigos únicos extraídos passou a ser exatamente igual ao número de colunas de cada arquivo, 399, 403 e 388, e nenhuma coluna ficou sem reconhecimento.

Números corrigidos, que substituem os informados antes:

| Medida | Valor informado antes | Valor correto |
|--------|-----------------------|---------------|
| Códigos presentes nas três edições | 316 | 330 |
| Desses, com pergunta diferente em alguma edição | 139 | 145 |
| Perguntas presentes nas três edições | 215 | 237 |
| Dessas, que trocaram de código | 78 | 92 |

O mapa de equivalência foi regravado com o leitor corrigido.

## Camada 3: linguagem, formatação e padrão visual

| Item | Verificação | Resultado |
|------|-------------|-----------|
| Ausência de travessão nos documentos | Contagem automática do caractere em todos os arquivos entregues | Aprovado, zero ocorrências |
| Paleta, contraste sobre fundo branco | Cálculo da razão de contraste pela fórmula de luminância relativa | Primária 4,32 e destaque 7,67, aprovadas. Secundária 2,04, restrita a áreas grandes, regra registrada |
| Paleta, legibilidade em preto e branco | Conversão para escala de cinza e medição da distância entre as três cores de série | **Reprovado na primeira proposta.** Ver correção abaixo |

### Erro encontrado e corrigido

A cor de destaque proposta, `#C1642F`, resulta em nível de cinza 122, contra 116 do azul primário. Distância de 6 níveis, indistinguível em impressão monocromática, o que viola o padrão de qualidade do projeto. A cor foi substituída por `#8C3A1E`, terracota escuro, com distância de 37 níveis da primária e 98 da secundária, e contraste de 7,67 sobre fundo branco.

## Camada 4: visão do avaliador

Pergunta-guia: onde este material perderia ponto neste estágio?

| Risco | Situação |
|-------|----------|
| Comparar edições por código de pergunta | Neutralizado. Regra de tripla confirmação estabelecida e documentada |
| Apresentar queda de senioridade que não existe | Neutralizado. A categoria nova de 2025-2026 será exibida com as duas leituras |
| Comparar volumes absolutos entre edições de tamanhos diferentes | Neutralizado. Toda comparação entre anos em base percentual |
| Tratar os dados antes da camada Bronze | Neutralizado. Arquivos verificados como crus e fiéis à origem |
| Gráfico ilegível em impressão | Neutralizado após a correção da paleta |

## Conclusão

Duas falhas reais foram encontradas e corrigidas nesta rodada, uma no leitor de cabeçalhos e uma na cor de destaque. Ambas passariam despercebidas na execução, porque nenhuma delas gera erro visível. As bases estão aprovadas para ingestão na camada Bronze e o padrão visual está fechado e validado por medição.

---

## Adendo de 05/09/2026: decisão posterior sobre a cor de destaque

Depois desta rodada, a Ana optou por abandonar a cor de destaque contrastante e trabalhar em rampa monocromática azul, com `#1B3A5C`, `#4E8098` e `#8FBCD4`, mais `#C9D3D9` como cinza de contexto. O terracota `#8C3A1E` aprovado acima **não foi utilizado no material entregue**.

A rampa final foi submetida às mesmas medições e aprovada: luminosidade estritamente decrescente, 177, 116 e 53 em escala de cinza, com distâncias de 61 e 63 níveis entre passos adjacentes, contra o mínimo de 25 exigido pelo padrão do projeto. A especificação vigente é a de `docs/guia-visual.md`, versão 2.0. Este relatório permanece como registro datado da rodada em que a falha do terracota original foi encontrada.
