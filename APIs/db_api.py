from flask import make_response, jsonify
from flask_restful import Resource

from models import BankAccount, BASchema, parser, db


class BankWithoutID(Resource):
    bankSchema = BASchema(many=True)

    def get(self):
        res = self.bankSchema.dump(BankAccount.query.all())
        return make_response(jsonify(res), 200)

    def post(self):
        args = parser.parse_args()

        if args['accountName'] is None or args['accountWallet'] is None:
            return make_response(jsonify({'message': 'Invalid parameters'}), 400)
            
        bankAccount = BankAccount(
            accountName=args['accountName'], accountWallet=args['accountWallet'])

        db.session.add(bankAccount)
        db.session.commit()

        res = BankAccount.query.all()[-1]
        res = self.bankSchema.dump([res])
        return make_response(jsonify(res[0]), 201)

    def delete(self):
        res = BankAccount.query.all()
        for elem in res:
            db.session.delete(elem)
            db.session.commit()
        res = self.bankSchema.dump(res)
        return make_response(jsonify(res), 200)


class BankWithID(Resource):
    bankSchema = BASchema()

    @classmethod
    def put_helper(cls, elem: BankAccount, args: dict) -> BankAccount:
        elem.accountName = args['accountName'] if (
            args['accountName'] is not None) else elem.accountName
        elem.accountWallet = args['accountWallet'] if (
            args['accountWallet'] is not None) else elem.accountWallet

        return elem

    def get(self, id: int):
        res = BankAccount.query.filter_by(accountID=id).first()
        if res is not None:
            res = self.bankSchema.dump(res)
            return make_response(jsonify(res), 200)
        return make_response(jsonify({'message': f'Index {id} not found'}), 404)

    def put(self, id: int):
        args = parser.parse_args()

        elem = BankAccount.query.filter_by(accountID=id).first()
        if elem is not None:
            elem = self.put_helper(elem, args)
            res = self.bankSchema.dump(elem)
            db.session.commit()
            return make_response(jsonify(res), 200)

        return make_response(jsonify({'message': f'Index {id} not found'}), 404)

    def delete(self, id: int):
        elem = BankAccount.query.filter_by(accountID=id).first()
        if elem is not None:
            db.session.delete(elem)
            db.session.commit()
            res = self.bankSchema.dump(elem)
            return make_response(jsonify(res), 200)

        return make_response(jsonify({'message': f'Index {id} not found'}), 404)
