import requests
import xmltodict
import json

from trello.providers import Provider
from trello.exceptions import ResponseNotOKError
from trello.utility import get_soup

class Goodreads(Provider):
    """
    Class to represent the Goodreads books
    """
    def __init__(self, key, secret, username):
        """
        Constructor for the Goodreads class
        """
        self.key = key
        self.secret = secret
        self.username = username
        self.url = "https://www.goodreads.com/user/show/{}.xml".format(self.username)
        self.shelves = []
        self.books = []
        self.get_cards()

    def get_shelves(self):
        """Method to get the shelves of the user"""
        payload = {'key': self.key}
        headers = {
            'User-Agent': 'TrelloUpdater',
            'From': 'anubhav.yadav@gmx.com',
        }
        r = requests.get(self.url, headers=headers, params=payload)
        if r.status_code != 200:
            raise ResponseNotOKError("Response was no 200!: {}".format(r.status_code))
        xml_obj = xmltodict.parse(r.text)
        json_response = json.loads(json.dumps(xml_obj))
        for shelf in json_response['GoodreadsResponse']['user']['user_shelves']['user_shelf']: 
            self.shelves.append({'name': shelf['name'], 'id': shelf['id']['#text']})

    def get_books_from_shelf(self, shelf_name):
        """Method to get list of all books from a given shelf"""
        url = "https://www.goodreads.com/review/list/{}?&shelf={}&per_page=infinite".format(self.username, shelf_name)
        soup = get_soup(url)
        books = []
        for row in soup.find('tbody', {'id': 'booksBody'}).find_all('tr'):
            title = row.find('td', {'class': 'field title'}).find('a').text.strip('\n').strip()
            url = row.find('td', {'class': 'field title'}).find('a').get('href')
            url = "https://goodreads.com{}".format(url)
            isbn = row.find('td', {'class': 'field isbn'}).find('div').text.strip()
            author = row.find('td', {'class': 'field author'}).find('div').text.strip()
            thumbnail = row.find('td', {'class': 'field cover'}).find('img').get('src')
            avg_rating = row.find('td', {'class': 'field avg_rating'}).find('div').text.strip()
            books.append({
                'title': title,
                'url': url,
                'isbn': isbn,
                'author': author,
                'thumbnail': thumbnail,
                'avg_rating': avg_rating
            })
        return books

    def get_cards(self):
        self.get_shelves()
        for shelf in self.shelves:
            self.books.extend(self.get_books_from_shelf(shelf['name']))
