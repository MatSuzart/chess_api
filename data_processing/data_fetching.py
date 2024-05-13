import requests
import re
from bs4 import BeautifulSoup

def fetch_players(query):
    # Definir a URL para a consulta de pesquisa
    url = "https://fide.com/search"

    # Cabeçalhos com base nas informações fornecidas
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'Content-Type': 'application/json',
        'Origin': 'https://fide.com',
        'Referer': f'https://fide.com/search?query={query}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    # Os parâmetros da consulta
    params = {'query': query}

    # Fazer a requisição GET
    response = requests.get(url, headers=headers, params=params)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        search_blocks = soup.find_all('div', class_='member-block')
    
        # Inicializar uma lista para armazenar informações do jogador
        players = []

        for block in search_blocks:
            player_entries = block.find_all(class_="member-block__one")
            
            for entry in player_entries:
                # Extrair o nome do jogador
                player_name = entry.find(class_="member-block-info-position").get_text(strip=True)
                
                # Extrair o título do jogador, se disponível
                player_title = entry.find(class_="member-block-info-name")
                player_title = player_title.get_text(strip=True) if player_title else "Sem título"
                
                # Extrair a URL do perfil do jogador
                player_url = entry.find('a')['href']
                
                # Extrair o ID do jogador da URL usando regex
                player_id_match = re.search(r'/profile/(\d+)', player_url)
                player_id = player_id_match.group(1) if player_id_match else "Sem ID"

                # Anexar as informações extraídas à lista de jogadores
                if 'profile' in player_url and 'news' not in player_url:
                    players.append({
                        'name': player_name,
                        'title': player_title,
                        'url': player_url,
                        'id': player_id  # Adicionar ID do jogador ao dicionário
                    })   
    else:
        print(f"Falha ao recuperar dados. Código de status: {response.status_code}")

    return players

# Dados do jogador Erigaisi Arjun
playerName = 'Erigaisi Arjun'
FIDE_ID = '35009192'

# Chamar a função fetch_players com o nome do jogador
player_info = fetch_players(playerName)

# Imprimir as informações do jogador
print("Informações do jogador:")
for player in player_info:
    print(f"Nome: {player['name']}")
    print(f"Título: {player['title']}")
    print(f"URL do perfil: {player['url']}")
    print(f"ID do jogador: {player['id']}")
    print()  # Linha em branco para separar os jogadores
