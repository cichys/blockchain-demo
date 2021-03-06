import time

from classes.Block import Block
from classes.DataFiles import DataFiles
from config.config import CONFIG


class Blockchain:

    def __init__(self):
        self.unconfirmed_transactions = [] # data yet to get into blockchain
        self.chain = []
        self.wallets = set()
        self.create_genesis_block()
        self.data_files = DataFiles()


    @property
    def last_block(self):
        return self.chain[-1]


    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)


    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * CONFIG['DIFFICULTY']):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash


    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True


    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * CONFIG['DIFFICULTY']) and
                block_hash == block.compute_hash())


    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)


    def mine(self, network):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        # announce it to the network
        network.announce_new_block(new_block)
        self.data_files.update_chain(self.chain)
        return new_block.index


    def add_new_wallet(self, wallet, network):
        """
        Add a new wallet on the blockchain and announce to the network
        """
        self.wallets.add(wallet)
        network.announce_new_wallet(wallet)
        self.data_files.update_wallets(self.wallets)
        return True


    def check_wallet_exists(self, name):
        """
        Check if wallet exists in the blockchain
        """
        for wallet in self.wallets:
            if name == wallet.name:
                return True
        return False


    def check_wallet_balance(self, name, amount):
        """
        Check if wallet has enough amount to complete the transaction
        """
        for wallet in self.wallets:
            if name == wallet.name:
                return wallet.balance >= amount
        return False

