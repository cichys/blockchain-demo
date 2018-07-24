import json


class DataFiles:

    def __init__(self):
        chain_file = open("data/chain.json", "w")
        chain_file.write("{}")
        chain_file.close() 
        wallets_file = open("data/wallets.json", "w")
        wallets_file.write("{}")
        wallets_file.close() 



    def update_chain(self, chain):
        list_for_json = []
        for block in chain:
            list_for_json.append(block.__dict__)

        chain_file = open("data/chain.json", "w")
        chain_file.write(json.dumps(list_for_json))
        chain_file.close()



    def update_wallets(self, wallets):
        list_for_json = []
        for wallet in wallets:
            list_for_json.append(wallet.__dict__)

        chain_file = open("data/wallets.json", "w")
        chain_file.write(json.dumps(list_for_json))
        chain_file.close()

