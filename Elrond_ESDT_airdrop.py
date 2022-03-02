import binascii

# You'll need Erdpy librarie. Go to Elrond docs to get set up with Erdpy
from erdpy.accounts import Account
from erdpy.proxy import ElrondProxy
from erdpy.transactions import Transaction



# Change here the token decimals and the token Id
TOKEN_DECIMALS = 1000000000000000000 # 10^18 (18 decimals)
TOKEN_ID = "GOLDEN-335e6d" 


def text_to_hex(text) :
    return binascii.hexlify(text.encode()).decode()

# Sometimes need to add a 0 (if it's even, to be sure that is grouped by bytes)
def num_to_hex(num) : 
    hexa = format(num, "x")
    if len(hexa)%2==1 :  
        return "0" + hexa
    return hexa


# Convert to a bigUint (adding the decimals)
def int_to_BigInt(num, decimals) : 
    return int(f"{num*decimals:.1f}".split(".")[0])         
     


def sendESDT(owner, receiver, token_id, amount, decimals):  

    payload = "ESDTTransfer@" + text_to_hex(token_id) + "@" + num_to_hex(int_to_BigInt(amount, decimals))
            
    tx = Transaction()
    tx.nonce = owner.nonce
    tx.value = "0"
    tx.sender = owner.address.bech32()
    tx.receiver = receiver.address.bech32()
    tx.gasPrice = gas_price
    tx.gasLimit = 500000 # 500k is standard for an ESDT transfer as of today
    tx.data = payload
    tx.chainID = chain
    tx.version = tx_version

    tx.sign(owner)
    tx_hash = tx.send(proxy)
    owner.nonce+=1
    return tx_hash   




         

proxy_address = "https://gateway.elrond.com"
proxy = ElrondProxy(proxy_address)
network = proxy.get_network_config()
chain = network.chain_id
gas_price = network.min_gas_price
tx_version = network.min_tx_version



# The owner of the tokens, that will send them
# You'll need a pem file. If you don't you should derive one following Elrond's tutos
owner = Account(pem_file="wallet_owner.pem")
owner.sync_nonce(proxy)


# All addresses should be in a file (one address per line)
# If the file is formatted in another way, you should parse it differently
# Note : set() avoid address duplicates
for address in list(set(open("addresses.txt").read().split("\n"))) : 
    sendESDT(owner, Account(address), TOKEN_ID, 100, TOKEN_DECIMALS)


  
