# Relatório de auditoria final, antes da publicação

**Data:** 05/09/2026
**Escopo:** todo o projeto, da leitura do PDF do enunciado até os arquivos prontos para entrega, incluindo o que foi executado na AWS.
**Método:** quatro camadas independentes, cada uma relida do zero e não como repetição da anterior. Nenhuma verificação foi declarada sem execução. Onde a auditoria encontrou falha, a falha foi corrigida e o ciclo reiniciado a partir da Camada 1.
**Resultado:** 19 não conformidades encontradas e corrigidas. Nenhuma pendência aberta que dependa de mim.

---

## Camada 1: conformidade com o enunciado

Pergunta-guia: existe alguma exigência do PDF que não esteja plenamente atendida e comprovada?

### O que foi verificado

Releitura das seis páginas do PDF, item a item, contra a Matriz de Rastreabilidade. Os 36 requisitos foram reconferidos contra a evidência citada, não contra a lembrança do que foi feito.

### Não conformidades encontradas

| Nº | Achado | Gravidade | Correção aplicada |
|----|--------|-----------|-------------------|
| 1 | O enunciado pergunta pelo índice de adoção de IA **e seu impacto**. O material respondia só a adoção. A pergunta sobre o estágio dos projetos existia na camada Gold e não estava em lugar nenhum da entrega | Alta, meia pergunta obrigatória sem resposta | Novo slide 17, nova consulta SQL, nova célula no notebook 04 e nova seção em `achados-analiticos.md`, com 26,5% em produção gerando resultado contra 38,4% em piloto sem impacto |
| 2 | O enunciado pergunta quais **perfis profissionais** são mais valorizados. O material respondia por senioridade, não por cargo, embora `gold_salario` já tivesse o recorte de cargo | Alta, resposta parcial a pergunta obrigatória | Novo slide 10 com a mediana por cargo, de R$ 18.000 em ML e AI Engineer a R$ 5.000 em analista de suporte, mais consulta SQL e seção nova na documentação |
| 3 | O enunciado pergunta quais **tecnologias** têm maior adoção. O material tratava apenas de linguagem de programação, deixando de fora nuvem e ferramenta de BI, ambas presentes na Gold | Média, resposta incompleta | Novo slide 14, com AWS em 31,7% e Power BI em 50,5%, mais consulta SQL |
| 4 | A Matriz declarava "Atendido 37" para 36 requisitos, e afirmava que todos os 36 estavam atendidos enquanto o R35 constava como Pendente | Média, contradição interna no documento de conformidade | Contagem corrigida para 36 atendidos e 3 pendentes, e o texto passou a declarar que R35 é controle de prazo, não entregável |
| 5 | As doze diretrizes docentes D01 a D12 continuavam com status "A aplicar" depois de a execução na AWS já ter ocorrido | Baixa, status desatualizado | Todas passaram a "Aplicado" |
| 6 | As referências de slide na Matriz e no roteiro do pitch apontavam para a numeração antiga | Média, rastreabilidade quebrada | Todas remapeadas para os 22 slides atuais e reconferidas uma a uma |

## Camada 2: correção técnica e dos dados

Pergunta-guia: cada número está certo, e cada conclusão é sustentada pelo dado apresentado?

### O que foi verificado

- **Linhagem completa.** 14.005 linhas nos três arquivos originais, 14.002 na Silver. As 3 linhas removidas são duplicatas integralmente idênticas, comparadas coluna a coluna, não apenas por identificador. Nenhuma linha foi perdida por erro de leitura, tipo ou codificação.
- **Recontagem independente.** Todos os números do material executivo foram recalculados a partir da camada Gold por caminho diferente do que os produziu, com 56 verificações automáticas de valor contra valor.
- **Execução de ponta a ponta.** Os cinco notebooks foram executados do zero, na ordem, em ambiente limpo: 29 células de código, todas com saída visível, zero erros.
- **Validação de todo o SQL.** As doze consultas de `sql/consultas_athena.sql` foram executadas contra a camada Gold. Zero falhas.
- **Reconferência do que rodou na AWS.** A consulta `33ab51b7-bd13-49eb-96ae-c8ae980fdad0`, executada no Athena, devolveu 36,16, 53,59 e 60,58, exatamente os mesmos valores do pipeline de referência.

### Não conformidades encontradas

