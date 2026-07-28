from datetime import datetime
import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st

# Configuração da Página do Streamlit com ícone e mensagem customizados
st.set_page_config(
    page_title="Sistema de Recibos A3", 
    page_icon="🤝",  # Ícone de aperto de mãos (representando acordo/pagamento)
    layout="wide"
)

# Mensagem de carregamento customizada (aparece na tela preta antes do app abrir)
st.markdown("""
    <style>
        div.stApp {
            background-image: url(https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjc2dDFobzNrdzNhaHR4N3hxbXg0aW80dGRsdWNjOXh5b3g1bGFucyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l49K2rmETDVrqy7yM/giphy.gif);
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: 0.5;
        }
    </style>
""", unsafe_allow_html=True)

st.info("Carregando Sistema Financeiro A3... Aguarde um momento.")

# URL da sua imagem (exemplo)
IMAGE_URL = "https://i.imgur.com/dinheiro.png" # Substitua pelo seu link

st.set_page_config(
    page_title="Sistema de Recibos A3", 
    page_icon=IMAGE_URL, # Usa sua imagem como ícone de aba e carregamento
    layout="wide"
)

# Opcional: Colocar a mesma imagem gigante no centro da tela enquanto carrega
st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 70vh;">
        <img src="{IMAGE_URL}" width="200px" alt="Carregando...">
    </div>
    <h3 style="text-align: center; color: #2e7d32;">Acessando sistema de pagamentos...</h3>
