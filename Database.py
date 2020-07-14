import sqlite3
from collections import namedtuple


class Database:
    """
    The EAN database
    This class essentially wraps various SQLite commands and queries
    """
    Product = namedtuple('Product', ['ean', 'name', 'description'])

    def __init__(self, file_name: str):
        try:
            self.ean_db = sqlite3.connect(file_name)
            self.cursor = self.ean_db.cursor()
            self.cursor.execute('''CREATE TABLE ean_db 
            (ean integer primary key, product_name, product_description)''')
        except sqlite3.OperationalError:
            print("Existing database found.")

    def add_product(self, product: Product):
        """ Add a product to the database """
        self.cursor.execute('INSERT INTO ean_db (ean, product_name, product_description) '
                            'VALUES (?, ?, ?)', (product.ean, product.name, product.description))
        self.ean_db.commit()

    def get_product(self, ean: int):
        """ Get a product based on the EAN """
        name = self.cursor.execute('SELECT product_name FROM ean_db WHERE ean = ?', (ean,)).fetchone()
        if name:
            name = name[0]
        description = self.cursor.execute('SELECT product_description FROM ean_db WHERE ean = ?', (ean,)).fetchone()
        if description:
            description = description[0]
        return Database.Product(ean, name, description)

    def __getitem__(self, ean: int):
        """ Allow convenient access to database using ean in brackets """
        return self.get_product(ean)

    def __setitem__(self, ean, product: tuple):
        """ Allow convenient access to database using ean in brackets """
        self.add_product(Database.Product(ean=ean, name=product[1], description=product[2]))

    def __del__(self):
        self.ean_db.close()


if __name__ == '__main__':
    db = Database('ean.db')
    db[1] = ('Yay', 'Really yay')
    print(db[1234])
