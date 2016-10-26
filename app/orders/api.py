from flask import request, Response, jsonify

from app.orders import orders


@orders.route('/orders', methods=['POST'])
def place_order():
    """Place an order """

    data = request.get_json(force=True)

    data['id'] = "123456789"
    resp = jsonify(data)
    resp.status_code = 201
    return resp


@orders.route('/orders/<id>', methods=['GET'])
def get_order(id):
    """Get an order"""

    if id != "123456789":
        return Response(status=404)

    data = {"name": "abc", "id": id, "amount": 3}
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@orders.route('/orders/<id>', methods=['PATCH'])
def update_order(id):
    """Update an order"""

    if id != "123456789":
        return Response(status=404)

    data = request.get_json(force=True)

    order = {"name": "abc", "id": id, "amount": 3}
    for key, value in data.items():
        order[key] = value
    resp = jsonify(order)
    resp.status_code = 200
    return resp


@orders.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    """Delete an order"""

    if id != "123456789":
        return Response(status=404)

    return Response(status=204)
