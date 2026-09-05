# Guia Visual da Entrega, Fase 3

**Origem:** padrão visual do material executivo da Fase 2, que recebeu nota 10. Nada do conteúdo da Fase 2 é aproveitado, apenas o sistema visual.
**Método de extração:** leitura da apresentação no Drive e recuperação dos valores exatos de cor no notebook público da Fase 2.
**Versão:** v2.0, de 05/09/2026. Substitui a v1.0, que previa cor de destaque em terracota.

## 1. Paleta final

Decisão da Ana em 05/09/2026: manter todo o sistema visual da Fase 2 e trabalhar em **rampa monocromática azul**, sem cor de destaque contrastante. A justificativa é semântica: os três passos de cor codificam a edição da pesquisa, que é uma variável ordinal, e uma rampa sequencial representa ordem melhor do que cores categóricas.

| Papel | Cor | Uso |
|-------|-----|-----|
| Azul escuro | `#1B3A5C` | Edição mais recente, série ou categoria em foco, títulos de bloco de leitura |
| Azul médio | `#4E8098` | Edição intermediária, kickers de seção, réguas |
| Azul claro | `#8FBCD4` | Edição mais antiga, barras de contexto, texto de apoio sobre fundo escuro |
| Cinza de contexto | `#C9D3D9` | Bordas de cartão, quarta série quando existir |
| Fundo escuro | `#132B44` | Capa e slide de encerramento |
| Texto principal | `#1A1A1A` | Títulos e corpo em fundo claro |
| Texto de apoio | `#6E6E6E` | Legendas, fonte dos dados, texto secundário |
| Fundo claro | `#FFFFFF` | Slides de conteúdo |

### Validação por medição

| Critério | Exigido | Medido |
|----------|---------|--------|
| Luminosidade estritamente decrescente na rampa | Sim | 177, 116 e 53 em escala de cinza |
| Distância em escala de cinza entre passos adjacentes | 25 níveis ou mais | 61 e 63 |
| Contraste do azul escuro sobre fundo branco | 4,5 ou mais | 11,63 |
| Contraste do azul médio sobre fundo branco | 4,5 ou mais | 4,32 |
| Contraste do branco sobre o fundo escuro da capa | 4,5 ou mais | 14,42 |
| Contraste do azul claro sobre o fundo escuro da capa | 4,5 ou mais | 7,08 |

A rampa é distinguível em impressão em preto e branco, como exige o padrão do projeto, e mantém separação suficiente sob deficiência de visão de cores dos tipos protan e tritan, já que a diferenciação se apoia em luminosidade e não em matiz.

**Restrição registrada:** o azul claro `#8FBCD4` tem contraste 2,04 sobre fundo branco, abaixo do mínimo de 3,0. Ele é usado apenas em áreas grandes, como preenchimento de barra, nunca em linha fina, texto ou marcador pequeno, e todo gráfico traz rótulo de valor visível, o que torna a leitura independente da cor. O cinza de contexto `#C9D3D9` segue a mesma restrição.

## 2. Anatomia do slide de conteúdo

1. Kicker em caixa alta, corpo 11, cor azul médio, nomeando a seção, por exemplo ESTRUTURA DO MERCADO.
2. Título afirmativo, corpo 28, que declara a conclusão em vez de nomear o assunto. Exemplo desta fase: "A faixa mediana do Sênior subiu 40% e as de entrada não se moveram".
3. Área de conteúdo, com gráfico à esquerda, em dimensão fixa de 8,64 por 4,8 polegadas, e leitura interpretativa à direita, em dois ou três blocos curtos com subtítulo em negrito.
4. Rodapé com a fonte dos dados, em corpo 9 e cor de apoio, e número da página à direita, coincidindo com a página do PDF.

Outros elementos do sistema: cartões arredondados com fundo `#F5F8FA` e borda no cinza de contexto para blocos comparativos, e faixa de números grandes em azul escuro para indicadores.

## 3. Tipografia

Calibri no material executivo, DejaVu Sans nos gráficos, ambas sem serifa humanista. Títulos em peso regular e corpo grande, texto em peso regular. Hierarquia estável em todos os slides, sem mistura de famílias dentro de um mesmo elemento.

## 4. Regras dos gráficos

- Todo gráfico é gerado em duas versões pelo mesmo código: a **versão completa**, em `figuras/`, com título, subtítulo, rótulos de eixo, unidade e fonte dos dados, usada na documentação e no notebook; e a **versão de slide**, em `figuras/deck/`, sem título, subtítulo e fonte, porque esses elementos pertencem ao slide e duplicá-los polui a leitura.
- Cor com função semântica, nunca decorativa: a rampa codifica a edição, e o azul escuro marca a categoria em foco nos gráficos de edição única.
- Escala honesta, eixo iniciando em zero.
- Rótulo de valor visível em todas as séries, sempre no padrão numérico brasileiro, com arredondamento meio para cima.
- Resolução de 200 pontos por polegada, sem imagem esticada ou cortada.
- Uma conclusão escrita para cada gráfico, no próprio slide.
- Gráfico de edição única cita apenas aquela edição na linha de fonte, nunca as três.
