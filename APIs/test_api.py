from flask import make_response, jsonify
from flask_restful import Resource

from models import BankAccount, BASchema, parser


testData = [BankAccount(
    accountID=1, accountName='Abraham', accountWallet=52.6)]

class TestWithoutID(Resource):
    bankSchema = BASchema(many=True)

    def get(self):
        res = self.bankSchema.dump(testData)
        return make_response(jsonify(res), 200)

    def post(self):
        args = parser.parse_args()

        if args['accountName'] is None or args['accountWallet'] is None:
            return make_response(jsonify({'message': 'Invalid parameters'}), 400)

        bankAccount = BankAccount(
            accountName=args['accountName'], accountWallet=args['accountWallet'])
        

        if len(testData) == 0:
            bankAccount.accountID = 1
        else:
            bankAccount.accountID = testData[-1].accountID + 1

        res = self.bankSchema.dump([bankAccount])

        testData.append(bankAccount)
        return make_response(jsonify(res[0]), 201)

    def delete(self):
        if len(testData)>0:
            res = self.bankSchema.dump(testData)
            testData.clear()
            return make_response(jsonify(res), 200)
        else:
            res=[[]]
            return make_response(jsonify(res[0]), 200)


class TestWithID(Resource):
    bankSchema = BASchema()

    @classmethod
    def put_helper(cls, elem: BankAccount, args: dict) -> BankAccount:
        elem.accountName = args['accountName'] if (
            args['accountName'] is not None) else elem.accountName
        elem.accountWallet = args['accountWallet'] if (
            args['accountWallet'] is not None) else elem.accountWallet

        return elem

    def get(self, id: int):
        for elem in testData:
            if elem.accountID == id:
                res = self.bankSchema.dump(elem)
                return make_response(jsonify(res), 200)
        return make_response(jsonify({'message': f'Index {id} not found'}), 404)

    def put(self, id: int):
        args = parser.parse_args()

        for elem in testData:
            if elem.accountID == id:
                elem = self.put_helper(elem, args)
                res = self.bankSchema.dump(elem)
                return make_response(jsonify(res), 200)

        return make_response(jsonify({'message': f'Index {id} not found'}), 404)

    def delete(self, id: int):
        for i in range(0, len(testData), 1):
            if testData[i].accountID == id:
                elem = testData.pop(i)
                res = self.bankSchema.dump(elem)
                return make_response(jsonify(res), 200)

        return make_response(jsonify({'message': f'Index {id} not found'}), 404)
