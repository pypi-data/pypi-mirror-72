from urllib.parse import urlparse


def is_url(link):
    """
    Check if link is valid
    """
    try:
        result = urlparse(link)
        if all([result.scheme, result.netloc]):
            return True
    except ValueError:
        return False


class Playlist:

    def __init__(self, ts3audiobot):
        self.ts3audiobot = ts3audiobot

    def add(self, link):
        if is_url(link):
            return self.ts3audiobot.request("list/add/{}".format(link))
        else:
            return False

    def clear(self):
        return self.ts3audiobot.request("list/clear")

    def delete(self):
        return self.ts3audiobot.request("delete")

    def get(self):
        return self.ts3audiobot.request("list/get")

    def item_move(self):
        return self.ts3audiobot.request("list/item/move")

    def item_delete(self):
        return self.ts3audiobot.request("list/item/delete")

    def list(self):
        return self.ts3audiobot.request("list/list")

    def load(self):
        return self.ts3audiobot.request("list/load")

    def merge(self):
        return self.ts3audiobot.request("list/merge")

    def rename(self):
        return self.ts3audiobot.request("list/name")

    def play(self):
        return self.ts3audiobot.request("list/play")

    def play_from(self, index):
        return self.ts3audiobot.request("list/play/{}".format(index))

    def get_queue(self):
        return self.ts3audiobot.request("list/queue")

    def save(self):
        return self.ts3audiobot.request("list/save")

    def show(self):
        return self.ts3audiobot.request("list/show")

    def random(self):
        return self.ts3audiobot.request("random")

    def enable_random(self):
        return self.ts3audiobot.request("random/on")

    def disable_random(self):
        return self.ts3audiobot.request("random/off")


class History:

    def __int__(self, ts3audiobot):
        self.ts3audiobot = ts3audiobot

    def add(self, id):
        return self.ts3audiobot.request("history/add/{id}".format(id=id))

    def clean(self, remove_defective=None):

        if not remove_defective:
            return self.ts3audiobot.request("history/clean")
        else:
            return self.ts3audiobot.request("history/clean/remove_defective")

    def delete(self, id):
        return self.ts3audiobot.request("history/delete/{id}".format(id=id))

    def history_form(self, count, userBDid):
        return self.ts3audiobot.request("history/from/{}/{}".format(count, userBDid))

    def history_id(self, id):
        return self.ts3audiobot.request("history/id/{}".format(id))

    def last(self, count):
        return self.ts3audiobot.request("history/last/{}".format(count))

    def play_last(self, count):
        return self.ts3audiobot.request("history/last/{}".format(count))

    def play(self, id):
        return self.ts3audiobot.request("history/play/{}".format(id))

    def rename(self, id, name):
        return self.ts3audiobot.request("history/rename/{}/{}".format(id, name))

    def till(self, date):
        return self.ts3audiobot.request("history/till/{}".format(date))

    def filter_titel(self, title):
        return self.ts3audiobot.request("history/title/{}".format(title))


class User:

    def __init(self, ts3audiobot):
        self.ts3audiobot = ts3audiobot

    def get_user_uid_by_id(self):
        return self.ts3audiobot.request("getuser/uid/byid")

    def get_username_by_id(self):
        return self.ts3audiobot.request("getuser/name/byid")

    def get_user_dbid_by_id(self):
        return self.ts3audiobot.request("getuser/dbid/byid")

    def get_user_channel_by_id(self):
        return self.ts3audiobot.request("getuser/channel/byid")

    def get_user_all_by_id(self):
        return self.ts3audiobot.request("getuser/all/byid")

    def get_user_id_by_name(self):
        return self.ts3audiobot.request("getuser/id/byname")

    def get_username_by_dbid(self):
        return self.ts3audiobot.request("getuser/name/bydbid")
   
