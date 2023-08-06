class Provider(object):
    """Blueprint for provider"""
    def __init__(self, url=None, username=None, password=None):
        self.url = url
        self.username = username
        self.password = password

    def get_cards(self):
        """`Provider` should return cards"""
        raise NotImplementedError
