/**
 * Material executivo do Tech Challenge Fase 3.
 * Gera entregaveis/TechChallenge_Fase3_MaterialExecutivo.pptx
 */
const pptxgen = require("pptxgenjs");
const path = require("path");

const AZUL_ESCURO = "1B3A5C";
const AZUL_MEDIO = "4E8098";
const AZUL_CLARO = "8FBCD4";
const CINZA = "C9D3D9";
const TINTA = "1A1A1A";
const APOIO = "6E6E6E";
const FUNDO_ESCURO = "132B44";

const F = "Calibri";
const FIG = (n) => path.resolve(__dirname, "..", "figuras", n);
// os graficos do deck nao trazem titulo, subtitulo nem fonte: esses elementos
// sao do slide, e duplicalos dentro da imagem polui a leitura
const FIG_DECK = (n) => path.resolve(__dirname, "..", "figuras", "deck", n);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";           // 13.3 x 7.5 polegadas
pres.author = "Ana Paula Correa Galdino";
pres.title = "Tech Challenge Fase 3, o mercado brasileiro de dados";

// a capa conta como pagina 1, ainda que nao exiba rodape, para que o numero
// impresso coincida com a pagina do PDF
let numero = 1;

function rodape(slide, fonte) {
  numero += 1;
  slide.addText(fonte || "Fonte: State of Data Brazil, Data Hackers e Bain, edições 2023-2024, 2024-2025 e 2025-2026.",
    { x: 0.55, y: 6.95, w: 10.6, h: 0.3, fontSize: 9, color: APOIO, fontFace: F, isTextBox: true, margin: 0 });
  slide.addText(String(numero),
    { x: 12.3, y: 6.95, w: 0.5, h: 0.3, fontSize: 9, color: APOIO, fontFace: F, align: "right", isTextBox: true, margin: 0 });
}

/** Slide padrao de conteudo: kicker, titulo afirmativo e area livre abaixo. */
function slideConteudo(kicker, titulo) {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText(kicker.toUpperCase(),
    { x: 0.55, y: 0.42, w: 11, h: 0.28, fontSize: 11, color: AZUL_MEDIO, fontFace: F, charSpacing: 1.4, isTextBox: true, margin: 0 });
  s.addText(titulo,
    { x: 0.55, y: 0.72, w: 12.2, h: 0.72, fontSize: 28, color: TINTA, fontFace: F, isTextBox: true, margin: 0, valign: "top" });
  return s;
}

/** Slide de grafico com leitura interpretativa a direita. */
function slideGrafico(kicker, titulo, imagem, leitura, fonte) {
  const s = slideConteudo(kicker, titulo);
  // largura e altura fixas, iguais em todos os slides de grafico, para manter o alinhamento
  s.addImage({ path: FIG_DECK(imagem), x: 0.5, y: 1.62, w: 8.64, h: 4.8 });
  // com tres blocos o passo precisa encurtar, senao o ultimo texto invade o rodape
  const tres = leitura.length >= 3;
  const passo = tres ? 1.58 : 1.75;
  const alturaTexto = tres ? 1.18 : 1.5;
  const corpo = tres ? 11.5 : 12;
  let y = tres ? 1.75 : 1.9;
  leitura.forEach((bloco) => {
    s.addText(bloco.titulo, { x: 9.35, y, w: 3.45, h: 0.34, fontSize: 14, bold: true, color: AZUL_ESCURO, fontFace: F, isTextBox: true, margin: 0 });
    s.addText(bloco.texto, { x: 9.35, y: y + 0.36, w: 3.45, h: alturaTexto, fontSize: corpo, color: APOIO, fontFace: F, isTextBox: true, margin: 0, valign: "top" });
    y += passo;
  });
  rodape(s, fonte);
  return s;
}

