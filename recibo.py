from datetime import datetime
import hashlib
import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st

# Configuração da Página do Streamlit
st.set_page_config(
    page_title="Guta Flow - Recibos",
    page_icon="🤝",
    layout="wide",
)

# Estilização CSS customizada para botões e espaçamentos
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

# Arquivo de cadastro de empresas simulado
DB_EMPRESAS = "empresas_cadastradas.csv"


def hash_senha(senha):
  return hashlib.sha256(senha.encode()).hexdigest()


def inicializar_banco_empresas():
  if not os.path.exists(DB_EMPRESAS):
    df_init = pd.DataFrame([
        {
            "usuario": "a3_aluminio",
            "senha": hash_senha("123456"),
            "razao_social": "A3 SERVIÇOS E PRODUTOS EM ALUMÍNIO LTDA",
            "cnpj": "00.000.000/0001-00",
        },
        {
            "usuario": "construtora_alpha",
            "senha": hash_senha("123456"),
            "razao_social": "ALPHA CONSTRUTORA E INCORPORADORA S/A",
            "cnpj": "11.111.111/0001-11",
        },
    ])
    df_init.to_csv(DB_EMPRESAS, index=False)


inicializar_banco_empresas()


def gerar_pdf_recibo(dados, razao_social, cnpj_empresa, filename="recibo.pdf"):
  c = canvas.Canvas(filename, pagesize=A4)
  largura, altura = A4

  c.setFillColor(colors.HexColor("#1b5e20"))
  c.rect(0, altura - 20, largura, 20, fill=1, stroke=0)

  c.setFillColor(colors.black)
  c.setFont("Helvetica-Bold", 12)
  c.drawString(50, altura - 55, razao_social)
  c.setFont("Helvetica", 9)
  c.setFillColor(colors.HexColor("#666666"))
  c.drawString(50, altura - 70, f"CNPJ: {cnpj_empresa}")

  c.setFont("Helvetica-Bold", 18)
  c.setFillColor(colors.HexColor("#2e7d32"))
  c.drawCentredString(largura / 2, altura - 110, "RECIBO DE PAGAMENTO / VALE")

  c.setStrokeColor(colors.HexColor("#cccccc"))
  c.setLineWidth(1)
  c.line(50, altura - 125, largura - 50, altura - 125)

  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  y = altura - 155

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
  c.drawString(220, y, f"{datetime.now().strftime('%d/%m/%Y às %H:%M')}")

  y -= 45
  c.setFillColor(colors.HexColor("#f1f8e9"))
  c.rect(50, y - 45, largura - 100, 45, fill=1, stroke=1)
  c.setStrokeColor(colors.HexColor("#c8e6c9"))

  c.setFont("Helvetica-Bold", 11)
  c.setFillColor(colors.HexColor("#1b5e20"))
  c.drawString(65, y - 28, "DESCRIÇÃO DO LANÇAMENTO")
  c.drawRightString(largura - 65, y - 28, f"R$ {dados['VALOR A SER PAGO']:.2f}")

  y -= 80
  c.setFont("Helvetica-Bold", 12)
  c.setFillColor(colors.HexColor("#333333"))
  c.drawString(50, y, "DADOS BANCÁRIOS / PAGAMENTO")
  y -= 15
  c.setStrokeColor(colors.HexColor("#dddddd"))
  c.line(50, y, largura - 50, y)

  y -= 25
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, "Forma/Banco:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(130, y, f"{dados['BANCO PORTADOR']}")

  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(320, y, "Tipo:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(380, y, f"{dados['TIPO']}")

  y -= 22
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, "Agência:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(130, y, f"{dados['AGENCIA']}")

  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(320, y, "Conta:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(380, y, f"{dados['CONTA']}")

  y -= 22
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(50, y, "Chave PIX:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(130, y, f"{dados['CHAVE PIX']}")

  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(colors.HexColor("#555555"))
  c.drawString(320, y, "Titular:")
  c.setFont("Helvetica", 10)
  c.setFillColor(colors.black)
  c.drawString(380, y, f"{dados['TITULAR DA CONTA']}")

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


# --- CONTROLE DE SESSÃO E LOGIN ---
if "autenticado" not in st.session_state:
  st.session_state["autenticado"] = False
  st.session_state["usuario"] = None
  st.session_state["razao_social"] = None
  st.session_state["cnpj"] = None

if "modo_cadastro" not in st.session_state:
  st.session_state["modo_cadastro"] = False

if not st.session_state["autenticado"]:
  # Criando colunas para centralizar e diminuir a largura visual da caixa de login
  _, col_centro, _ = st.columns([1, 1.2, 1])

  with col_centro:
    # Exibindo o logo centralizado (certifique-se de que o arquivo 'gutaflow.png' está na mesma pasta)
    st.image("gutaflow.png", width=140, use_container_width=False)

    if not st.session_state["modo_cadastro"]:
      st.markdown(
          "<h3 style='text-align: center;'>Acesso ao Sistema</h3>",
          unsafe_allow_html=True,
      )

      with st.form("form_login"):
        usuario_input = st.text_input("Usuário da Empresa")
        senha_input = st.text_input("Senha", type="password")
        btn_login = st.form_submit_button("Entrar no Sistema")

        if btn_login:
          df_empresas = pd.read_csv(DB_EMPRESAS)
          empresa_encontrada = df_empresas[
              (df_empresas["usuario"] == usuario_input)
              & (df_empresas["senha"] == hash_senha(senha_input))
          ]

          if not empresa_encontrada.empty:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario_input
            st.session_state["razao_social"] = empresa_encontrada.iloc[0][
                "razao_social"
            ]
            st.session_state["cnpj"] = empresa_encontrada.iloc[0]["cnpj"]
            st.success("Login realizado com sucesso! Carregando...")
            st.rerun()
          else:
            st.error("Usuário ou senha inválidos.")

      with st.expander("ℹ️ Empresas de Demonstração"):
        st.markdown("- **Usuário:** `a3_aluminio` | **Senha:** `123456`")
        st.markdown("- **Usuário:** `construtora_alpha` | **Senha:** `123456`")

      st.markdown("---")
      st.markdown(
          "<p style='text-align: center; margin-bottom: 5px;'>Ainda não tem"
          " cadastro?</p>",
          unsafe_allow_html=True,
      )
      if st.button("🏢 Cadastrar Nova Empresa"):
        st.session_state["modo_cadastro"] = True
        st.rerun()

    else:
      st.markdown(
          "<h3 style='text-align: center;'>Cadastro de Nova Empresa</h3>",
          unsafe_allow_html=True,
      )

      with st.form("form_cadastro_empresa", clear_on_submit=True):
        nova_razao = st.text_input("Razão Social da Empresa")
        novo_cnpj = st.text_input("CNPJ")
        novo_usuario = st.text_input("Nome de Usuário para Acesso")
        nova_senha = st.text_input("Senha", type="password")

        btn_cadastrar = st.form_submit_button("✨ Finalizar Cadastro")

        if btn_cadastrar:
          if (
              not nova_razao
              or not novo_cnpj
              or not novo_usuario
              or not nova_senha
          ):
            st.error("Por favor, preencha todos os campos do cadastro.")
          else:
            df_empresas = pd.read_csv(DB_EMPRESAS)
            if novo_usuario in df_empresas["usuario"].values:
              st.error("Este nome de usuário já existe. Escolha outro.")
            else:
              nova_linha = pd.DataFrame([{
                  "usuario": novo_usuario,
                  "senha": hash_senha(nova_senha),
                  "razao_social": nova_razao,
                  "cnpj": novo_cnpj,
              }])
              df_empresas = pd.concat(
                  [df_empresas, nova_linha], ignore_index=True
              )
              df_empresas.to_csv(DB_EMPRESAS, index=False)
              st.success(
                  "Empresa cadastrada com sucesso! Os campos foram limpos."
              )

      st.markdown("---")
      if st.button("🔙 Voltar para o Login"):
        st.session_state["modo_cadastro"] = False
        st.rerun()

else:
  # --- INTERFACE PRINCIPAL (APÓS O LOGIN) ---
  usuario_atual = st.session_state["usuario"]
  razao_social_atual = st.session_state["razao_social"]
  cnpj_atual = st.session_state["cnpj"]
  excel_relatorio = f"relatorio_pagamentos_{usuario_atual}.xlsx"

  with st.sidebar:
    st.subheader("🏢 Empresa Conectada")
    st.info(f"**{razao_social_atual}**\n\nCNPJ: {cnpj_atual}")
    if st.button("🚪 Sair / Logout"):
      st.session_state["autenticado"] = False
      st.session_state["usuario"] = None
      st.session_state["razao_social"] = None
      st.session_state["cnpj"] = None
      st.rerun()

  st.title("💹 Sistema de Emissão de Recibos e Vales")
  st.markdown(
      "Gerencie pagamentos e emissores de recibos para"
      f" **{razao_social_atual}** de forma rápida e organizada."
  )
  st.divider()

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
        banco = st.text_input("Banco Portador", value="")
        tipo_pagamento = st.text_input(
            "Tipo (ex: PIX, Dinheiro, Depósito)", value=""
        )

      st.markdown("---")
      col4, col5, col6 = st.columns(3)
      with col4:
        agencia = st.text_input("Agência", value="")
      with col5:
        conta = st.text_input("Conta", value="")
      with col6:
        chave_pix = st.text_input("Chave PIX", value="")

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

        if os.path.exists(excel_relatorio):
          df_existente = pd.read_excel(excel_relatorio)
          df_novo = pd.concat(
              [df_existente, pd.DataFrame([dados_novo])], ignore_index=True
          )
        else:
          df_novo = pd.DataFrame([dados_novo])

        df_novo.to_excel(excel_relatorio, index=False)

        pdf_filename = f"recibo_{funcionario.replace(' ', '_')}.pdf"
        gerar_pdf_recibo(
            dados_novo, razao_social_atual, cnpj_atual, pdf_filename
        )

        st.success(
            "✨ Recibo gerado com sucesso e adicionado ao relatório de"
            " acompanhamento!"
        )

        with open(pdf_filename, "rb") as pdf_file:
          st.download_button(
              label="📥 Clique aqui para baixar o PDF do Recibo",
              data=pdf_file,
              file_name=pdf_filename,
              mime="application/pdf",
          )

  with aba_relatorio:
    st.subheader("📊 Acompanhamento de Pagamentos e Vales")

    if os.path.exists(excel_relatorio):
      df_rel = pd.read_excel(excel_relatorio)

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
      st.dataframe(df_rel, use_container_width=True)

      st.markdown("")
      with open(excel_relatorio, "rb") as excel_file:
        st.download_button(
            label="📥 Baixar Planilha Consolidada da Empresa (Excel)",
            data=excel_file,
            file_name=f"relatorio_{usuario_atual}.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
    else:
      st.info(
          "Ainda não há registros salvos para esta empresa. Emita o primeiro"
          " recibo na aba ao lado!"
      )
