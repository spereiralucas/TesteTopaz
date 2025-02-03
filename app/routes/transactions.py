from app import app
from app.utils.validator import validate
from flask import jsonify, make_response, request
from app.controllers.transactionController import TransactionController


new_transaction_schema = {
    'date_hour': {'required': True, 'empty': False, 'regex': r'^\d{2}\d{2}\d{4}\d{2}\d{2}$'},
    'value': {'type': 'float', 'required': True, 'empty': False},
    'channel': {'type': 'integer', 'required': True, 'empty': False, 'allowed': [0, 1, 2, 3]},
    'origin_agency': {'type': 'integer', 'required': True, 'empty': False},
    'origin_account': {'type': 'integer', 'required': True, 'empty': False},
    'dest_agency': {'type': 'integer', 'required': True, 'empty': False},
    'dest_account': {'type': 'integer', 'required': True, 'empty': False}
}


@app.route('/api/transaction/create', methods=['PUT'])
@validate(new_transaction_schema)
def create_transaction():
    """
    Esta rota retorna uma mensagem informando se a transação é ou não considerada suspeita.
    ---
    tags:
      - New Transaction
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            date_hour:
              type: string
              example: "040220250821"
            value:
              type: float,
              example: 12.50
            channel:
              type: integer
              example: 2
            origin_agency:
              type: integer,
              example: 1234
            origin_account:
              type: integer
              example: 43210
            dest_agency:
              type: integer,
              example: 6789
            dest_account:
              type: integer,
              example: 98760

    responses:
      201:
        description: Created
        schema:
          type: object
          properties:
            suspect:
              type: boolean
              example: False
            response:
              type: integer
              example: 201

      400:
        description: Bad Request
        schema:
          type: object
          properties:
            reason:
              type: string
              example: "Multiples similar transactions on period"
            response:
              type: integer
              example: 400
            suspect:
              type: boolean
              example: True
    """

    data = request.get_json()
    response = TransactionController().get_transaction(data)
    result = jsonify(response)
    result.status_code = response['response']

    return make_response(result)