// =====================================================================
// 1. Capa
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: FUNDO_ESCURO };
  s.addText("O mercado brasileiro de dados,\nem três edições da mesma pesquisa",
    { x: 0.9, y: 2.15, w: 11.4, h: 1.9, fontSize: 40, color: "FFFFFF", fontFace: F, isTextBox: true, margin: 0, lineSpacing: 46 });
  s.addText("Tech Challenge Fase 3  ·  Engenharia de Dados e Analytics em ambiente AWS",
    { x: 0.9, y: 4.25, w: 11.4, h: 0.4, fontSize: 16, color: AZUL_CLARO, fontFace: F, isTextBox: true, margin: 0 });
  s.addText("Ana Paula Corrêa Galdino  ·  RM370461",
    { x: 0.9, y: 5.6, w: 6, h: 0.3, fontSize: 13, color: "FFFFFF", fontFace: F, isTextBox: true, margin: 0 });
  s.addText("POSTECH, Data Analytics (DTAT)",
    { x: 0.9, y: 5.95, w: 6, h: 0.3, fontSize: 11, color: "FFFFFF", fontFace: F, isTextBox: true, margin: 0 });
  s.addText("Setembro de 2026",
    { x: 8.5, y: 5.95, w: 3.8, h: 0.3, fontSize: 11, color: "FFFFFF", fontFace: F, align: "right", isTextBox: true, margin: 0 });
  s.addNotes("Abertura. Apresentar o objetivo em uma frase: entender o mercado brasileiro de dados para orientar contratação, capacitação e investimento.");
}

// =====================================================================
// 2. Sumario executivo
// =====================================================================
{
  const s = slideConteudo("Sumário executivo", "A IA virou prioridade, o talento sênior encareceu e a diversidade regrediu");
  const itens = [
    { n: "60,6%", t: "dos respondentes dizem que a empresa prioriza IA generativa", d: "Eram 36,2% duas edições atrás. Só 26,5% declaram projetos em produção gerando resultado." },
    { n: "+40%", t: "na faixa salarial mediana do profissional Sênior", d: "Júnior e Pleno ficaram parados nas três edições. Contratar pronto encareceu, formar não." },
    { n: "22,0%", t: "de participação feminina, em queda nas duas transições da série", d: "Eram 24,4% na primeira edição. A direção é a mesma nas três, não é oscilação de amostra." },
    { n: "39,7%", t: "em trabalho totalmente remoto, contra 46,3% antes", d: "Os dois modelos flexíveis pagam R$ 14.000 de mediana, contra R$ 7.000 no presencial integral." },
  ];
  let y = 1.85;
  itens.forEach((i) => {
    s.addText(i.n, { x: 0.55, y, w: 1.85, h: 0.62, fontSize: 30, bold: true, color: AZUL_ESCURO, fontFace: F, isTextBox: true, margin: 0 });
    s.addText(i.t, { x: 2.55, y: y + 0.02, w: 10.2, h: 0.34, fontSize: 16, bold: true, color: TINTA, fontFace: F, isTextBox: true, margin: 0 });
    s.addText(i.d, { x: 2.55, y: y + 0.38, w: 10.2, h: 0.62, fontSize: 13, color: APOIO, fontFace: F, isTextBox: true, margin: 0 });
    y += 1.32;
  });
  rodape(s);
  s.addNotes("Quatro mensagens que sustentam todo o material. Cada uma vira uma decisão na última seção.");
}

