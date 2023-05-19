from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time

# Realiza o scraping duas vezes com um intervalo de 5 segundos
for i in range(4):

    req = Request(
       url='https://www.amazon.com.br/Boa-Noite-Punpun-Inio-Asano/dp/8545709617/ref=sr_1_18?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=22AADNKEK4C4M&keywords=manga&qid=1684276476&sprefix=mang%2Caps%2C229&sr=8-18',
       headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    )

    try:
        pagina = urlopen(req).read()
        bs = BeautifulSoup(pagina, "html.parser")
    except HTTPError as e:
        print(e)  # mostra o erro
    except URLError as e:
        print('Servidor não encontrado.')
    else:
        regex = r'<span(?: class="[^"]*")?\s*id="price"[^>]*>(.*?)</span>' # Usei aspas simples para a regex por causa das aspas duplas do id

        '''Explicação da regex:
           Há apenas uma ocorrência da tag span com o id "price" no html da página, e ela envolve o preço atual do produto.
           Por isso, essa regex captura todos os caracteres que estão dentro da tag span com id "price", independentemente
           dos outros atributos da tag span (os carecteres (?: class="[^"]*")? fazem com que o atributo class seja ignorado, e
           com [^>]*, a regex aceita quaisquer caracteres que não sejam o > de fechamento da tag após o atributo id). 
           Para capturar o preço, os caracteres >(.*?) capturam todos os caracteres após o ">" e antes do fechamento da tag span.
        '''

        # Buscamos o elemento span com id "price" na página
        try:
            elemento_span = bs.find("span", {"id": "price"})
        except AttributeError as e:
            print('Tag não encontrada')
        else:
            # Salvamos o match da regex no preco
            if  not elemento_span:
                print("Elemento não encontrado")
                break
            else:
                match = re.search(regex, str(elemento_span))
                if match:
                    preco = match.group(
                        1)  # O match.group(1) é necessário para pegar a parte da regex que está no grupo de captura (.*?) - definido pelos parênteses
                    print('Preço no site agora:')
                    print(preco)


            # Teste do preço e manipulação dos arquivos

            arquivo_alertas = 'alerta_de_precos.txt'
            arquivo_preco = 'ultimo_preco.txt'

            # Abrindo o arquivo do preço em modo write
            with open(arquivo_preco, 'w') as a_preco:
                a_preco.write(preco)

            # Caso o preço não tenha mudado sozinho, adicionamos um novo preço fictício
            preco_modificado = 'R$ {}'.format(round(random.uniform(20.00, 100.00), 2))

            if i > 0:
                if preco_antigo == preco:
                    with open(arquivo_preco, 'w') as a_preco:
                        a_preco.write(preco_modificado)

                with open(arquivo_alertas, 'a') as a_alertas:
                    mensagem = 'O preço mudou de {} para {}\n'.format(preco_antigo, preco_modificado)
                    a_alertas.write(mensagem)
                    preco_antigo = preco_modificado
            else:
                # Vai salvar o preco antigo como o preço normal apenas na primeira raspagem
                with open(arquivo_preco, 'r') as a_preco:
                    a_preco.seek(0)  # Para voltar ao início do arquivo
                    preco_antigo = a_preco.read()

# Aguarda 5 segundos entre as raspagens
time.sleep(5)