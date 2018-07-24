class Network:

    def __init__(self):
        # the address to other participating members of the network
        self.peers = set()


    def consensus(self, blockchain):
        """
        Our simple consensus algorithm. If a longer valid chain is found, our chain is replaced with it.
        """

        longest_chain = None
        current_len = len(blockchain.chain)

        for node in self.peers:
            response = requests.get('http://{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            if length > current_len and blockchain.check_chain_validity(chain):
                current_len = length
                longest_chain = chain
    
        if longest_chain:
            blockchain = longest_chain
            return True

        return False


    def announce_new_block(self, block):
        """
        A function to announce to the network once a block has been mined.
        Other blocks can simply verify the proof of work and add it to their
        respective chains.
        """
        for peer in self.peers:
            url = "http://{}/add_block".format(peer)
            requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))

