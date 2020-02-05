import hashlib

from timeit import default_timer as timer


def proof_of_work(last_proof):
    start = timer()

    print("Searching for next proof")
    proof = 0
    print('last_proof ---->', last_proof)
    while valid_proof(last_proof['proof'], proof, last_proof['difficulty']) is False:
        proof += 1
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof, diff):
    nash = hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest()
    return nash[:diff] == '0' * diff