// =====================================================================
// 3. Contexto
// =====================================================================
{
  const s = slideConteudo("Contexto", "A decisão do cliente depende de evidência que ele não tem");
  const cards = [
    { r: "SITUAÇÃO", t: "Expandir a área de dados e IA", d: "Uma instituição financeira de grande porte precisa definir contratação, capacitação e investimento em tecnologia." },
    { r: "COMPLICAÇÃO", t: "Faltam evidências sobre o mercado", d: "Salário, senioridade, stack e modelo de trabalho mudam rápido, e a percepção interna não acompanha." },
    { r: "RESOLUÇÃO", t: "Três edições da mesma pesquisa", d: "14.005 respostas do State of Data Brazil, processadas em um data lake na AWS e lidas como série histórica." },
  ];
  let x = 0.55;
  cards.forEach((c) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.85, w: 3.95, h: 3.15, fill: { color: "F5F8FA" }, line: { color: CINZA, width: 1 }, rectRadius: 0.06 });
    s.addText(c.r, { x: x + 0.32, y: 2.2, w: 3.3, h: 0.3, fontSize: 11, bold: true, color: AZUL_MEDIO, fontFace: F, charSpacing: 1.2, isTextBox: true, margin: 0 });
    s.addText(c.t, { x: x + 0.32, y: 2.6, w: 3.3, h: 0.8, fontSize: 18, color: TINTA, fontFace: F, isTextBox: true, margin: 0 });
    s.addText(c.d, { x: x + 0.32, y: 3.5, w: 3.3, h: 1.35, fontSize: 12.5, color: APOIO, fontFace: F, isTextBox: true, margin: 0, valign: "top" });
    x += 4.2;
  });
  s.addText("Todas as análises deste material respondem a uma dessas três decisões, e nenhuma recomendação aparece sem o número que a sustenta.",
    { x: 0.55, y: 5.35, w: 12.2, h: 0.4, fontSize: 13, italic: true, color: TINTA, fontFace: F, isTextBox: true, margin: 0 });
  rodape(s, "Fonte: enunciado do Tech Challenge Fase 3 e pesquisa State of Data Brazil.");
  s.addNotes("O problema de negócio em três blocos. Fio condutor do material inteiro.");
}

// =====================================================================
// 4. A base
// =====================================================================
{
  const s = slideConteudo("Os dados", "Três edições, mais de mil perguntas, uma base que não se une sozinha");
  const nums = [
    { n: "14.005", d: "respostas nas três\nedições da pesquisa" },
    { n: "1.190", d: "colunas somadas\nentre as edições" },
    { n: "3", d: "padrões diferentes de\nnomenclatura de coluna" },
    { n: "145", d: "códigos que mudam de\nsignificado entre edições" },
  ];
  let x = 0.55;
  nums.forEach((i) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.9, w: 2.95, h: 2.6, fill: { color: "F5F8FA" }, line: { color: CINZA, width: 1 }, rectRadius: 0.06 });
    s.addText(i.n, { x: x + 0.2, y: 2.3, w: 2.55, h: 0.85, fontSize: 34, bold: true, color: AZUL_ESCURO, fontFace: F, align: "center", isTextBox: true, margin: 0 });
    s.addText(i.d, { x: x + 0.2, y: 3.25, w: 2.55, h: 0.9, fontSize: 12, color: APOIO, fontFace: F, align: "center", isTextBox: true, margin: 0 });
    x += 3.15;
  });
  s.addText("Edições utilizadas: 2023-2024, 2024-2025 e 2025-2026, as três últimas publicadas pelo Data Hackers, conforme exige o enunciado.",
    { x: 0.55, y: 5.0, w: 12.2, h: 0.4, fontSize: 14, color: TINTA, fontFace: F, isTextBox: true, margin: 0 });
  s.addText("Após o tratamento restam 14.002 linhas: três registros eram duplicatas integralmente idênticas e foram removidos.",
    { x: 0.55, y: 5.42, w: 12.2, h: 0.4, fontSize: 12.5, color: APOIO, fontFace: F, isTextBox: true, margin: 0 });
  s.addText("Nenhum arquivo foi aberto ou salvo em planilha antes da ingestão, para preservar codificação, separador e formato de origem na camada Bronze.",
    { x: 0.55, y: 5.82, w: 12.2, h: 0.4, fontSize: 12.5, color: APOIO, fontFace: F, isTextBox: true, margin: 0 });
  rodape(s);
  s.addNotes("Preparar a próxima seção: a base parece simples e não é. É aqui que o trabalho técnico começa.");
}

// =====================================================================
// 5. Arquitetura
// =====================================================================
{
  const s = slideConteudo("Arquitetura da solução", "Um data lake em camadas, com todo o processamento em Spark");
  s.addImage({ path: FIG_DECK("arquitetura_aws.png"), x: 0.5, y: 1.6, w: 12.3, h: 4.75 });
  rodape(s, "Diagrama construído no Draw.io. Arquivo editável entregue junto com o material.");
  s.addNotes("Bronze guarda o dado cru, Silver harmoniza, Gold responde a pergunta de negócio. Athena consulta, Glue processa, tudo em us-east-1.");
}

