import requests
from bs4 import BeautifulSoup
import json

def coletar_citacoes(url):
    """
    Coleta citações, autores e tags de uma página web.
    """
    print(f"Coletando dados de: {url}")
    dados_coletados = []
    
    try:
        # Faz a requisição HTTP para a URL
        response = requests.get(url)
        # Se a requisição não for bem-sucedida, levanta um erro
        response.raise_for_status()

        # Analisa o HTML da página com Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra todos os blocos de citação na página
        blocos_de_citacao = soup.find_all('div', class_='quote')
        
        # Percorre cada bloco de citação para extrair os dados
        for bloco in blocos_de_citacao:
            texto = bloco.find('span', class_='text').text.strip()
            autor = bloco.find('small', class_='author').text.strip()
            tags_html = bloco.find('div', class_='tags').find_all('a', class_='tag')
            
            # Extrai o texto de cada tag
            tags = [tag.text.strip() for tag in tags_html]
            
            dados_coletados.append({
                'cita': texto,
                'autor': autor,
                'tags': tags
            })
            
        return dados_coletados

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return []
    except Exception as e:
        print(f"Erro ao processar a página de {url}: {e}")
        return []

if __name__ == "__main__":
    # URL do site de exemplo
    URL_ALVO = "http://quotes.toscrape.com/"
    
    # Chama a função para coletar os dados
    todas_as_citacoes = coletar_citacoes(URL_ALVO)
    
    # Salva os dados em um arquivo JSON
    with open('dados_coletados.json', 'w', encoding='utf-8') as f:
        json.dump(todas_as_citacoes, f, ensure_ascii=False, indent=4)
        
    print("\n--- Coleta de Dados Finalizada ---")
    print(f"Total de citações coletadas: {len(todas_as_citacoes)}")
    print("Os dados foram salvos no arquivo 'dados_coletados.json'.")