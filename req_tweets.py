import requests
import json
from bs4 import BeautifulSoup
import csv


instance ="twitter.com"
# URL de la instancia local de Nitter
base_url = "http://localhost:8080"

# Hashtag a buscar
hashtag = "Conquis4ETB"

# Realizar la búsqueda de tweets con el hashtag especificado
search_url = f"{base_url}/search?f=tweets&q={hashtag}&e-nativeretweets=on&e-media=on&e-verified=on&since=&until="

# definir variable global para contar los tweets en scope que se pueda utilizar en la función recursiva
i = 0


def save_tweets(url):
    global i
    response = requests.get(url)

    def has_exact_class(tag):
        return tag.get('class') == ['show-more']

    soup = BeautifulSoup(response.text, "html.parser")
    show_more_div = soup.find(has_exact_class)

    tweets_data = []

    for tweet in soup.find_all("div", class_="timeline-item", limit=100):
        i+=1
        # Contenido del tweet
        content = tweet.find("div", class_="tweet-content").get_text(strip=True) if tweet.find("div",
                                                                                               class_="tweet-content") else "N/A"

        # Usuario que publicó el tweet
        user_elem = tweet.find("a", class_="username")
        username = user_elem.text.strip() if user_elem else "N/A"
        user_link = f"{instance}{user_elem['href']}" if user_elem and 'href' in user_elem.attrs else "N/A"

        # Enlace al tweet
        tweet_link_elem = tweet.find("a", class_="tweet-link")
        tweet_link = f"{instance}{tweet_link_elem['href']}" if tweet_link_elem and 'href' in tweet_link_elem.attrs else "N/A"

        tweets_data.append([username, user_link, content, tweet_link])

    with open("tweets_definitivo.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        #writer.writerow(["Usuario", "Perfil", "Tweet", "Enlace"])  # Encabezados
        writer.writerows(tweets_data)

    if i >= 80:
        exit(0)
    else:
        # buscar la siguiente página y guardar los tweets recursivamente
        #print(show_more_div)
        if show_more_div:
            link = show_more_div.find('a')
            if link and 'href' in link.attrs:
                href = link['href']
                print(f'Enlace encontrado: {href}')
                url = f"{base_url}/search{href}"
                save_tweets(url)

            else:
                print('No se encontró el atributo href en el enlace:\n ', soup)
        else:
            print('No se encontró el div con la clase "show-more":\n ', soup)

save_tweets(search_url)