// =====================================================================
// 6. O problema tecnico central
// =====================================================================
{
  const s = slideConteudo("Método", "O código da pergunta muda de significado entre as edições");
  s.addShape(pres.ShapeType.roundRect, { x: 0.55, y: 1.75, w: 7.4, h: 2.75, fill: { color: "F5F8FA" }, line: { color: CINZA, width: 1 }, rectRadius: 0.05 });
  s.addText("O mesmo código 2.q, em três edições", { x: 0.85, y: 1.98, w: 6.8, h: 0.32, fontSize: 14, bold: true, color: TINTA, fontFace: F, isTextBox: true, margin: 0 });
  const linhas = [
    ["2023-2024", "ocorrência de demissões em massa"],
    ["2024-2025", "ocorrência de demissões em massa"],
    ["2025-2026", "modelo de trabalho atual"],
  ];
  let y = 2.48;
  linhas.forEach(([ed, desc], i) => {
    s.addText(ed, { x: 0.85, y, w: 1.7, h: 0.3, fontSize: 12.5, bold: true, color: AZUL_MEDIO, fontFace: F, isTextBox: true, margin: 0 });
    s.addText(desc, { x: 2.6, y, w: 5.1, h: 0.3, fontSize: 12.5, color: i === 2 ? AZUL_ESCURO : APOIO, bold: i === 2, fontFace: F, isTextBox: true, margin: 0 });
    y += 0.42;
  });
  s.addText("Unir as bases pelo código produziria um gráfico comparando demissões com trabalho remoto, sem gerar erro algum na execução.",
    { x: 0.85, y: 3.78, w: 6.8, h: 0.42, fontSize: 12, italic: true, color: APOIO, fontFace: F, isTextBox: true, margin: 0 });

  s.addText("A regra adotada: tripla confirmação", { x: 8.35, y: 1.9, w: 4.4, h: 0.34, fontSize: 15, bold: true, color: AZUL_ESCURO, fontFace: F, isTextBox: true, margin: 0 });
  s.addText([
    { text: "código da pergunta", options: { bullet: true, breakLine: true } },
    { text: "texto integral da pergunta", options: { bullet: true, breakLine: true } },
    { text: "categorias observadas nos dados", options: { bullet: true } },
  ], { x: 8.35, y: 2.32, w: 4.4, h: 1.2, fontSize: 13, color: APOIO, fontFace: F, isTextBox: true, margin: 0, paraSpaceAfter: 6 });
  s.addText("Só entra na série histórica a coluna aprovada nos três critérios. O mapa completo das 237 perguntas equivalentes acompanha a entrega.",
    { x: 8.35, y: 3.62, w: 4.4, h: 0.9, fontSize: 12, color: APOIO, fontFace: F, isTextBox: true, margin: 0 });

  const achados = [
    ["330", "códigos existem nas três edições"],
    ["145", "deles mudam de pergunta"],
    ["237", "perguntas são equivalentes"],
    ["92", "delas trocaram de código"],
  ];
  let x2 = 0.55;
  achados.forEach(([n, d]) => {
    s.addText(n, { x: x2, y: 5.05, w: 3.0, h: 0.5, fontSize: 24, bold: true, color: AZUL_MEDIO, fontFace: F, isTextBox: true, margin: 0 });
    s.addText(d, { x: x2, y: 5.55, w: 3.0, h: 0.6, fontSize: 11.5, color: APOIO, fontFace: F, isTextBox: true, margin: 0 });
    x2 += 3.15;
  });
  rodape(s, "Fonte: análise própria sobre os cabeçalhos das três edições da pesquisa.");
  s.addNotes("Este é o diferencial técnico do trabalho. Sem essa regra, toda a série histórica seria inválida sem que ninguém percebesse.");
}


