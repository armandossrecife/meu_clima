import requests
import configparser

# Carrega o token de um arquivo de configuração
token = configparser.ConfigParser()
token.read("config.ini")
MEU_TOKEN = token["climatempo"]["token"]

# API do servico clima tempo (https://www.climatempo.com.br/)
API_CLIMA_TEMPO = 'http://apiadvisor.climatempo.com.br/api/v1'

def pega_dados_clima_local():
    """
    Pega as informações básicas da localidade padrão (BR)
    - retorno: lista contendo um dicionário com os dados de retorno
    """
    URL = f"{API_CLIMA_TEMPO}/anl/synoptic/locale/BR?token={MEU_TOKEN}"
    try: 
        # Faz a requisicao do servico
        response_dados_clima_local = requests.get(URL)
        if response_dados_clima_local.status_code==200: 
            dados = response_dados_clima_local.json()
            qtd_itens = len(dados)
            informacoes = dados[qtd_itens-1]
            pais = informacoes['country']
            data = informacoes['date']
            texto = informacoes['text']
            return pais, data, texto
        else: 
            # retorna o conteudo do erro levantando uma excecao
            retorno_erro = response_dados_clima_local.json()
            messagem_erro = retorno_erro['detail']
            raise ValueError(messagem_erro) 
    except Exception as ex: 
        print(f"pega_dados_clima_local Erro: {str(ex)}")
        return None

print('Serviço de referência: Clima Tempo (https://www.climatempo.com.br/)')
print('Aguarde...')
try: 
    if pega_dados_clima_local(): 
        pais, data, texto = pega_dados_clima_local()
        print('Mostra informações gerais da localidade: ')
        print(f"País: {pais}")
        print(f"Data: {data}")
        print(f"Informações: {texto}")
    else: 
        print('Dados indisponíveis')
except Exception as ex: 
    print(f"Erro: {str(ex)}")
