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
        if int(product_entry['error']) != 0:
            raise OpenGtinException(int(product_entry['error']))
        return product_entry


class OpenGtinException(Exception):
    def __init__(self, code: int):
        self.error_codes = {
            0: ["OK", "Operation war erfolgreich"],
            1: ["not found", "die EAN konnte nicht gefunden werden"],
            2: ["checksum", "die EAN war fehlerhaft (Checksummenfehler)"],
            3: ["EAN-format", "die EAN war fehlerhaft (ungültiges Format / fehlerhafte Ziffernanzahl)"],
            4: ["not a global, unique EAN",
                "es wurde eine für interne Anwendungen reservierte EAN eingegeben (In-Store, Coupon etc.)"],
            5: ["access limit exceeded", "Zugriffslimit auf die Datenbank wurde überschritten"],
            6: ["no product name", "es wurde kein Produktname angegeben"],
            7: ["product name too long", "der Produktname ist zu lang (max. 20 Zeichen)"],
            8: ["no or wrong main category id",
                "die Nummer für die Hauptkategorie fehlt oder liegt außerhalb des erlaubten Bereiches"],
            9: ["no or wrong sub category id",
                "die Nummer für die zugehörige Unterkategorie fehlt oder liegt außerhalb des erlaubten Bereiches"],
            10: ["illegal data in vendor field", "unerlaubte Daten im Herstellerfeld"],
            11: ["illegal data in description field", "unerlaubte Daten im Beschreibungsfeld"],
            12: ["data already submitted", "Daten wurden bereits übertragen"],
            13: ["queryid missing or wrong",
                 "die UserID/queryid fehlt in der Abfrage oder ist für diese Funktion nicht freigeschaltet"],
            14: ["unknown command", "es wurde mit dem Parameter 'cmd' ein unbekanntes Kommando übergeben"]
        }
        self.code = code
        self.message = self.error_codes[code]

    def __str__(self):
        return f"OpenGTIN API returned the error code {self.code}: {self.message[0]}"


if __name__ == '__main__':
    o = OpenGTIN()
    try:
        print(o.query(3))
    except OpenGtinException as e:
        print(e)
