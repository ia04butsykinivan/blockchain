import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Створення блоку генезису, де previous_hash - прізвище, а proof (nounce) - день,
        # місяць та рік народження.
        self.new_block(previous_hash="butsykin", proof=4112002)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            # 'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

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

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self):
        proof = 0

        while self.valid_proof(proof) is False:
            proof += 1

        return proof

    # Умова валідності nounce полягає в тому, що хеш блоку має закінчуватися значенням 11.
    # Для перевірки, створюємо новий блок та хешуємо його, але є проблема, що час змінюється
    # для наступних блоків
    def valid_proof(self, proof):
        block = self.new_block(proof)

        # У якості підтвердження доказу перевіримо на наявність місяць народження у кінці хешу
        return self.hash(block)[len(self.hash(block))-2:] == "11"



# Ствоюємо новий блокчейн:
blockchain = Blockchain()

proof = blockchain.proof_of_work()
block = blockchain.new_block(proof)

print()
print("----------")
print("Block 1")
print("Previous hash:", block["previous_hash"])
print("New hash: ", blockchain.hash(block))
print("----------")

proof = blockchain.proof_of_work()
block = blockchain.new_block(proof)

print()
print("----------")
print("Block 2")
print("Previous hash:", block["previous_hash"])
print("New hash: ", blockchain.hash(block))
print("----------")