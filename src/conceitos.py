"""
Mapa de conceitos de negocio para colunas de cada edicao.

Regra do projeto: nenhuma coluna entra na analise pelo codigo da pergunta.
O codigo muda de significado entre edicoes. Cada conceito abaixo foi resolvido
pela descricao da pergunta e sera validado pelo dominio de valores observado
antes de qualquer agregacao.

Cada entrada: conceito -> {edicao: descricao_normalizada_da_pergunta}
A resolucao para o nome real da coluna acontece em tempo de execucao.
"""

# perguntas do enunciado que cada conceito atende
COBERTURA = {
    "R17": "Como esta estruturado o mercado brasileiro de Dados",
    "R18": "Quais perfis profissionais sao mais valorizados",
    "R19": "Cenario de diversidade de genero",
    "R20": "Tecnologias com maior adocao",
    "R21": "Indice de adocao de IA e seu impacto",
    "R22": "Diferencas entre regioes, senioridades e modelos de trabalho",
    "R23": "Oportunidades e desafios para empresas",
}

CONCEITOS = {
    # ---------- perfil demografico ----------
    "idade":            {"desc": {"2023-2024": "idade", "2024-2025": "idade", "2025-2026": "idade"}, "req": ["R17"]},
    "faixa_idade":      {"desc": {"2023-2024": "faixa_idade", "2024-2025": "faixa_idade", "2025-2026": "faixa_idade"}, "req": ["R17"]},
    "genero":           {"desc": {"2023-2024": "genero", "2024-2025": "genero", "2025-2026": "genero"}, "req": ["R19"]},
    "regiao_onde_mora": {"desc": {"2023-2024": "regiao_onde_mora", "2024-2025": "regiao_onde_mora", "2025-2026": "regiao_onde_mora"}, "req": ["R22"]},
    "uf_onde_mora":     {"desc": {"2023-2024": "uf_onde_mora", "2024-2025": "uf_onde_mora", "2025-2026": "uf_onde_mora"}, "req": ["R22"]},
    "nivel_ensino":     {"desc": {"2023-2024": "nivel_de_ensino", "2024-2025": "nivel_de_ensino", "2025-2026": "nivel_de_ensino"}, "req": ["R17"]},
    "area_formacao":    {"desc": {"2023-2024": "area_de_formacao", "2024-2025": "area_de_formacao", "2025-2026": "area_de_formacao"}, "req": ["R17"]},

    # ---------- vinculo e empresa ----------
    "situacao_trabalho": {"desc": {"2023-2024": "qual_sua_situacao_atual_de_trabalho", "2024-2025": "situacao_de_trabalho", "2025-2026": "situacao_de_trabalho"}, "req": ["R17"]},
    "setor":             {"desc": {"2023-2024": "setor", "2024-2025": "setor", "2025-2026": "setor"}, "req": ["R17"]},
    "porte_empresa":     {"desc": {"2023-2024": "numero_de_funcionarios", "2024-2025": "numero_de_funcionarios", "2025-2026": "numero_de_funcionarios"}, "req": ["R17"]},
    "tamanho_time_dados":{"desc": {"2023-2024": "qual_o_numero_aproximado_de_pessoas_que_atuam_com_dados_na_sua_empresa_hoje", "2024-2025": "numero_de_pessoas_em_dados", "2025-2026": "numero_de_pessoas_em_dados"}, "req": ["R17"]},

    # ---------- carreira e remuneracao ----------
    "cargo":            {"desc": {"2023-2024": "cargo_atual", "2024-2025": "cargo_atual", "2025-2026": "cargo_atual"}, "req": ["R18"]},
    "nivel":            {"desc": {"2023-2024": "nivel", "2024-2025": "nivel", "2025-2026": "nivel"}, "req": ["R18", "R19", "R22"]},
    "faixa_salarial":   {"desc": {"2023-2024": "faixa_salarial", "2024-2025": "faixa_salarial", "2025-2026": "faixa_salarial"}, "req": ["R18", "R19"]},
    "tempo_exp_dados":  {"desc": {"2023-2024": "quanto_tempo_de_experiencia_na_area_de_dados_voce_tem", "2024-2025": "tempo_de_experiencia_em_dados", "2025-2026": "tempo_de_experiencia_em_dados"}, "req": ["R18"]},
    "atua_como_gestor": {"desc": {"2023-2024": "gestor", "2024-2025": "atua_como_gestor", "2025-2026": "atua_como_gestor"}, "req": ["R19"]},

    # ---------- modelo de trabalho e satisfacao ----------
    "modelo_trabalho":       {"desc": {"2023-2024": "atualmente_qual_a_sua_forma_de_trabalho", "2024-2025": "modelo_de_trabalho_atual", "2025-2026": "modelo_de_trabalho_atual"}, "req": ["R22"]},
    "modelo_trabalho_ideal": {"desc": {"2023-2024": "qual_a_forma_de_trabalho_ideal_para_voce", "2024-2025": "modelo_de_trabalho_ideal", "2025-2026": "modelo_de_trabalho_ideal"}, "req": ["R22", "R23"]},
    "satisfacao":            {"desc": {"2023-2024": "voce_esta_satisfeito_na_sua_empresa_atual", "2024-2025": "satisfeito_atualmente", "2025-2026": "satisfeito_atualmente"}, "req": ["R23"]},
    "planos_mudar":          {"desc": {"2023-2024": "voce_pretende_mudar_de_emprego_nos_proximos_6_meses", "2024-2025": "planos_de_mudar_de_emprego_6m", "2025-2026": "planos_de_mudar_de_emprego_6m"}, "req": ["R23"]},

    # ---------- tecnologia ----------
    "linguagem_preferida": {"desc": {"2023-2024": "entre_as_linguagens_listadas_abaixo_qual_e_a_sua_preferida", "2024-2025": "linguagem_preferida", "2025-2026": "linguagem_preferida"}, "req": ["R20"]},
    "cloud_preferida":     {"desc": {"2023-2024": "cloud_preferida", "2024-2025": "cloud_preferida", "2025-2026": "cloud_preferida"}, "req": ["R20"]},
    "bi_preferida":        {"desc": {"2023-2024": "qual_sua_ferramenta_de_bi_preferida", "2024-2025": "ferramenta_de_bi_preferida", "2025-2026": "ferramenta_de_bi_preferida"}, "req": ["R20"]},

    # ---------- inteligencia artificial ----------
    "ia_prioridade":  {"desc": {"2023-2024": "ai_generativa_e_uma_prioridade_em_sua_empresa", "2024-2025": "ai_generativa_e_llm_e_uma_prioridade", "2025-2026": "ai_generativa_e_llm_e_uma_prioridade"}, "req": ["R21"]},
    # so existe na edicao 2025-2026, portanto nao entra em serie historica
    "ia_resultados":  {"desc": {"2025-2026": "empresa_esta_conseguindo_ter_bons_resultados_com_llms"}, "req": ["R21"], "escopo": "edicao_unica"},
    "ia_barreiras":   {"desc": {"2023-2024": "motivos_que_levam_a_empresa_a_nao_usar_ai_genrativa_e_llms", "2024-2025": "motivos_para_nao_usar_ai_generativa_e_llm", "2025-2026": "motivos_para_nao_usar_ai_generativa_e_llm"}, "req": ["R21", "R23"]},
    "ia_tipo_uso":    {"desc": {"2023-2024": "tipos_de_uso_de_ai_generativa_e_llms_na_empresa", "2024-2025": "tipo_de_uso_de_ai_generativa_e_llm_na_empresa", "2025-2026": "tipo_de_uso_de_ai_generativa_e_llm_na_empresa"}, "req": ["R21"]},
    "ia_uso_pessoal": {"desc": {"2023-2024": "utiliza_chatgpt_ou_llms_no_trabalho", "2024-2025": "usa_chatgpt_ou_copilot_no_trabalho", "2025-2026": "usa_chatgpt_ou_copilot_no_trabalho"}, "req": ["R21"]},
}