// =====================================================================
// 7 a 15. Blocos analiticos, um por pergunta do enunciado
// =====================================================================
slideGrafico("Estrutura do mercado",
  "Finanças e tecnologia concentram mais de um terço do mercado",
  "fig08_setor.png",
  [
    { titulo: "Onde estão os profissionais", texto: "Os dois maiores setores somam 36,0% dos respondentes. A diferença entre eles, de 1,1 ponto, não é significativa a 95% de confiança: é empate na liderança." },
    { titulo: "O que isso significa", texto: "O cliente disputa talento em um dos dois maiores empregadores de dados do país, contra concorrentes diretos e contra empresas de tecnologia." },
  ],
  "Fonte: State of Data Brazil, edição 2025-2026, 3.227 respostas válidas para a pergunta de setor.");

slideGrafico("Estrutura do mercado",
  "A concentração no Sudeste aumentou em vez de ceder ao trabalho remoto",
  "fig09_regiao.png",
  [
    { titulo: "Concentração crescente", texto: "O Sudeste sai de 61,4% para 64,4% entre a primeira e a última edição, sem qualquer sinal de dispersão geográfica." },
    { titulo: "Leitura para contratação", texto: "Buscar talento fora do eixo tradicional continua sendo exceção, e não a regra do mercado." },
  ]);

slideGrafico("Perfis valorizados",
  "A faixa mediana do Sênior subiu 40% e as de entrada não se moveram",
  "fig03_salario_nivel.png",
  [
    { titulo: "O que mudou", texto: "O Sênior saiu de R$ 10.000 para R$ 14.000 entre a primeira e a segunda edição e estabilizou. Júnior e Pleno não se moveram." },
    { titulo: "A decisão que isso força", texto: "O preço de entrada da senioridade subiu 40% e o do Pleno não subiu. Formar internamente ficou relativamente mais barato do que disputar Sênior pronto." },
    { titulo: "O topo novo", texto: "A edição 2025-2026 criou o nível Especialista/Staff+, com mediana de R$ 18.000 sobre 349 respostas. Por existir em uma só edição, ele fica fora da série histórica." },
  ],
  "Fonte: State of Data Brazil. Mediana do ponto médio da faixa declarada, não salário médio. Valores nominais, sem correção pela inflação do período.");

slideGrafico("Perfis valorizados",
  "Engenharia de dados e machine learning lideram a mediana salarial",
  "fig12_salario_cargo.png",
  [
    { titulo: "Quem o mercado paga melhor", texto: "ML e AI Engineer lidera com mediana de R$ 18.000. Engenharia e Arquitetura de Dados, Analytics Engineer e Data Product Manager vêm em seguida, todos em R$ 14.000." },
    { titulo: "A distância dentro da área", texto: "Analista de Dados, de BI e de Negócios ficam em R$ 7.000, metade da mediana dos cargos de engenharia. O rótulo genérico de profissional de dados esconde uma diferença de duas vezes." },
    { titulo: "Leitura para o cliente", texto: "Se a expansão prevê plataforma e IA, o orçamento por posição parte de R$ 14.000. Se prevê consumo analítico, parte de R$ 7.000." },
  ],
  "Fonte: State of Data Brazil, edição 2025-2026. Cargos com menos de 30 respostas foram omitidos. Valores nominais.");

slideGrafico("Diversidade de gênero",
  "A participação feminina cai edição após edição, de 24,4% para 22,0%",
  "fig01_genero_serie.png",
  [
    { titulo: "Tendência, não ruído", texto: "São 2,5 pontos perdidos nas duas transições da série, sempre na mesma direção, sobre bases de 5.293, 5.215 e 3.494 respostas." },
    { titulo: "Risco para o cliente", texto: "Uma base que encolhe reduz o alcance de qualquer meta de diversidade construída sobre contratação externa." },
  ]);

slideGrafico("Diversidade de gênero",
  "Proporcionalmente, mais mulheres na entrada e menos no topo",
  "fig02_genero_nivel.png",
  [
    { titulo: "O funil aperta na senioridade", texto: "Entre as mulheres, 25,8% estão no nível Júnior, contra 19,1% entre os homens. No Sênior a relação se inverte, 31,4% contra 35,2%." },
    { titulo: "Onde agir", texto: "O gargalo está na progressão, não apenas na porta de entrada. Programas de promoção interna atacam a causa certa." },
  ],
  "Fonte: State of Data Brazil, edição 2025-2026. O nível Especialista/Staff+ existe apenas nesta edição.");

