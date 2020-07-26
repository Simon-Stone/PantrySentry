import re

import gkeepapi


class ListManager:
    """
    This class wraps the Google Keep API
    """

    def __init__(self, user_name, password, list_name, backend='Google Keep'):
        if backend == 'Google Keep':
            print("Logging into Google Keep...", end="")
            self.api = gkeepapi.Keep()
            self.api.login(username=user_name, password=password)
            print("...done.")
            # Google Keep API returns a generator but we assume only the first returned note is the pantry inventory
            self.list = [p for p in self.api.find(query=list_name)][0]
        else:
            self.api = None

    def get_index(self, new_item: str):
        for idx, item in enumerate(self.list.items):
            if new_item in item.text:
                print(f"Found {new_item} on the list.")
                return idx
        return None

    def add(self, item: str):
        if isinstance(self.api, gkeepapi.Keep):
            item_idx = self.get_index(item)
            if item_idx is None:
                self.list.add(item, False)
            else:
                self.increase_count(item_idx)
            self.api.sync()
        else:
            raise ValueError("No way to add an item using the currently selected backend.")

    def increase_count(self, item_idx: int):
        regex = re.compile(r'x(?P<count>[0-9]+)')
        text = self.list.items[item_idx].text.split()
        if match := regex.match(text[-1]):
            #  If the last part of the item text is a count of the format 'xNUMBER'
            if self.list.items[item_idx].checked:
                # If the item was checked, the counter is reset to (implicit) 1
                text[-1] = ""
            else:
                # If the item was not checked, the counter is increased
                new_count = int(match.group('count')) + 1
                text[-1] = 'x' + str(new_count)
        else:
            # Otherwise add a counter of the same format (if it wasn't checked)
            if not self.list.items[item_idx].checked:
                new_count = 2
                text.append('x' + str(new_count))
        new_text = " ".join(text)
        self.list.items[item_idx].text = new_text
        self.list.items[item_idx].checked = False

    def remove(self, item: str):
        if isinstance(self.api, gkeepapi.Keep):
            item_idx = self.get_index(item)
            if item_idx is None:
                raise ValueError(f"Item {item} is not in the pantry!")
            else:
                self.decrease_count(item_idx)
            self.api.sync()
        else:
            raise ValueError("No way to remove an item using the currently selected backend.")

    def decrease_count(self, item_idx: int):
        if self.list.items[item_idx].checked:
            # If the item was checked, raise an error
            raise ValueError(f"Item {self.list.items[item_idx].text.rstrip()} was already checked!")
        regex = re.compile(r'x(?P<count>[0-9]+)')
        text = self.list.items[item_idx].text.split()
        if match := regex.match(text[-1]):
            #  If the last part of the item text is a count of the format 'xNUMBER'
            new_count = int(match.group('count')) - 1
            if new_count == 1:
                text[-1] = ""
            else:
                text[-1] = 'x' + str(new_count)
            new_text = " ".join(text)
            self.list.items[item_idx].text = new_text
            self.list.items[item_idx].checked = False
        else:
            # Otherwise (only one instance of the item present) check the item
            self.list.items[item_idx].checked = True


if __name__ == '__main__':
    import keyring
    import userdata

    lm = ListManager(userdata.google_keep_username, keyring.get_password('Google Keep', userdata.google_keep_username),
                     'Basement food')
    lm.add('Bananas')
