class Wallet:

    def __init__(self, data):
        self.name = data["name"]
        self.timestamp = data["timestamp"]
        self.balance = 0