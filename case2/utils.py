import io
import xlsxwriter

def gerar_relatorio_excel(queryset):
    # Processamento dados
    dados_organizados = {}
    for item in queryset:
        chave = (item.cas, item.nome)
        if chave not in dados_organizados:
            dados_organizados[chave] = {
                "C": {"solubilidade": "-", "dados": {}},
                "NC": {"solubilidade": "-", "dados": {}},
                "vor_consolidado": "-",
                "valor_vor_consolidado": "-"
            }
        
        # Atualiza dados por efeito (C/NC)
        if item.efeito in ["C", "NC"]:
            d = dados_organizados[chave][item.efeito]
            d["solubilidade"] = item.solu_concentracao or d["solubilidade"]
            d["dados"][item.ambiente] = item
            
            if item.vor and item.vor != "-":
                dados_organizados[chave]["vor_consolidado"] = item.vor
                dados_organizados[chave]["valor_vor_consolidado"] = item.valor_vor

    # Config
    output = io.BytesIO()
    wb = xlsxwriter.Workbook(output, {"in_memory": True})
    ws = wb.add_worksheet("Relatório Consolidado")

    # Estilos
    estilo_base = {"font_name": "Calibri", "font_size": 11, "align": "center", "valign": "vcenter", "text_wrap": True}
    
    # Cabeçalhos
    estilo_topo = wb.add_format({**estilo_base, "bold": True, "bg_color": "#e76a25", "font_color": "#FFFFFF", "border": 1})
    estilo_via = wb.add_format({**estilo_base, "bold": True, "bottom": 1, "bottom_color": "#e76a25"})
    estilo_colunas = wb.add_format({**estilo_base, "bold": True, "bottom": 2, "bottom_color": "#e76a25", "border_color": "#E8E8E8"})
    
    # Formatos de Célula
    estilos_dados = {
        "padrao": wb.add_format({**estilo_base, "border": 1, "border_color": "#E8E8E8"}),
        "numero": wb.add_format({**estilo_base, "border": 1, "border_color": "#E8E8E8", "num_format": "0.00E+00"}),
        "laranja": wb.add_format({**estilo_base, "bg_color": "#FFC299", "bold": True, "border": 1, "num_format": "0.00E+00"}),
        "cinza": wb.add_format({**estilo_base, "bg_color": "#D3D3D3", "bold": True, "border": 1, "num_format": "0.00E+00"})
    }

    # Layout
    ws.merge_range("G1:J2", "MÁXIMAS ACEITÁVEIS PARA ÁGUA\nNO PONTO DE EXPOSIÇÃO", estilo_topo)
    ws.merge_range("G3:J3", "VIA DE EXPOSIÇÃO: INALAÇÃO", estilo_via)
    ws.merge_range("G4:H4", "AMBIENTE ABERTO", estilo_topo)
    ws.merge_range("I4:J4", "AMBIENTE FECHADO", estilo_topo)

    titulos = ["CAS Nº", "CONTAMINANTE", "FONTE VOR", "VALOR VOR", "SOLUBILIDADE", "EFEITO"]
    for col, texto in enumerate(titulos):
        ws.merge_range(0, col, 4, col, texto, estilo_colunas)

    sub_titulos = ["CONC. MÁX\n(mg/L)", "VALOR CONSIDERADO\n(mg/L)", "CONC. MÁX\n(mg/L)", "VALOR CONSIDERADO\n(mg/L)"]
    for i, texto in enumerate(sub_titulos):
        ws.write(4, 6 + i, texto, estilo_colunas)

    # Linhas
    linha_atual = 5
    for (cas, nome), info in dados_organizados.items():
        # Lógica de cor para o Bloco VOR
        tem_alerta = any(getattr(a, 'aplicar_laranja', False) for e in ["C", "NC"] for a in info[e]["dados"].values())
        estilo_vor = estilos_dados["laranja"] if tem_alerta else estilos_dados["numero"]

        # Escreve colunas fixas (Mesclando 2 linhas por substância)
        ws.merge_range(linha_atual, 0, linha_atual + 1, 0, cas, estilos_dados["padrao"])
        ws.merge_range(linha_atual, 1, linha_atual + 1, 1, nome, estilos_dados["padrao"])
        ws.merge_range(linha_atual, 2, linha_atual + 1, 2, info["vor_consolidado"], estilos_dados["padrao"])
        
        val_vor = info["valor_vor_consolidado"]
        ws.merge_range(linha_atual, 3, linha_atual + 1, 3, float(val_vor) if val_vor != "-" else "-", estilo_vor)

        # Detalhes de C e NC
        for i, efeito in enumerate(["C", "NC"]):
            detalhe = info[efeito]
            ws.write(linha_atual + i, 4, detalhe["solubilidade"], estilos_dados["padrao"])
            ws.write(linha_atual + i, 5, efeito, estilos_dados["padrao"])

            for col_idx, amb in enumerate(["Aberto", "Fechado"]):
                obj = detalhe["dados"].get(amb)
                val = float(obj.concentracao_max) if obj and obj.concentracao_max else "-"
                ws.write(linha_atual + i, 6 + (col_idx * 2), val, estilos_dados["numero"] if val != "-" else estilos_dados["padrao"])

        # Colunas de Valor Considerado (H e J)
        for col_idx, amb in enumerate(["Aberto", "Fechado"]):
            obj = info["C"]["dados"].get(amb) or info["NC"]["dados"].get(amb)
            if obj:
                estilo_cons = estilos_dados["cinza"] if getattr(obj, 'aplicar_cinza', False) else estilos_dados["numero"]
                valor_cons = float(getattr(obj, 'valor_considerado', 0))
                ws.merge_range(linha_atual, 7 + (col_idx * 2), linha_atual + 1, 7 + (col_idx * 2), valor_cons, estilo_cons)
            else:
                ws.merge_range(linha_atual, 7 + (col_idx * 2), linha_atual + 1, 7 + (col_idx * 2), "-", estilos_dados["padrao"])

        linha_atual += 2

    # Ajuste de Colunas
    larguras = [15, 40, 15, 15, 18, 10, 20, 20, 20, 20]
    for i, w in enumerate(larguras):
        ws.set_column(i, i, w)

    # Limpar células fora da tabela
    fundo_branco = wb.add_format({"bg_color": "#FFFFFF", "border": 0})
    max_linha = linha_atual - 1  # última linha usada
    max_coluna = 9   # coluna J

    for r in range(0, 50):
        for c in range(0, 15):
            # Só aplica se estiver fora da tabela
            if r > max_linha or c > max_coluna:
                ws.write(r, c, "", fundo_branco)

    wb.close()
    output.seek(0)
    return output