slideGrafico("Tecnologias",
  "Python domina e o SQL aparece ao lado dele, não no lugar",
  "fig07_linguagens.png",
  [
    { titulo: "Stack estável", texto: "Python é a linguagem preferida de forma dominante nas três edições, sem concorrente próximo." },
    { titulo: "Mudança de formato", texto: "Em 2025-2026 a pergunta passou a aceitar mais de uma resposta, por isso a métrica é a menção e a soma ultrapassa 100% naquela edição." },
  ],
  "Fonte: State of Data Brazil. Percentual de respondentes que citam a linguagem como preferida.");

slideGrafico("Tecnologias",
  "AWS lidera na nuvem e o Power BI não tem concorrente em BI",
  "fig13_ferramentas.png",
  [
    { titulo: "Nuvem", texto: "AWS é a preferida de 31,7% dos respondentes que declaram preferência, à frente de Google Cloud, com 20,6%, e Azure, com 14,7%." },
    { titulo: "Visualização", texto: "Power BI concentra 50,5% da preferência declarada, cinco vezes o segundo colocado. Nenhuma outra ferramenta passa de 10%." },
    { titulo: "Consequência para o cliente", texto: "A solução deste projeto foi construída em AWS, a mesma nuvem em que o mercado tem mais gente pronta para contratar." },
  ],
  "Fonte: State of Data Brazil, edição 2025-2026. Bases de 2.095 e 1.866 respostas válidas.");

slideGrafico("Adoção de inteligência artificial",
  "A adoção de IA quase dobrou enquanto a rejeição caiu pela metade",
  "fig06_ia_serie.png",
  [
    { titulo: "A maior mudança do período", texto: "A IA generativa passou de prioridade declarada por 36,2% dos respondentes para 60,6% em duas edições. Nenhum outro indicador se moveu tanto." },
    { titulo: "A janela está aberta agora", texto: "Quem estrutura a área de IA neste ciclo entra junto com o mercado. Quem esperar mais uma edição entra atrasado." },
  ],
  "Fonte: State of Data Brazil. A pergunta é respondida por quem trabalha em empresa: bases de 896, 1.045 e 652 respostas válidas.");

slideGrafico("Adoção de inteligência artificial",
  "Em duas edições, a IA saiu da margem e virou pauta de orçamento",
  "fig05_ia_prioridade.png",
  [
    { titulo: "O detalhe da mudança", texto: "O crescimento vem das duas faixas de prioridade declarada, com discussão de orçamento, e não de uso informal." },
    { titulo: "Quem ficou para trás", texto: "Apenas 11,4% dos respondentes dizem que a IA não é prioridade na empresa, contra 28,8% duas edições atrás." },
  ],
  "Fonte: State of Data Brazil. A pergunta é respondida por quem trabalha em empresa: bases de 896, 1.045 e 652 respostas válidas.");

slideGrafico("Adoção de inteligência artificial",
  "A prioridade já virou consenso, o resultado em produção ainda não",
  "fig11_ia_impacto.png",
  [
    { titulo: "O tamanho da lacuna", texto: "Enquanto 60,6% declaram a IA como prioridade, apenas 26,5% dizem ter projetos em produção gerando resultado no negócio." },
    { titulo: "Onde o mercado está parado", texto: "38,4% mantêm pilotos rodando sem impacto declarado. Somados aos 15,0% em planejamento, mais da metade ainda não saiu da experimentação." },
    { titulo: "A oportunidade", texto: "A disputa deixou de ser por adotar IA e passou a ser por operacionalizar. Quem tira o piloto do papel primeiro captura o diferencial." },
  ],
  "Fonte: State of Data Brazil, edição 2025-2026, 646 respostas válidas. Pergunta existente apenas nesta edição.");

