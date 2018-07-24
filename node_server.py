import time
import json
from flask import Flask, request
import requests

from classes.Blockchain import Blockchain
from classes.Network import Network


app =  Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()

network = Network()



# endpoint to submit a new transaction. This will be used by
# our application to add new data (posts) to the blockchain
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]
 
    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404
 
    tx_data["timestamp"] = time.time()
    blockchain.add_new_transaction(tx_data)

    return "Success", 201


# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
@app.route('/chain', methods=['GET'])
def get_chain():
    # make sure we've the longest chain
    network.consensus(blockchain)
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    return json.dumps({
        "length": len(chain_data),
        "chain": chain_data
    })


# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine(network)
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined.".format(result)


# endpoint to query unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


# endpoint to add new peers to the network.
@app.route('/add_nodes', methods=['POST'])
def register_new_peers():
    nodes = request.get_json()
    if not nodes:
        return "Invalid data", 400
    for node in nodes:
        network.peers.add(node)

    return "Success", 201


@app.route('/get_nodes', methods=['GET'])
def get_registered_nodes():
    list_peers = [] #because peers is a set
    for peer in network.peers:
        list_peers.append(peer)
    return json.dumps(list_peers)


# endpoint to add a block mined by someone else to the node's chain. 
# The block is first verified by the node and then added to the chain.
@app.route('/add_block', methods=['POST'])
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"], block_data["transactions"],
                  block_data["timestamp", block_data["previous_hash"]])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201




app.run(debug=True, port=8000)