""", unsafe_allow_html=True)

# Estilização CSS customizada para deixar o visual moderno
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            width: 100%;
            border-radius: 6px;
            font-weight: 600;
            background-color: #2e7d32;
            color: white;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #1b5e20;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Nome do arquivo de relatório
EXCEL_RELATORIO = "relatorio_pagamentos.xlsx"


def gerar_pdf_recibo(dados, filename="recibo.pdf"):
  c = canvas.Canvas(filename, pagesize=A4)
  largura, altura = A4

  # Cabeçalho decorativo superior
  c.setFillColor(colors.HexColor("#1b5e20"))
  c.rect(0, altura - 20, largura, 20, fill=1, stroke=0)

  # Cabeçalho da Empresa
  c.setFillColor(colors.black)
  c.setFont("Helvetica-Bold", 13)
  c.drawString(50, altura - 55, "A3 SERVIÇOS E PRODUTOS EM ALUMÍNIO LTDA")

  c.setFont("Helvetica-Bold", 18)
  c.setFillColor(colors.HexColor("#2e7d32"))
  c.drawCentredString(largura / 2, altura - 105, "RECIBO DE PAGAMENTO / VALE")

  # Linha divisória
  c.setStrokeColor(colors.HexColor("#cccccc"))
  c.setLineWidth(1)
  c.line(50, altura - 120, largura - 50, altura - 120)

  # Informações principais
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  y = altura - 150

  c.drawString(50, y, "FUNCIONÁRIO(A) / RECEBEDOR:")
  c.setFont("Helvetica", 11)
  c.setFillColor(colors.black)
  c.drawString(220, y, f"{dados['FUNCIONÁRIO(A)']}")

  y -= 25
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, "EQUIPE:")
  c.setFont("Helvetica", 11)
  c.setFillColor(colors.black)
  c.drawString(220, y, f"{dados['EQUIPE']}")

  y -= 25
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, "TIPO DE OPERAÇÃO:")
  c.setFont("Helvetica", 11)
  c.setFillColor(colors.black)
  c.drawString(220, y, f"{dados['TIPO DE OPERAÇÃO/ DESCRIÇÃO']}")

  y -= 25
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, "DATA DE EMISSÃO:")
  c.setFont("Helvetica", 11)
  c.setFillColor(colors.black)
  c.drawString(
      220, y, f"{datetime.now().strftime('%d/%m/%Y às %H:%M')}"
  )

  y -= 45
  # Tabela de Valores (Caixa de Destaque)
  c.setFillColor(colors.HexColor("#f1f8e9"))
  c.rect(50, y - 45, largura - 100, 45, fill=1, stroke=1)
  c.setStrokeColor(colors.HexColor("#c8e6c9"))

  c.setFont("Helvetica-Bold", 11)
  c.setFillColor(colors.HexColor("#1b5e20"))
  c.drawString(65, y - 28, "DESCRIÇÃO DO LANÇAMENTO")
  c.drawRightString(largura - 65, y - 28, f"R$ {dados['VALOR A SER PAGO']:.2f}")

  y -= 80
  # Dados Bancários
  c.setFont("Helvetica-Bold", 12)
  c.setFillColor(colors.HexColor("#333333"))
  c.drawString(50, y, "DADOS BANCÁRIOS / PAGAMENTO")
  y -= 15
  c.setStrokeColor(colors.HexColor("#dddddd"))
  c.line(50, y, largura - 50, y)

  y -= 25
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, f"Forma/Banco:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(130, y, f"{dados['BANCO PORTADOR']}")

  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(320, y, f"Tipo:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(380, y, f"{dados['TIPO']}")

  y -= 22
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, f"Agência:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(130, y, f"{dados['AGENCIA']}")

  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(320, y, f"Conta:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(380, y, f"{dados['CONTA']}")

  y -= 22
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, f"Chave PIX:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(130, y, f"{dados['CHAVE PIX']}")

  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(320, y, f"Titular:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(380, y, f"{dados['TITULAR DA CONTA']}")

  # Assinatura
  y -= 130
  c.setStrokeColor(colors.HexColor("#333333"))
  c.setLineWidth(1)
  c.line(120, y, largura - 120, y)
  y -= 18
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.black)
  c.drawCentredString(
      largura / 2, y, f"Assinatura do Recebedor: {dados['FUNCIONÁRIO(A)']}"
  )

  c.save()


# --- INTERFACE PRINCIPAL ---

st.title("📄 Sistema de Emissão de Recibos e Vales")
st.markdown(
    "Gerencie pagamentos e emissores de recibos de forma rápida, moderna e"
    " organizada."
)
st.divider()

# Criação de Abas para Organização
aba_emissao, aba_relatorio = st.tabs(
    ["📝 Emitir Novo Recibo", "📊 Relatório e Histórico"]
)

with aba_emissao:
  st.subheader("Preencha os dados do recibo")

  with st.form("form_recibo", clear_on_submit=False):
    col1, col2, col3 = st.columns(3)

    with col1:
      st.markdown("##### 👤 Colaborador")
      funcionario = st.text_input("Nome do Funcionário(a)")
      equipe = st.selectbox("Equipe", ["NOITE", "MANHA", "TARDE", "GERAL"])

    with col2:
      st.markdown("##### 💰 Financeiro")
      valor = st.number_input(
          "Valor a ser pago (R$)", min_value=0.0, format="%.2f"
      )
      tipo_operacao = st.selectbox(
          "Tipo de Operação", ["VALE", "PAGAMENTO", "ADIANTAMENTO"]
      )

    with col3:
      st.markdown("##### 🏦 Dados Bancários")
      banco = st.text_input("Banco Portador", value="DINHEIRO")
      tipo_pagamento = st.text_input(
          "Tipo (ex: PIX, Dinheiro, ND)", value="ND"
      )

    st.markdown("---")
    col4, col5, col6 = st.columns(3)
    with col4:
      agencia = st.text_input("Agência", value="ND")
    with col5:
      conta = st.text_input("Conta", value="ND")
    with col6:
      chave_pix = st.text_input("Chave PIX", value="ND")

    titular = st.text_input(
        "Titular da Conta (Opcional - preenche com o nome se vazio)"
    )

    st.markdown("")
    submitted = st.form_submit_button(
        "🚀 Gerar Recibo em PDF e Salvar no Relatório"
    )

  if submitted:
    if not funcionario:
      st.error("Por favor, preencha o nome do funcionário.")
    else:
      dados_novo = {
          "FUNCIONÁRIO(A)": funcionario,
          "VALOR A SER PAGO": valor,
          "BANCO PORTADOR": banco,
          "TIPO": tipo_pagamento,
          "AGENCIA": agencia,
          "CONTA": conta,
          "CHAVE PIX": chave_pix,
          "TITULAR DA CONTA": titular if titular else funcionario,
          "EQUIPE": equipe,
          "TIPO DE OPERAÇÃO/ DESCRIÇÃO": tipo_operacao,
          "STATUS": "PAGO",
          "DATA": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      }

      # 1. Salvar no Relatório (Excel)
      if os.path.exists(EXCEL_RELATORIO):
        df_existente = pd.read_excel(EXCEL_RELATORIO)
        df_novo = pd.concat(
            [df_existente, pd.DataFrame([dados_novo])], ignore_index=True
        )
      else:
        df_novo = pd.DataFrame([dados_novo])

      df_novo.to_excel(EXCEL_RELATORIO, index=False)

      # 2. Gerar PDF do Recibo
      pdf_filename = f"recibo_{funcionario.replace(' ', '_')}.pdf"
      gerar_pdf_recibo(dados_novo, pdf_filename)

      st.success(
          "✨ Recibo gerado com sucesso e adicionado ao relatório de"
          " acompanhamento!"
      )

      # Botão elegante para download do PDF
      with open(pdf_filename, "rb") as pdf_file:
        st.download_button(
            label="📥 Clique aqui para baixar o PDF do Recibo",
            data=pdf_file,
            file_name=pdf_filename,
            mime="application/pdf",
        )

with aba_relatorio:
  st.subheader("📊 Acompanhamento de Pagamentos e Vales")

  if os.path.exists(EXCEL_RELATORIO):
    df_rel = pd.read_excel(EXCEL_RELATORIO)

    # Cards de Métricas Estilizadas
    col_m1, col_m2, col_m3 = st.columns(3)
    total_pago = df_rel["VALOR A SER PAGO"].sum()
    total_registros = len(df_rel)

    col_m1.metric(
        label="💵 Valor Total Lançado", value=f"R$ {total_pago:,.2f}"
    )
    col_m2.metric(label="📋 Total de Recibos Emitidos", value=total_registros)
    col_m3.metric(
        label="🏢 Equipes Atendidas", value=df_rel["EQUIPE"].nunique()
    )

    st.markdown("---")

    # Exibição da tabela interativa
    st.dataframe(df_rel, use_container_width=True)

    st.markdown("")
    # Botão para baixar a planilha completa
    with open(EXCEL_RELATORIO, "rb") as excel_file:
      st.download_button(
          label="📥 Baixar Planilha Consolidada (Excel)",
          data=excel_file,
          file_name="relatorio_pagamentos.xlsx",
          mime=(
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ),
      )
  else:
    st.info(
        "Ainda não há registros salvos. Emita o primeiro recibo na aba ao"
        " lado!"
    )
