from app.utils.elasticConn import elastic_conn
from app.models.customer import Customer
from elasticsearch_dsl import Search, Q
from app import db


class CustomerController():
    def __init__(self):
        super().__init__()
        self.db = db.session
        self.els = elastic_conn()

    def get_account(self, request):
        try:
            query = self.db.query(Customer)\
                .filter_by(account=request['account'])\
                .filter_by(agency=request['agency']).first()

            if not query:
                new_customer = Customer(
                    name=request['name'],
                    age=request['age'],
                    account=request['account'],
                    agency=request['agency']
                )

                self.db.add(new_customer)
                self.db.commit()

                response = {
                    'response': 201,
                    'message': 'Created'
                }
            else:
                response = {
                    'response': 409,
                    'message': 'Account already exists'
                }

        except Exception as e:
            response = {
                'response': 400,
                'message': f'Bad Request: {e}'
            }

        finally:
            return response

    def list_customer_info(self, agency, account):
        transactions = []
        try:
            query = self.db.query(Customer)\
                .filter_by(account=account)\
                .filter_by(agency=agency).first()

            if query:
                search = (Search(using=self.els, index='transaction')\
                    .query(
                        Q("bool", should=[
                            Q("bool", must=[
                                Q("match", account_orig=account),
                                Q("match", agency_orig=agency)]),
                            Q("bool", must=[
                                Q("match", account_dest=account),
                                Q("match", agency_dest=agency)]
                            )
                        ], minimum_should_match=1)
                    ).sort("-date_hour").extra(size=5)
                )

                result = {}
                balance = 0
                for item in search.execute():
                    if query.agency == item['agency_orig'] and query.account == item['account_orig']:
                        type_ = 'credit'
                        balance = balance + (item['value'] * -1)
                    elif query.agency == item['agency_dest'] and query.account == item['account_dest']:
                        type_ = 'debit'
                        balance = balance + item['value']

                    result = {
                        'agencia': query.agency,
                        'conta': query.account,
                        'type': type_,
                        'valor': item['value'],
                        'suspect': item['suspect']
                    }

                    transactions.append(result)

                return {
                    'nome': query.name,
                    'idade': query.age,
                    'last_transactions': transactions,
                    'balance': balance,
                    'response': 200
                }
            else:
                return {
                    'response': 404,
                    'message': 'Account not found'
                }

        except Exception as e:
            return {
                'response': 400,
                'message': f'Bad Request: {e}'
            }
        finally:
            self.els.close()