slideGrafico("Modelos de trabalho",
  "O trabalho remoto recua e o presencial avança",
  "fig04_modelo_trabalho.png",
  [
    { titulo: "Movimento recente", texto: "O remoto integral caiu 6,6 pontos e o presencial integral subiu 4,1, concentrados na última edição." },
    { titulo: "Contramão da preferência", texto: "O modelo que mais encolhe está entre os dois de maior satisfação declarada, empatados no topo, como mostra o gráfico seguinte." },
  ]);

slideGrafico("Retenção",
  "Flexibilidade, e não o remoto puro, separa satisfeitos de insatisfeitos",
  "fig10_satisfacao_modelo.png",
  [
    { titulo: "O que os dados dizem", texto: "Remoto integral e híbrido flexível empatam no topo, com 74,5% e 75,0%. A diferença de 0,5 ponto não é significativa a 95%, com z igual a 0,23." },
    { titulo: "Onde está a diferença real", texto: "A separação está entre ter e não ter flexibilidade: 20,9 pontos entre o híbrido flexível, com 75,0%, e o presencial integral, com 54,0%." },
    { titulo: "Consequência prática", texto: "Política de trabalho deixa de ser assunto administrativo e passa a ser instrumento de retenção de talento escasso." },
  ],
  "Fonte: State of Data Brazil, edição 2025-2026. Bases de 1.281, 631, 645 e 670 respostas por modelo.");

// =====================================================================
// 16. Recomendacoes
// =====================================================================
{
  const s = slideConteudo("Recomendações", "Três decisões que os dados sustentam");
  const recs = [
    {
      r: "CONTRATAR",
      t: "Contratar no meio da carreira e promover por dentro",
      d: "A faixa mediana do Sênior subiu 40% em duas edições e a do Pleno não se moveu. O prêmio pago por senioridade pronta cresceu, o custo de quem ainda vai chegar lá não, e a disputa acontece em um dos dois maiores empregadores de dados do país.",
    },
    {
      r: "CAPACITAR",
      t: "Tratar IA generativa como competência de todo o time",
      d: "Seis em cada dez respondentes dizem que a empresa já priorizou IA, mas só 26,5% declaram projetos em produção gerando resultado. A vantagem competitiva não está mais em adotar, e sim em sair do piloto, o que depende de gente treinada dentro de casa.",
    },
    {
      r: "INVESTIR",
      t: "Usar flexibilidade de trabalho como instrumento de retenção",
      d: "Os dois modelos flexíveis pagam mediana de R$ 14.000, contra R$ 7.000 no presencial integral, e concentram a maior satisfação declarada. Com o remoto encolhendo 6,6 pontos no mercado, manter flexibilidade é alavanca de retenção e de custo ao mesmo tempo.",
    },
  ];
  let y = 1.85;
  recs.forEach((rec) => {
    s.addShape(pres.ShapeType.roundRect, { x: 0.55, y, w: 12.2, h: 1.45, fill: { color: "F5F8FA" }, line: { color: CINZA, width: 1 }, rectRadius: 0.05 });
    s.addText(rec.r, { x: 0.9, y: y + 0.2, w: 2.0, h: 0.3, fontSize: 12, bold: true, color: AZUL_MEDIO, fontFace: F, charSpacing: 1.2, isTextBox: true, margin: 0 });
    s.addText(rec.t, { x: 3.05, y: y + 0.18, w: 9.4, h: 0.34, fontSize: 16, bold: true, color: TINTA, fontFace: F, isTextBox: true, margin: 0 });
    s.addText(rec.d, { x: 3.05, y: y + 0.56, w: 9.4, h: 0.78, fontSize: 12.5, color: APOIO, fontFace: F, isTextBox: true, margin: 0, valign: "top" });
    y += 1.6;
  });
  rodape(s);
  s.addNotes("Cada recomendação amarra em um número apresentado antes. Nenhuma opinião sem dado por trás.");
}

