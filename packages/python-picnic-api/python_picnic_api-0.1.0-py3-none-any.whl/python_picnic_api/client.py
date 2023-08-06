from .session import PicnicAPISession


class PicnicAPI:
    def __init__(self, username: str, password: str):
        """Instantiate a new API client.

        Args:
            username (str): username, usualy your email. Defaults to None.
            password (str): password. Defaults to None.
        """
        self._username = username
        self._password = password

        self.session = PicnicAPISession()
        self.session.login(username, password)

    def _get(self, path: str):
        url = "https://storefront-prod.nl.picnicinternational.com/api/15" + path
        return self.session.get(url).json()

    def _post(self, path: str, data):
        url = "https://storefront-prod.nl.picnicinternational.com/api/15" + path
        return self.session.post(url, json=data).json()
        

    def get_user(self):
        return self._get('/user')

    def search(self, term):
        path = '/search?search_term=' + term
        return self._get(path)

    def get_cart(self):
        return self._get('/cart')

    def add_product_to_cart(self, productId, count=1):
        data = {'product_id': productId, 'count': count}
        return self._post('/cart/add_product', data)

    def remove_product_from_cart(self, productId, count=1):
        data = {'product_id': productId, 'count': count}
        return self._post('/cart/remove_product', data)

    def clear_cart(self):
        return self._post('/cart/clear')

    def get_delivery_slots(self):
        return self._get('/cart/delivery_slots')
    
    def get_current_deliveries(self):
        data = ["CURRENT"]
        return self._post('/deliveries', data=data)


if __name__ == "__main__":
    sess = PicnicAPI("alyxissbrink@gmail.com", "vr387WEJ!")
