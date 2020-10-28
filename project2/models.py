import collections

class Message:
    def __init__(self, text, time, writer):
        self.text=text
        self.time=time
        self.writer=writer
    def __str__(self):
        return f"{self.writer}: {self.text}. ----{self.time}"



class Channel:
    def __init__(self, name, creater):
        self.name=name
        self.creater=creater
        self.message_history=collections.deque(maxlen=100)

    def send_message(self, m):
        self.message_history.append(m)


class User:
    def __init__(self, name):
        self.name=name
        self.created_channels = []

    def create_channel(self, c):
        self.created_channels.append(c)
