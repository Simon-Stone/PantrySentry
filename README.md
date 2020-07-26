# PantrySentry
The PantrySentry is a program written in Python 3 that keeps track of the items in your pantry.

# Usage:
Set up your user data.
First run the following lines through the Python interpreter (replacing your personal information):
```python
import keyring
keyring.set_password("Google Keep", "your-username", "your-google-keep-password")
```
Then create a file ``userdata.py`` and place it in the ``PantrySentry`` root directory. The file needs to define two variables as follows:
```python
openGTIN_user_id = your_openGTIN_user_id
google_keep_username = your_Google_Keep_user_id
```
You can obtain a user ID for the Open GTIN database [here](https://opengtindb.org/).


Start the script ``PantrySentry.py``
Add to pantry:
- Use the keyboard or a barcode scanner to enter the [EAN](https://en.wikipedia.org/wiki/International_Article_Number) of the item you want to process.

Remove from pantry:
- Use the barcode in switch_direction.gif to switch to "remove" mode. Everything scanned in the next minute will be removed from the pantry.