// =====================================================================
// 17. Metodo e limitacoes
// =====================================================================
{
  const s = slideConteudo("Método e limitações", "O que sustenta os números, e o que eles não podem dizer");
  s.addText("Como os números foram apurados", { x: 0.55, y: 1.9, w: 5.9, h: 0.32, fontSize: 15, bold: true, color: AZUL_ESCURO, fontFace: F, isTextBox: true, margin: 0 });
  s.addText([
    { text: "Arquivos originais preservados na camada Bronze, sem tratamento prévio", options: { bullet: true, breakLine: true } },
    { text: "Colunas confirmadas por código, texto da pergunta e categorias observadas", options: { bullet: true, breakLine: true } },
    { text: "Erros de digitação da pesquisa de origem corrigidos e documentados", options: { bullet: true, breakLine: true } },
    { text: "Indicadores principais recalculados por caminho independente", options: { bullet: true, breakLine: true } },
    { text: "Diferenças entre categorias testadas antes de virarem afirmação", options: { bullet: true } },
  ], { x: 0.55, y: 2.42, w: 5.9, h: 3.1, fontSize: 12.5, color: APOIO, fontFace: F, isTextBox: true, margin: 0, paraSpaceAfter: 7, valign: "top" });

  s.addText("O que os dados não permitem afirmar", { x: 6.95, y: 1.9, w: 5.8, h: 0.32, fontSize: 15, bold: true, color: AZUL_ESCURO, fontFace: F, isTextBox: true, margin: 0 });
  s.addText([
    { text: "A pesquisa é voluntária: descreve a comunidade respondente, não o país", options: { bullet: true, breakLine: true } },
    { text: "A remuneração é coletada em faixas, então não existe salário médio aqui", options: { bullet: true, breakLine: true } },
    { text: "Os valores são nominais: a variação não desconta a inflação do período", options: { bullet: true, breakLine: true } },
    { text: "As perguntas sobre IA são respondidas só por quem trabalha em empresa, com base menor", options: { bullet: true, breakLine: true } },
    { text: "A última edição tem menos respondentes, por isso toda comparação é percentual", options: { bullet: true, breakLine: true } },
    { text: "Perguntas de uma só edição não entram em série histórica", options: { bullet: true, breakLine: true } },
    { text: "O nível Especialista/Staff+ existe apenas na edição mais recente", options: { bullet: true } },
  ], { x: 6.95, y: 2.42, w: 5.8, h: 3.1, fontSize: 12.5, color: APOIO, fontFace: F, isTextBox: true, margin: 0, paraSpaceAfter: 7, valign: "top" });

  s.addText("Todo o código, os notebooks executados e as consultas SQL acompanham a entrega e reproduzem estes números do zero.",
    { x: 0.55, y: 5.75, w: 12.2, h: 0.4, fontSize: 13, italic: true, color: TINTA, fontFace: F, isTextBox: true, margin: 0 });
  rodape(s, "Fonte: documentação de auditoria do projeto, entregue junto com o material.");
  s.addNotes("Declarar limitação antes que o avaliador pergunte é o que separa análise de opinião.");
}

// =====================================================================
// 18. Encerramento
// =====================================================================
{
  numero += 1;
  const s = pres.addSlide();
  s.background = { color: FUNDO_ESCURO };
  s.addText("Obrigada", { x: 0.9, y: 2.75, w: 8, h: 0.9, fontSize: 40, color: "FFFFFF", fontFace: F, isTextBox: true, margin: 0 });
  s.addText("O mercado brasileiro de dados está mais caro no topo, mais concentrado do que parece e mais decidido sobre IA do que estava há dois anos. As três decisões deste material saem daí.",
    { x: 0.9, y: 3.75, w: 9.4, h: 1.1, fontSize: 15, color: "FFFFFF", fontFace: F, isTextBox: true, margin: 0 });
  s.addText("Ana Paula Corrêa Galdino  ·  RM370461  ·  POSTECH Data Analytics",
    { x: 0.9, y: 5.9, w: 8.5, h: 0.3, fontSize: 12, color: "FFFFFF", fontFace: F, isTextBox: true, margin: 0 });
  s.addNotes("Fechar retomando a promessa da abertura e abrir para perguntas.");
}

pres.writeFile({ fileName: path.resolve(__dirname, "..", "entregaveis", "TechChallenge_Fase3_MaterialExecutivo.pptx") })
  .then((f) => console.log("gerado:", f, "|", numero, "slides"));
