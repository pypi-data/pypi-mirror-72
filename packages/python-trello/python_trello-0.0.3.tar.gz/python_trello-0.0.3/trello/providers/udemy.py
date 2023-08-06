from trello.providers import Provider
from trello.utility import get_soup
import requests


class Udemy(Provider):
    """Class to get all the courses from udemy"""

    def __init__(self, user_id):
        """Constructor to the Udemy class"""
        self.user_id = user_id
        self.url = "https://www.udemy.com/user/{}/".format(self.user_id)
        self.soup = get_soup(self.url)
        self.courses = []
        self.api_id = self.get_api_id()
        self.api_url = "https://www.udemy.com/api-2.0/users/{}/subscribed-profile-courses/".format(self.api_id)
        self.course_url = "https://www.udemy.com/api-2.0/courses/{}/public-curriculum-sections"
        self.get_cards_api()

    def get_cards_api(self):
        self.hit_api()

    def hit_api(self):
        # @TODO add headers
        r = requests.get(self.api_url)
        response = r.json()
        if response['next']:
            self.api_url = response['next']
            self.hit_api()
        self.courses.extend(response['results'])

    def get_api_id(self):
        t = self.soup.find('div', {'class': 'img-circle user-avatar__img'})
        id = t.attrs['style'].replace("background-image:url(", "").replace(")", "")
        return id.split('/')[-1].split('_')[0]

    def get_cards(self):
        self.get_all_pages()
        return self.courses

    def get_titles(self, soup):
        """Get all course titles from a page"""
        titles = []
        for course in soup.find_all('li', {'class': 'card'}):
            title = course.find('strong', {'class': 'details__name'}).text.strip().strip('\n').strip()
            url = course.find('a').get('href')
            img = course.find('img', {'class': 'img'}).get('src')
            titles.append({'title': title, 'url': 'https://www.udemy.com{}'.format(url), 'thumbnail': img})
        return titles

    def get_all_pages(self):
        """Methog to get all the pages from udemy course"""
        pages = self.get_max_pages()
        for i in range(1, int(pages) + 1):
            url = "https://udemy.com/user/{}/?subscribed_courses={}&key=subscribed_courses".format(self.get_user_id(),
                                                                                                   i)
            soup = get_soup(url)
            self.courses.extend(self.get_titles(soup))

    def get_user_id(self):
        """Method to get the user id from the url"""
        return self.url.strip('/').split('/')[-1]

    def get_max_pages(self):
        pages_text = self.soup.find('ul', {'class': 'pagination'}).find_all('li')[-2].text
        return pages_text.strip().strip('\n').strip()

    def get_curriculum(self, course_id):
        """
        Get the currliculum from any udemy course url
        """
        # @TODO add headers
        r = requests.get(self.course_url.format(str(course_id)))
        try:
            return [x['title'] for x in r.json()['results']]
        except KeyError:
            print(course_id)
            raise KeyError
