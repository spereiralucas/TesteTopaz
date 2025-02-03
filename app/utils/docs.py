create_account_doc = """
    Esta rota retorna uma mensagem informando se a conta foi ou não criada..
    ---
    tags:
      - New Account
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            agencia:
              type: integer
              example: 1234
            conta:
              type: integer
              example: 5678
            nome:
              type: string
              example: "Fulano"
            idade:
              type: integer,
              example: 35

    responses:
      201:
        description: Created
      400:
        description: Bad Request
      409:
        description: Conflict
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Olá, mundo!"
    """
