import urllib.parse
from urllib.parse import urlparse
from ts3audiobot_api.commands import Playlist, History, User


def format_url(url):
    return urllib.parse.quote(url, safe='')


class CommandCaller:

    def __init__(self, ts3audiobot):
        """
        Init
        :param ts3audiobot:
        """
        self.ts3audiobot = ts3audiobot

    def play(self, link):
        """
        PLAY REQUESTED URL
        """

        # MAKE REQUEST
        print("play/{url}".format(url=format_url(link)))
        return self.ts3audiobot.request("play/{url}".format(url=format_url(link)))

    def pause(self):
        return self.ts3audiobot.request("pause")

    def unpause(self):
        return self.ts3audiobot.request("play")

    def get_song(self):
        return self.ts3audiobot.request("song")

    def set_volume(self, volume):
        if 0 >= volume <= 100:
            return self.ts3audiobot.request("volume/{int}".format(int=volume))
        else:
            return False

    def stop(self):
        return self.ts3audiobot.request("stop")

    def add_song(self, link):
        return self.ts3audiobot.request("add/{url}".format(url=format_url(link)))

    def enable_channel_commander(self):
        return self.ts3audiobot.request("bot/commander/on")

    def disable_channel_commander(self):
        return self.ts3audiobot.request("bot/commander/off")

    def come(self):
        return self.ts3audiobot.request("bot/come")

    def connect_via_template(self, template):
        return self.ts3audiobot.request("bot/connect/template/{template}".format(template=format_url(template)))

    def connect_new(self, ip):
        return self.ts3audiobot.request("bot/connect/to/{ip}".format(ip=format_url(ip)))

    def get_information(self):
        return self.ts3audiobot.request("bot/info")

    def get_bots(self):
        return self.ts3audiobot.request("bot/list")

    def move(self):
        return self.ts3audiobot.request("move")

    def set_name(self, name):
        return self.ts3audiobot.request("bot/name/{name}".format(name=format_url(name)))

    def get_badges(self):
        return self.ts3audiobot.request("bot/badges")

    def save_settings(self, template):
        return self.ts3audiobot.request("bot/save/{template}".format(template=format_url(template)))

    def setup(self):
        return self.ts3audiobot.request("bot/setup")

    def disconnect(self):
        return self.ts3audiobot.request("bot/disconnect")

    def use(self, bot_id):
        self.ts3audiobot.bot_id = bot_id

    def clear(self):
        return self.ts3audiobot.request("clear")

    def eval(self):
        return self.ts3audiobot.request("eval")

    def help(self):
        return self.ts3audiobot.request("help")

    def get_settings(self, value=None):

        if not value:
            return self.ts3audiobot.raw_request("settings")
        else:
            return self.ts3audiobot.raw_request("settings/get/{value}".format(value=format_url(value)))

    def set_settings(self, name, value):
        return self.ts3audiobot.raw_request("settings/set/{name}/{value}".format(name=format_url(name), value=format_url(value)))

    def get_bot_settings(self, template, name):
        return self.ts3audiobot.request("settings/bot/get/{template}/{name}".format(template=format_url(template), name=format_url(name)))

    def set_bot_settings(self, template, name, value):
        return self.ts3audiobot.request("settings/bot/set/{template}/{name}/{value}".format(template=format_url(template),
                                                                                            name=format_url(name),
                                                                                            value=format(value)))

    def get_global_settings(self, value):
        return self.ts3audiobot.raw_request("settings/global/get/{value}".format(value=format_url(value)))

    def set_global_settings(self, name, value):
        return self.ts3audiobot.raw_request("settings/global/set/{name}/{value}".format(name=format_url(name), value=format_url(value)))

    def init_playlist(self):
        return Playlist(self.ts3audiobot)

    def init_history(self):
        return History(self.ts3audiobot)

    def init_user(self):
        return User(self.ts3audiobot)