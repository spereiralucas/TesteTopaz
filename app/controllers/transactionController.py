from app.models.transaction import ChannelEnum, TypeEnum
from app.utils.elasticConn import elastic_conn
from app.models.customer import Customer
from datetime import datetime, timedelta
from elasticsearch_dsl import Search, Q
from sqlalchemy import or_
from app import db


class TransactionController():
    def __init__(self):
        super().__init__()
        self.db = db.session
        self.els = elastic_conn()

    def get_transaction(self, request):
        try:
            customers = self.db.query(Customer).filter(
                or_((
                    Customer.account == request['origin_account']) & (
                    Customer.agency == request['origin_agency']), (
                    Customer.account == request['dest_account']) & (
                    Customer.agency == request['dest_agency']
                ))
            ).all()

            if customers.__len__() < 2:
                return {
                    'response': 404,
                    'message': 'Account not found'
                }

            else:
                date_hour = datetime.strptime(request['date_hour'], '%d%m%Y%H%M')
                channel = ChannelEnum(request['channel']).name

                is_valid = self.rules(date_hour, channel, request)

                new_transaction = {
                    'date_hour': date_hour,
                    'value': request['value'],
                    'channel': channel,
                    'suspect': is_valid['suspect'],
                    'agency_orig': request['origin_agency'],
                    'account_orig': request['origin_account'],
                    'agency_dest': request['dest_agency'],
                    'account_dest': request['dest_account']
                }

                if is_valid:
                    self.els.index(index='transaction', body=new_transaction)

                return is_valid

        except Exception:
            pass

    def rules(self, date_hour, channel, request):
        one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
        search = Search(using=self.els, index='transaction')\
            .filter('range', date_hour={'gt': one_hour_ago})\
            .filter(
                Q('match', account_orig=request['origin_account']) &
                Q('match', account_dest=request['dest_account']) &
                Q('match', agency_orig=request['origin_agency']) &
                Q('match', agency_dest=request['dest_agency'])
            ).filter(
                'range', value={'gte': request['value'] * 0.5, 'lte': request['value'] * 1.5}
            )

        if (date_hour.hour < 10 or date_hour.hour > 16) and channel == 'Teller':
            return {
                'response': 400,
                'suspect': True,
                'reason': f'Invalid interval on {channel}'
            }

        if request['value'] > 500 and (date_hour.hour >= 0 and date_hour.hour <= 6):
            return {
                'response': 400,
                'suspect': True,
                'reason': 'Incompatible hour and value'
            }

        if search.execute().hits.total.value != 0:
            return {
                'response': 400,
                'suspect': True,
                'reason': 'Multiples similar transactions on period'
            }

        if ChannelEnum(request['channel']).name == ('InternetBanking' or 'MobileBanking'):
            age = self.db.query(Customer.age)\
                .filter_by(agency=request['origin_agency'])\
                .filter_by(account=request['origin_account'])\
                .first()

            if age[0] >= 60 and (date_hour.hour < 7 and date_hour.hour >= 23) and request['value'] >= 500:
                return {
                    'response': 400,
                    'suspect': True,
                    'reason': 'Profile Incompatible with this action'
                }

        if request['value'] >= 2000:
            search = Search(using=self.els, index='transaction')\
                .filter(
                    Q('match', account_orig=request['origin_account']) &
                    Q('match', account_dest=request['dest_account']) &
                    Q('match', agency_orig=request['origin_agency']) &
                    Q('match', agency_dest=request['dest_agency'])
                )

            if search.execute().hits.total.value == 0:
                return {
                    'response': 400,
                    'suspect': True,
                    'reason': 'High value to unusual destiny'
                }

        else:
            return {
                'response': 201,
                'suspect': False
            }
