import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Створення блоку генезису, де previous_hash - прізвище, а proof (nounce) - день,
        # місяць та рік народження.

        self.new_block("butsykin")

    def new_block(self, previous_hash=None):
        block = self.proof_of_work(previous_hash)

        self.add_block(block)

        return block

    def add_block(self, block):
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def first_block(self):
        return self.chain[0]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': 4112002,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        while self.valid_proof(block) is False:
            block['proof'] += 1

        return block

    def valid_proof(self, block):
        # У якості підтвердження доказу перевіримо на наявність місяць народження у кінці хешу
        return self.hash(block)[len(self.hash(block))-2:] == "11"



# Ствоюємо новий блокчейн:
blockchain = Blockchain()

# Створюємо новий блок:
block = blockchain.new_block()

print()
print("----------")
print("Block 0")
print("Previous hash:", blockchain.first_block["previous_hash"])
print("New hash: ", blockchain.hash(blockchain.first_block))
print("----------")
print()
print("----------")
print("Block 1")
print("Previous hash:", block["previous_hash"])
print("New hash: ", blockchain.hash(block))
print("----------")

block = blockchain.new_block()

print()
print("----------")
print("Block 2")
print("Previous hash:", block["previous_hash"])
print("New hash: ", blockchain.hash(block))
print("----------")