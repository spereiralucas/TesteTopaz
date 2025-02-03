from app import app
from app.utils.validator import validate
from flask import jsonify, make_response, request
from app.controllers.customerController import CustomerController


add_customer_schema = {
    'name': {'type': 'string', 'required': True, 'empty': False},
    'age': {'type': 'integer', 'required': True, 'empty': False}
}


@app.route('/api/customer/<int:agency>/<int:account>', methods=['PUT'])
@validate(add_customer_schema)
def get_customer(agency, account):
    """
    Esta rota retorna uma mensagem informando se a conta foi ou não criada.
    ---
    tags:
      - New Account
    consumes:
      - application/json
    parameters:
      - name: agency
        in: path
        type: string
        required: true
        description: Código da agência bancária
        example: "1234"
      - name: account
        in: path
        type: string
        required: true
        description: Número da conta do cliente
        example: "567890"
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Fulano"
            age:
              type: integer,
              example: 35

    responses:
      201:
        description: Created
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Created"
            response:
              type: integer
              example: 201
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            errors:
              type: dict
              example: "{'age': ['must be of integer type']"
            message:
              type: string
              example: "Bad request was sent"
            response:
              type: integer
              example: 400

      409:
        description: Conflict
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Account already exists"
            response:
              type: integer
              example: 409
    """

    data = request.get_json()

    data['agency'] = agency
    data['account'] = account

    response = CustomerController().get_account(data)
    result = jsonify(response)
    result.status_code = response['response']

    return make_response(result)


@app.route('/api/customer/<int:agency>/<int:account>', methods=['GET'])
def list_customer_info(agency, account):
    """
    Esta rota retorna informações da conta e os ultimos 5 registros de transações
    ---
    tags:
      - Balance
    consumes:
      - application/json
    parameters:
      - name: agency
        in: path
        type: string
        required: true
        description: Código da agência bancária
        example: "1234"
      - name: account
        in: path
        type: string
        required: true
        description: Número da conta do cliente
        example: "567890"

    responses:
      200:
        description: Sucesso
        schema:
          type: object
          properties:
            balance:
              type: float
              example: -23.0
            idade:
              type: integer
              example: 45
            last_transactions:
              type: array
              items:
                type: object
                properties:
                  agencia:
                    type: integer
                    example: 4321
                  conta:
                    type: integer
                    example: 1234
                  suspect:
                    type: boolean
                    example: true
                  type:
                    type: string
                    example: "credit"
                  valor:
                    type: float
                    example: 30.0
            nome:
              type: string
              example: "Beltrano"

      404:
        description: Not Found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Account not found"
            response:
              type: integer
              example: 404
    """
    response = CustomerController().list_customer_info(agency, account)
    result = jsonify(response)
    result.status_code = response['response']

    return make_response(result)