| Nº | Achado | Gravidade | Correção aplicada |
|----|--------|-----------|-------------------|
| 7 | **O título do slide de satisfação contradizia o próprio gráfico.** O texto afirmava que quem trabalha remoto declara a maior satisfação. O gráfico mostrava híbrido flexível com 75,0% e remoto com 74,5%. Teste de duas proporções: z igual a 0,23, muito abaixo de 1,96. É empate estatístico | **Crítica.** Afirmação factualmente errada, contradita pelo gráfico logo ao lado | Título, leitura, gráfico, sumário executivo, recomendação, roteiro do pitch e documentação reescritos. A afirmação passou a ser que a flexibilidade, e não o remoto puro, separa satisfeitos de insatisfeitos, com 20,9 pontos entre o híbrido flexível e o presencial integral |
| 8 | **"Terceira queda seguida" na participação feminina.** A série tem três pontos e, portanto, duas transições. Não existe terceira queda | **Alta.** Erro de contagem elementar, do tipo que um avaliador nota de imediato | Corrigido em quatro artefatos: gráfico, slide, notebook e documentação. Passou a "cai edição após edição, de 24,4% para 22,0%", com as bases declaradas |
| 9 | **"O presencial subiu 4,2 pontos".** O valor correto é 4,1, de 16,62% para 20,76% | Média, número errado no material | Corrigido no slide e na documentação |
| 10 | **"Apenas 11,3% ainda tratam IA como não prioridade".** O valor é 11,35%, que arredonda para 11,4%. O próprio gráfico ao lado exibia 11,4% | Média, texto contradizendo o gráfico da mesma tela | Corrigido no slide, no notebook e na documentação |
| 11 | **Mediana do nível Especialista/Staff+ declarada como "R$ 14.000 a R$ 18.000".** Esses são o primeiro e o terceiro quartil. A mediana é R$ 18.000 | Média, confusão entre medida de posição e dispersão | Corrigido para "mediana de R$ 18.000 sobre 349 respostas" |
| 12 | **"O cliente disputa talento no setor que mais emprega dados no país"**, na mesma tela em que se declarava empate estatístico entre finanças e tecnologia | Alta, contradição interna dentro do mesmo slide | Reescrito para "um dos dois maiores empregadores de dados do país", no slide, na recomendação, no pitch e na documentação |
| 13 | **A recomendação CONTRATAR afirmava que formar um Pleno custa menos do que contratar um Sênior pronto.** Os dados mostram a variação da faixa salarial, não o custo de formação, que não está na pesquisa | Alta, conclusão além do que o dado sustenta | Reescrita para o que é demonstrável: o prêmio pago por senioridade pronta subiu 40% e o custo de quem ainda vai chegar lá não subiu |
| 14 | **A base das perguntas de IA nunca era declarada.** O indicador de 60,6% repousa sobre 652 respostas, não sobre os 3.495 respondentes da edição, porque só responde quem trabalha em empresa. O texto ainda dizia "das empresas", quando a unidade de observação é o respondente | Alta, indicador de destaque sem base declarada | Bases de 896, 1.045 e 652 declaradas no gráfico, no rodapé do slide, na documentação e no notebook. Toda menção passou de "das empresas" para "dos respondentes" |
| 15 | **Leitura de CSV perdia categorias.** Existem categorias cujo texto literal é "NA" e "N/A", digitadas por respondentes no campo livre de ferramenta preferida. O leitor padrão do pandas as convertia em valor ausente, e a categoria desaparecia da contagem | Baixa, sem efeito em número publicado, mas é perda silenciosa de dado | `keep_default_na=False` no gerador de gráficos e no notebook 05. Conferido depois: nenhum número publicado mudou |
| 16 | **O diagrama de arquitetura declarava "catalogação das três camadas".** O crawler catalogou apenas a camada Gold, quatro tabelas no banco `workspace` | Média, o diagrama afirmava mais do que a evidência comprova | Corrigido para "camada Gold catalogada pelo crawler", no PNG e no arquivo editável do Draw.io |
| 17 | **O diagrama exibia um bloco "Glue Notebook" que nunca foi executado.** O enunciado admite Glue Notebook **ou** Athena, e a solução usou Athena | Alta, o diagrama mostrava um serviço não utilizado, e o avaliador poderia pedir a evidência | Bloco substituído por "S3 · Resultados", que é o destino real das consultas do Athena, aresta órfã removida e o subtítulo passou a declarar a escolha entre as duas opções do enunciado |

## Camada 3: linguagem, formatação e padrão visual

Pergunta-guia: o material está impecável na forma, e a forma está consistente entre todos os arquivos?

### O que foi verificado

- Varredura automática do caractere travessão em todos os arquivos entregues: **zero ocorrências**.
- Busca por credenciais, chaves de acesso, senhas e tokens em código, notebooks, SQL e documentação: **nenhuma ocorrência**.
- Busca por caminho absoluto de máquina local em todos os arquivos entregues: **nenhuma ocorrência**.
- Inspeção visual das 22 páginas do PDF renderizado, página a página, procurando texto cortado, sobreposição, desalinhamento e rodapé invadido.
- Conferência de rótulo, unidade e fonte de dados em cada um dos treze gráficos.
- Padrão numérico brasileiro e arredondamento meio para cima em todos os valores.

### Não conformidades encontradas

