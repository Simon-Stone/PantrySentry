import keyring

import userdata
from Database import Database
from listmanager import ListManager
from opengtin import OpenGTIN, OpenGtinException


class PantrySentry:
    """
    The PantrySentry class is the top-level class to interact with the Pantry Sentry.
    """

    def __init__(self, local_ean_db_name='ean.db'):
        """
        Create a new PantrySentry
        """
        # Get the local, persistent EAN database that is queried before any web services are used
        self.local_ean_db = Database(local_ean_db_name)
        # Handle to the online Open GTIN database in case an item is not already in the local db
        self.online_ean_db = OpenGTIN(userdata.openGTIN_user_id)
        self.pantry = ListManager(userdata.google_keep_username,
                                  keyring.get_password('Google Keep', userdata.google_keep_username),
                                  list_name='Basement food')

    def barcode_to_product_name(self, ean: int):
        """ Get the product name based on the barcode """
        product = self.local_ean_db[ean]
        if not product.name:
            try:
                db_entry = self.online_ean_db.query(ean)
                product = Database.Product(ean=ean, name=db_entry['name'], description=db_entry['descr'])
                # Update the local database
                self.local_ean_db[ean] = product
            except OpenGtinException as e:
                print(e)
        return product.name

    def add_item(self, item_name: str):
        self.pantry.add(item_name)

    def start(self):
        while True:
            print("Waiting for EAN input...")
            ean = int(input())
            product_name = self.barcode_to_product_name(ean)
            if product_name:
                self.add_item(product_name)
                print(f"Added {product_name} to the pantry.")
            else:
                self.add_item(str(ean))
                print(f"Could not find product name for {ean}. Added the EAN to the list instead.")


if __name__ == '__main__':
    pantry_sentry = PantrySentry()
    print("Starting the Pantry Sentry")
    pantry_sentry.start()
