import hashlib
from urls import get, post, end

from timeit import default_timer as timer


def mine():
    while True:
        last_proof = get(end['lp'])
        next_proof = proof_of_work(last_proof)
        check_proof = post(end['mine'], {'proof': next_proof})
        if not len(check_proof['errors']):
            break


def proof_of_work(last_proof):
    start = timer()

    print('Searching for next proof')
    proof = last_proof['proof']
    while valid_proof(last_proof['proof'], proof, last_proof['difficulty']) is False:
        proof += 1
    print('Proof found: (' + str(proof) + ') in ' +
          str(round(timer() - start, 2)) + ' seconds.')
    return proof


def valid_proof(last_proof, proof, diff):
    nash = hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest()
    return nash[:diff] == '0' * diff
