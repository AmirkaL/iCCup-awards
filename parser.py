import requests
from bs4 import BeautifulSoup

def get_iccup_awards(nickname):

    url = f"https://iccup.com/dota/profile/awards/{nickname}.html"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        awards_containers = soup.find_all('div', class_='awards-container')

        result = []
        seen_awards = set()

        for container in awards_containers:
            awards_list = container.find('div', class_='awards-list')
            if awards_list:
                awards = awards_list.find_all('div', class_='singleAward')
                for award in awards:
                    if 'award-off' not in award.get('class', []):
                        title = award.find('h4', class_='award-title').text.strip()
                        reason = award.find('p', class_='award-desc').text.strip()
                        image = award.find('img')['src']

                        if not image.startswith('http'):
                            image = 'https://iccup.com' + image

                        award_key = (title, image)
                        if award_key not in seen_awards:
                            seen_awards.add(award_key)
                            result.append({'title': title, 'reason': reason, 'image': image})

        return result

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return []


if __name__ == '__main__':
    nickname = input("Введите никнейм профиля iCCup: ")
    awards = get_iccup_awards(nickname)

    if awards:
        print("\nНаграды:")
        for award in awards:
            print(f"- {award['title']}: {award['reason']} ({award['image']})")
    else:
        print(f"У профиля {nickname} нет наград или профиль не найден.")