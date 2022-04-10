import base64

from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction

# paste your wallets mnemonic keys and wallet
sender_private_key, sender_address = mnemonic.to_private_key("key1 key2 key3.."), "YOUR-WALLET-CODE"

#paste assets creator wallet 
close_assets_to = "ASSETS-CREATOR-ADDRESS-HERE" 

_, receiver = sender_private_key, sender_address
amount = 0  # The amount of how many of the asset will be transferred. It should be 0 for opt-out.

index = "609428783" # index of the asset 

def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo

algod_address = "https://api.algoexplorer.io"
algod_token = ""
headers = {'User-Agent': 'py-algorand-sdk'}
algod_client = algod.AlgodClient(algod_token, algod_address, headers);    

params = algod_client.suggested_params()

# # create the opt-out transaction
txn = transaction.AssetTransferTxn(
    sender_address, params, receiver, amount, index, close_assets_to, None, None, None,None 
)

# sign the transaction
signed_txn = txn.sign(sender_private_key)

# send the transaction
try:
    tx_confirm = algod_client.send_transaction(signed_txn)
    print('Transaction sent with ID', signed_txn.transaction.get_txid())
    wait_for_confirmation(algod_client, txid=signed_txn.transaction.get_txid())
except Exception as e:
    print(e)