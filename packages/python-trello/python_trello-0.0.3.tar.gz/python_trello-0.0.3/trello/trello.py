import requests


class Trello(object):
    """
    A class to implement Trello Api
    """

    def __init__(self, trello_key, trello_token):
        """
        Constructor for `Trello` class
        """
        self.trello_key = trello_key
        self.trello_token = trello_token
        self.payload = {
            'key': self.trello_key,
            'token': self.trello_token
        }
        self.base_url = "https://api.trello.com/1"

    def _get_response(self, url):
        response = requests.request("GET", url, params=self.payload)
        if response.status_code != requests.codes.ok:
            return None
        return response.json()

    def get_lists(self, board_id):
        return self._get_response(self.base_url + '/boards/{}/lists'.format(board_id))

    def get_cards(self, list_id):
        return self._get_response(self.base_url + '/lists/{}/cards'.format(list_id))

    def get_card(self, card_id):
        return self._get_response(self.base_url + '/cards/{}'.format(card_id))

    def create_checklist(self, card_id, name):
        """
        Create a checklist on the card with `card_id`
        return id of the checklist created else None
        """
        url = self.base_url + '/cards/{}/checklists'.format(card_id)
        payload = {
            'key': self.trello_key,
            'token': self.trello_token,
            'name': name
        }
        response = requests.request("POST", url, params=payload)
        if response.status_code != requests.codes.ok:
            return None
        return response.json()['id']

    def add_items_to_checklist(self, checklist_id, items):
        """
        Adds item to an already created checklists with `checklist_id`
        `items` should be an iterable.
        """
        # @TODO add exceptions
        url = self.base_url + '/checklists/{}/checkItems'.format(checklist_id)
        for name in items:
            payload = {
                'key': self.trello_key,
                'token': self.trello_token,
                'name': name
            }
            requests.request("POST", url, params=payload)

    def create_card(self, list_id, name, desc):
        """
        Create a card on the list with id `list_id`
        """
        url = self.base_url + '/cards'
        payload = {
            'key': self.trello_key,
            'token': self.trello_token,
            'idList': list_id,
            'name': name,
            'desc': desc
        }
        response = requests.request("POST", url, params=payload)
        if response.status_code != requests.codes.ok:
            return None
        return response.json()['id']

    def add_attachment_to_card(self, card_id, attachment_url, name):
        """
        Add an attachment to an existing card with `card_id`
        """
        url = self.base_url + '/cards/{}/attachments'.format(card_id)
        payload = {
            'key': self.trello_key,
            'token': self.trello_token,
            'id': card_id,
            'url': attachment_url,
            'name': name
        }
        response = requests.request("POST", url, params=payload)
        if response.status_code != requests.codes.ok:
            return None
        return response.json()['id']

    def create_webhook(self, redirect_url, board_id, description="webhook"):
        url = self.base_url + f'/tokens/{self.trello_token}/webhooks'
        payload = {
            'key': self.trello_key,
            'callbackURL': redirect_url,
            'description': description,
            'idModel': board_id,
        }
        response = requests.request("POST", url, params=payload)
        if response.status_code != requests.codes.ok:
            return None
        return response.json()
