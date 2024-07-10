# Bibliotecas a serem utilizadas
import pytesseract
import cv2
import streamlit as st
from pdf2image import convert_from_path
import tempfile
import shutil
from PIL import Image

# Define o caminho para o executável do Tesseract dentro do repositório
tesseract_cmd = os.path.join(os.path.dirname(__file__), 'tesseract.exe')

# Identificação do local onde realmente se encontra o tesseract (o pip instala em lugar errado)
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# FUNÇÃO PARA TRANSFORMAR PDF EM PNG
def conversor_png(arquivo):
    # Leitura da imagem
    images = convert_from_path(arquivo, poppler_path="D:\\Users\\50109192\\AppData\\Local\\Programs\\Tesseract-OCR\\poppler-24.02.0\\Library\\bin")
    # Salvar cada pagina do PDF como uma imagem em uma lista
    lista_imagens_pdf = []
    for page in range(0, len(images)):
        lista_imagens_pdf.append(images[page])
    return lista_imagens_pdf

# FUNÇÃO PARA OCR COMPLETO DE PÁGINA DO PDF
def extracao_texto(nome_arquivo):
    # Leitura da imagem
    img = cv2.imread(nome_arquivo)
    # OCR da imagem lida
    return pytesseract.image_to_string(img, lang='por')

# CRIANDO INTERFACE

# Ajustando as variáveis dentro das "session states", para lidar melhor com os autos re-run do streamlit
if 'check_envio' not in st.session_state:
    st.session_state['check_envio'] = False
    # Tornar a check_envio para true depois que for clicada
def check_envio_true():
    st.session_state['check_envio'] = True
    # Tornar a check_envio para false caso o arquivo selecionado seja alterado
def check_envio_false():
    st.session_state.check_envio = False

# Abrindo a logo da Arcelor para colocar como ícone da página
icon_arcelor = Image.open('logo_cinza_laranja.png')

# Ajustando a largura e características da página
st.set_page_config(page_title="Extrator De Textos", layout='centered',page_icon=icon_arcelor)

# Título da página

st.header("📃Extrator de Textos (OCR)")
st.subheader("Carregue abaixo arquivos em formato PNG ou PDF para exrair textos. ")
st.write("Obs.: O reconhecimento dos textos não é 100%. Confira e valide antes de qualquer uso.")

st.write('')
st.write('')
st.write('')
st.write('')
st.write('')

# Campo para upload de arquivo
img_user = st.file_uploader(label="Selecione seu arquivo:",accept_multiple_files=False, type=['png','pdf'])

# Se imagem selecionada...
if img_user:
    
    st.write('')
    st.write('')

    # Espaço em branco reservado para o botão de envio
    enviar_button_placeholder = st.empty()

    # Se o botão de envio ainda não tiver sido apertado, ele aparece
    if st.session_state['check_envio'] == False:
        if enviar_button_placeholder.button(label="Enviar"):
            # Se o botão de envio for apertado, ele some
            enviar_button_placeholder.empty()

            # Enquanto a imagem está sendo lida, fica um spinner rodando
            with st.spinner('Extraindo texto do arquivo selecionado...'):

                # Criar um arquivo temporário para armazenar o upload
                with tempfile.NamedTemporaryFile(delete=False) as temp_file_nome_incorreto:
                    temp_file_nome_incorreto.write(img_user.getbuffer())
                    temp_file_nome_incorreto_path = temp_file_nome_incorreto.name

                # Conferência do tipo de arquivo inputado - se for png
                if img_user.type == 'image/png':

                    # Invocando a função de extração criada
                    resultado_ocr = extracao_texto(temp_file_nome_incorreto_path)

                    # Apagar botão
                    check_envio_false()

                    # Gerando o texto extraído
                    st.download_button('Download do arquivo gerado.',data=resultado_ocr, file_name="Texto_Extraido.txt",type='primary')
                
                # Conferência do tipo de arquivo inputado - se for pdf
                else:
                    resultado_conversao = conversor_png(temp_file_nome_incorreto_path)

                    # Lista para armazenar os caminhos dos arquivos temporários
                    arquivos_temporarios = []

                    # Salva cada imagem como um arquivo temporário
                    for i, image in enumerate(resultado_conversao):
                        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                        image.save(temp_file.name)
                        arquivos_temporarios.append(temp_file.name)

                    # Criando uma lista com quantidade de páginas para alimentar o seletor
                    resultado_ocr_convertido_final = str()
                    for qtd, name in enumerate(arquivos_temporarios):   
                    
                        resultado_ocr_convertido = extracao_texto(name)
                        resultado_ocr_convertido_final += f"--------------PÁGINA {qtd+1}--------------" + "\n" + resultado_ocr_convertido + "\n"
                    
                        # Espaço reservado para o botão de envio
                    enviar_button_placeholder = st.empty()

                    # Botão para download do arquivo
                    download = st.download_button('Download do arquivo gerado.',
                                                data=resultado_ocr_convertido_final, 
                                                file_name="Texto_Extraido.txt",
                                                type='primary')
                

                    # Invocando a função de extração criada para ler cada imagem criada do pdf
                    #for indice_arquivo, arquivos in enumerate(arquivos_temporarios):

                    #    resultado_ocr_convertido = extracao_texto(arquivos_temporarios[indice_arquivo])
                    #    st.text(resultado_ocr_convertido)


# Assinatura GITD
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.divider()
st.markdown("_Aplicativo desenvolvido e mantido pela Gerência de Inovação e Transformação Digital - VPFCT_")
