from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip, TextClip, concatenate_videoclips

# Dimensões do vídeo (Formato Vertical 9:16 ideal para Reels, Shorts e WhatsApp)
largura, altura = 720, 1280
fps = 24

# 1. Cena de Abertura: Dor do Cliente
fundo_1 = ColorClip(size=(largura, altura), color=(248, 249, 250)).set_duration(4)
texto_dor = TextClip(
    "Cansado de preencher\nrecibos à mão?",
    fontsize=40, color="black", font="Arial-Bold", align="center"
).set_duration(4).set_position(("center", "center"))

cena_1 = CompositeVideoClip([fundo_1, texto_dor])

# 2. Cena do Sistema / Logo
fundo_2 = ColorClip(size=(largura, altura), color=(27, 94, 32)).set_duration(4) # Verde corporativo
try:
    logo = ImageClip("gutaflow.png").resize(width=200).set_duration(4).set_position(("center", 400))
    tem_logo = True
except:
    tem_logo = False

texto_sistema = TextClip(
    "Guta Flow Recibos\n\nSistema Web para Empresas",
    fontsize=32, color="white", font="Arial-Bold", align="center"
).set_duration(4).set_position(("center", 650))

if tem_logo:
    cena_2 = CompositeVideoClip([fundo_2, logo, texto_sistema])
else:
    cena_2 = CompositeVideoClip([fundo_2, texto_sistema])

# 3. Cena da Solução (PDF e Relatórios)
fundo_3 = ColorClip(size=(largura, altura), color=(255, 255, 255)).set_duration(4)
texto_solucao = TextClip(
    "✅ Recibos em PDF na hora\n✅ Relatórios em Excel\n✅ Controle por Equipes",
    fontsize=34, color="#1b5e20", font="Arial-Bold", align="center"
).set_duration(4).set_position(("center", "center"))

cena_3 = CompositeVideoClip([fundo_3, texto_solucao])

# 4. Cena de Chamada para Ação (CTA)
fundo_4 = ColorClip(size=(largura, altura), color=(30, 30, 30)).set_duration(4)
texto_cta = TextClip(
    "Modernize sua empresa hoje!\n\nEntre em contato e teste.",
    fontsize=36, color="white", font="Arial-Bold", align="center"
).set_duration(4).set_position(("center", "center"))

cena_4 = CompositeVideoClip([fundo_4, texto_cta])

# Concatenando todas as cenas em um único vídeo final
video_final = concatenate_videoclips([cena_1, cena_2, cena_3, cena_4])

# Salvando o arquivo de vídeo gerado
print("Renderizando o vídeo de demonstração, aguarde...")
video_final.write_videofile("demonstracao_gutaflow.mp4", fps=fps, codec="libx264", audio=False)
print("Vídeo gerado com sucesso: 'demonstracao_gutaflow.mp4'!")
