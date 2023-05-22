import os
import speech_recognition as sr
import datetime
import wikipedia
from gtts import gTTS 
import playsound
import pywhatkit
import pyautogui
import pysimplegui as sg
import re
import time
import openai
from GoogleNews import GoogleNews

googlenews = GoogleNews(lang='pt', period='2d')
openai.api_key = "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"
ultimas_noticias_faladas = []
limite_noticias = 5

sg.theme('DarkAmber')  

layout = [  [sg.Text('Pandora ON')] ]

window = sg.Window('Window Title', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()

def obter_resposta(texto):
    response = openai.Completion.create(
        engine="davinci",
        prompt=texto,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def execute_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Ouvindo...')
        audio = r.listen(source)
    try:
        comando = r.recognize_google(audio, language='pt-BR')
        comando = comando.lower()
        if 'pandora' in comando:
            comando = comando.replace('pandora', '')
            return comando
    except sr.UnknownValueError:
        print('Não entendi o comando.')
    except sr.RequestError as e:
        print(f'Erro na conexão com o serviço de reconhecimento de voz: {e}')
    return None

def falar(texto):
    if texto and texto.strip():  
        tts = gTTS(text=texto, lang='pt-br')
        arquivo_temporario = 'temp.mp3'
        tts.save(arquivo_temporario)
        playsound.playsound(arquivo_temporario)
        os.remove(arquivo_temporario)
    else:
        print('Nenhum texto para falar.')

def comando_voz_usuario():
    comando = execute_comando()
    if comando is not None:
        if 'bom dia' in comando:
                    falar('Bom dia, em que posso ajudar?')
        elif 'boa tarde' in comando:
                    falar('Boa tarde, em que posso ajudar?')
        elif 'boa noite' in comando:
                    falar('Boa noite, Durma bem')
        elif 'horas' in comando:
                    hora = datetime.datetime.now().strftime('%H:%M')
                    falar('Agora são ' + hora)
        elif 'data' in comando:
                    data = datetime.date.today().strftime('%d/%m/%Y')
                    falar('Hoje é ' + data)
        elif 'procure por' in comando:
                    procurar = comando.replace('procure por', '')
                    wikipedia.set_lang('pt')
                    resultado = wikipedia.summary(procurar, 2)
                    falar(resultado)
        elif 'notícias' in comando:
                    jornal = comando.replace('notícias', '')
                    googlenews.search(jornal)
                    noticias = googlenews.result()
                    contador_noticias = 0
                    for noticia in noticias:
                        if contador_noticias >= limite_noticias:
                            break
                        titulo = noticia['title']
                        if titulo not in ultimas_noticias_faladas:
                            falar(titulo)
                            ultimas_noticias_faladas.append(titulo)
                            contador_noticias += 0
                        else:
                            continue
        elif 'toque' in comando:
                    musica = comando.replace('toque', '')
                    resultado = pywhatkit.playonyt(musica)
                    resultado_sem_link = ' '.join([palavra for palavra in resultado.split() if 'youtube.com' not in palavra])
                    falar('tocando música ' + resultado_sem_link)
        elif 'pesquise' in comando:
                    termo_pesquisa = comando.replace('pesquise', '')
                    pesquisa_url = f'{termo_pesquisa}'
                    pywhatkit.search(pesquisa_url)
                    falar(f'pesquisando{termo_pesquisa} no google.')
        elif 'abrir' and 'abra' in comando:
            abra = comando.replace('abrir', '')
            pyautogui.press('win')
            time.sleep(1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         )
            pyautogui.write(abra)
            time.sleep(1)
            pyautogui.press('enter')
            falar(f'abrindo o {abra}')
        else:
            resposta = obter_resposta(comando)
            falar(resposta)

while True:
    comando_voz_usuario()
    time.sleep(2)