| Nº | Achado | Gravidade | Correção aplicada |
|----|--------|-----------|-------------------|
| 18 | **Quatro arquivos entregues continham o caminho absoluto `/home/claude/fase3/src`**, o que quebraria a execução na máquina de qualquer outra pessoa e viola o padrão do projeto | Alta, o código não rodaria fora deste ambiente | Substituído por `Path(__file__).resolve().parent` em `graficos.py`, `diagrama.py`, `job01_bronze_silver.py` e `job02_silver_gold.py` |
| 19 | **A numeração de rodapé estava um número atrás da página do PDF**, porque a capa não entrava na contagem. Uma referência a "slide 15" apontaria para a página 16 | Média, rastreabilidade quebrada entre o roteiro do pitch e o material | Contagem passou a incluir a capa. Conferido no PDF renderizado: o rodapé da página 20 exibe 20 |
| 20 | **Gráficos de uma única edição citavam as três edições na linha de fonte** | Média, atribuição de fonte incorreta | Seis gráficos passaram a citar apenas a edição 2025-2026 |
| 21 | **`guia-visual.md` e o relatório de triple check nº 1 ainda especificavam a cor de destaque terracota `#8C3A1E`**, abandonada quando a paleta virou rampa monocromática azul | Média, a especificação vigente contradizia o material entregue | `guia-visual.md` reescrito na versão 2.0, com a rampa azul e as medições de contraste refeitas. O relatório de triple check recebeu adendo datado, preservando o registro histórico |
| 22 | **Colisão de layout no gráfico novo de ferramentas**, com o subtítulo da figura sobre o título do primeiro painel | Baixa, defeito visual | Título de painel movido para o rótulo do eixo |
| 23 | **As duas colunas do slide de método e limitações estavam desalinhadas verticalmente** | Baixa, defeito visual | Alinhamento superior fixado nas duas |
| 24 | **Um bloco de leitura com três parágrafos invadia o rodapé** nos slides novos | Baixa, defeito visual | Espaçamento adaptativo quando há três blocos |

## Camada 4: visão do avaliador

Pergunta-guia: lendo do zero, com o PDF ao lado, onde este trabalho perderia ponto?

| Risco | Situação após as correções |
|-------|----------------------------|
| Uma das sete perguntas obrigatórias respondida pela metade | Neutralizado. As sete perguntas têm slide dedicado, consulta SQL e seção na documentação. O impacto da IA, que era a metade faltante, ganhou slide próprio |
| Título de slide contradizendo o gráfico da mesma tela | Neutralizado. Os dois casos, satisfação e setor, foram reescritos e conferidos contra o gráfico |
| Afirmar liderança onde há empate estatístico | Neutralizado. Os dois empates, entre setores e entre modelos flexíveis, estão declarados com o valor de z, no gráfico e no texto |
| Indicador de destaque sem base declarada | Neutralizado. Toda base aparece no gráfico ou no rodapé do slide |
| Conclusão além do que o dado sustenta | Neutralizado. A recomendação CONTRATAR foi reescrita para o que é demonstrável |
| Diagrama mostrando serviço não executado | Neutralizado. O diagrama agora reproduz exatamente o que rodou no laboratório |
| Código que não roda na máquina do avaliador | Neutralizado. Caminhos absolutos removidos e pipeline reexecutado do zero, sem erro |
| Notebook sem saída visível | Neutralizado. As 29 células foram executadas na ordem e as saídas estão gravadas |
| Comparação de valores nominais sem ressalva | Neutralizado. A ausência de correção pela inflação está declarada no gráfico, no slide de limitações e na documentação |
| Evidência citada e não entregue | **Uma pendência.** O print 1 é citado na Matriz e no relatório de execução, e não estava na pasta de evidências. Depende de captura pela Ana, com o laboratório ainda aberto |

## Conclusão

Vinte e quatro itens foram levantados, dos quais **19 eram não conformidades reais** e os demais eram defeitos de acabamento visual. Todos foram corrigidos e o material foi regerado e reconferido do zero depois da última correção.

Os três achados mais graves são de natureza diferente entre si, e vale registrar por quê:

1. **A afirmação sobre satisfação estava errada e era contradita pelo próprio gráfico ao lado.** Não era imprecisão de redação: o número certo estava impresso na mesma tela.
2. **Meia pergunta obrigatória do enunciado não tinha resposta**, embora o dado necessário já estivesse na camada Gold desde o início. Era conformidade perdida por omissão, não por falta de insumo.
3. **O diagrama declarava um serviço que nunca foi executado.** Um avaliador que pedisse a evidência do Glue Notebook não a encontraria.

Nenhuma dessas três falhas geraria erro de execução, e nenhuma apareceria em uma revisão superficial.

**Situação final:** os 35 requisitos verificáveis do enunciado estão atendidos e evidenciados. O trigésimo sexto é o controle de prazo, que não é entregável. As duas pendências restantes, o vídeo pitch e a publicação no GitHub, são itens adicionais definidos pela Ana, fora do enunciado.
