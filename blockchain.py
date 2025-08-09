# Libraries
from Crypto.Hash import SHA256
import json
from time import time
from uuid import uuid4


class Blockchain:
    def __init__(self):
        self.chain = []
        self.currentTransaction = []
        # Create A New Genesis Block
        self.newBlock(previousHash='1', proof=100)

    def newBlock(self, proof, previousHash=None):
        """
        Creates A New Block And Adds It To The Chain
        
        :param proof: <int> The Proof Given By The Proof of Work Algorithm
        :param previousHash: (Optional) <str> Hash of Previous Block
        :return: <dict> New Block"""
        
        block = {
            'Index': len(self.chain) + 1,
            'Timestamp': time(),
            'Transactions': self.currentTransaction, 
            'Proof': proof,
            'Previous Hash': previousHash or self.hash(self.chain[-1]) if self.chain else '1'
        }
        # Reset The Current List of Transactions
        self.currentTransaction = []
        self.chain.append(block)
        return block

    def newTransaction(self, sender, recipient, amount):
        """
        Adds A New Transaction To The List of Transactions
        
        Creates A New Transaction To Go Into The Next Mined Block

        :param sender: <str> Address of The Sender
        :param recipient: <str> Address of The Recipient
        :param amount: <int> Amount
        :return: <int> The Index of The Block That Will Hold This Transaction
        """
        
        self.currentTransaction.append({
            'Sender': sender,
            'Recipient': recipient,
            'Amount': amount,
        })

        return self.lastBlock['Index'] + 1 if self.chain else 1

    @staticmethod
    def hash(block):
        """
        Creates A SHA-256 Hash of Block
        :param block: <dict> Block
        :return: <str>
        """
        blockString = json.dumps(block, sort_keys=True).encode()
        return SHA256.new(data=blockString).hexdigest()

    @property
    def lastBlock(self):
        """
        Returns The Last Block In The Chain
        """
        if not self.chain:
            return None  # In Case The Chain Is Empty
        return self.chain[-1]
