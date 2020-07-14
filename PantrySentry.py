import gkeepapi
import keyring

from Database import Database
from opengtin import OpenGTIN


class PantrySentry:
    """
    The PantrySentry class is the top-level class to interact with the Pantry Sentry.
    """

    def __init__(self, local_ean_db_name='ean.db',
                 keep_username='sipreuss@gmail.com',
                 keep_password=keyring.get_password('Google Keep', 'sipreuss@gmail.com'),
                 keep_list_name='Basement food'):
        """
        Create a new PantrySentry
        """
        # Get the local, persistent EAN database that is queried before any web services are used
        self.local_ean_db = Database(local_ean_db_name)
        # Handle to the online Open GTIN database in case an item is not already in the local db
        self.online_ean_db = OpenGTIN()
        self.keep = gkeepapi.Keep()
        print("Logging into Google Keep...", end="")
        self.keep.login(username=keep_username, password=keep_password)
        print("...done.")
        # Google Keep API returns a generator but we assume only the first returned note is the pantry inventory
        self.pantry = [p for p in self.keep.find(query=keep_list_name)][0]

    def barcode_to_product_name(self, ean: int):
        """ Get the product name based on the barcode """
        product = self.local_ean_db[ean]
        if not product.name:
            db_entry = self.online_ean_db.query(ean)
            product = Database.Product(ean=ean, name=db_entry['name'], description=db_entry['descr'])
            # Update the local database
            self.local_ean_db[ean] = product
        return product.name

    def add_item(self, item_name: str):
        # TODO: Check if item already exists and increase count instead of adding
        self.pantry.add(item_name, False)
        self.keep.sync()

    def start(self):
        while True:
            print("Waiting for EAN input...")
            ean = int(input())
            product_name = self.barcode_to_product_name(ean)
            self.add_item(product_name)
            print(f"Added {product_name} to the pantry.")


if __name__ == '__main__':
    pantry_sentry = PantrySentry()
    print("Starting the Pantry Sentry")
    pantry_sentry.start()
