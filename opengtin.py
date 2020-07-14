import re
import urllib.request as request


class OpenGTIN:
    """
    Python wrapper of the online OpenGTIN database API
    """

    def __init__(self, user_id=400000000):
        self.user_id = str(user_id)
        self.url = 'http://opengtindb.org/?ean='

    def query(self, ean: int):
        query_url = self.url + str(ean) + '&cmd=query&queryid=' + self.user_id
        response = request.urlopen(query_url)
        response = response.read()
        return self.parse_response(response.decode('iso-8859-1'))

    @staticmethod
    def parse_response(response: str):
        """
        The response from the OpenGTIN database consists of key-value pairs separated by an equal sign
        :param response:
        :return:
        """
        regex = re.compile(r'(?P<key>\w+)=(?P<value>.*)')
        product_entry = {
            match.group('key'): match.group('value')
            for match in regex.finditer(response)
        }
        if not product_entry['name']:
            product_entry['name'] = product_entry['detailname']
        return product_entry


if __name__ == '__main__':
    o = OpenGTIN()
    print(o.query(4311501484777))
