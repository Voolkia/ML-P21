from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from web3 import Web3
from eth_account import Account
import json
import binascii

from flask_cors import CORS

# Ganache GUI 
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

app = Flask(__name__)
# CORS ONLY FOR DEVELOPMENT
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

#FROM GANACHE GUI 
private_key = '4f7955aef258d9205866298e6ee1a034840a7813644c139457a145b6f387e001'
account = Account.privateKeyToAccount(private_key)

# CONTRACT config
CONTRACT_ADDR = '0x628606941742E688fac54aaA487a9448606E610f'
CONTRACT_ABI = json.loads("""[
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "previousOwner",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "newOwner",
          "type": "address"
        }
      ],
      "name": "OwnershipTransferred",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "string",
          "name": "_authors",
          "type": "string"
        },
        {
          "indexed": true,
          "internalType": "string",
          "name": "_title",
          "type": "string"
        }
      ],
      "name": "PaperStored",
      "type": "event"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "string",
          "name": "_username",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_password",
          "type": "string"
        }
      ],
      "name": "checkUserData",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "string",
          "name": "_username",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_lastName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_email",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_password",
          "type": "string"
        }
      ],
      "name": "createUser",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "isOwner",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [],
      "name": "renounceOwnership",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "address",
          "name": "newOwner",
          "type": "address"
        }
      ],
      "name": "transferOwnership",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_paperContent",
          "type": "bytes32"
        },
        {
          "internalType": "string",
          "name": "_issue",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_authors",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_title",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_username",
          "type": "string"
        }
      ],
      "name": "storePaper",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_idPaper",
          "type": "uint256"
        }
      ],
      "name": "getPaperById",
      "outputs": [
        {
          "internalType": "string",
          "name": "issue",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "authors",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "title",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "username",
          "type": "string"
        },
        {
          "internalType": "bytes32",
          "name": "content",
          "type": "bytes32"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_content",
          "type": "bytes32"
        }
      ],
      "name": "getPaperByContent",
      "outputs": [
        {
          "internalType": "string",
          "name": "issue",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "authors",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "title",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "username",
          "type": "string"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "papersCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getLastID",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    }
  ]""")
CONTRACT_INSTANCE = w3.eth.contract(address=CONTRACT_ADDR, abi=CONTRACT_ABI)

# parser = reqparse.RequestParser()

class PublicationList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user') # string
    parser.add_argument('content') # string
    parser.add_argument('vol') # string
    parser.add_argument('authors') # string
    parser.add_argument('title') # string
    #TODO: ADD PARSER FOR OTHER

    def get(self):
        count = CONTRACT_INSTANCE.functions.papersCount().call()
        publications = {}
        for id in range(count):
            [vol, author, title, user, content] = CONTRACT_INSTANCE.functions.getPaperById(id).call()
            publications[str(id)] = {
                "volume": vol, 
                "authors": author,
                "title": title,
                "user": user,
                "content_hash": str(binascii.hexlify(content))
            }
        return publications
    
    def post(self):
      # aca se guarda el paper 
      args = self.parser.parse_args()
      nonce = w3.eth.getTransactionCount(account.address)
      pm_txn = CONTRACT_INSTANCE.functions.storePaper(args.content, 
                                                      args.vol,
                                                      args.authors, 
                                                      args.title, 
                                                      args.user).buildTransaction({
                                                          "nonce": nonce,
                                                      })
      signed_txn = w3.eth.account.signTransaction(pm_txn, private_key=private_key)
      txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
      receipt = w3.eth.waitForTransactionReceipt(txn_hash)
      print(receipt)
      if(receipt.status) :
        code = 201
      else: 
        code = 409
      return {"receipt" : f'0x{str(binascii.hexlify(txn_hash))}'}, code

class Publication(Resource):
    def get(self, publication_id):
        [vol, author, title, user, content]\
             = CONTRACT_INSTANCE.functions.getPaperById(int(publication_id)).call()
        return {
            "volume": vol, 
            "authors": author,
            "title": title,
            "user": user,
            "content_hash": str(binascii.hexlify(content))
        }


class PaperByContent(Resource):
    def get(self, content):
        [vol, author, title, user] = \
            CONTRACT_INSTANCE.functions.getPaperByContent(content).call()
        return {
            "volume": vol, 
            "authors": author,
            "title": title,
            "user": user,
        }

class Count(Resource):
    def get(self):
        return {"count": CONTRACT_INSTANCE.functions.papersCount().call()}

##
## Actually setup the Api resource routing here
##
RESOURCES = [
  (PublicationList, '/publications'),
  (Publication, '/publications/<publication_id>'),
  (Count, '/publications/count'),
  (PaperByContent, '/publications/content/<content>'),
]

for resource,endpoint in RESOURCES:
  api.add_resource(resource, endpoint)


if __name__ == '__main__':
    app.run(debug=True)
