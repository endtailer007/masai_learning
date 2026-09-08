import pandas as pd
import json
processed_orders = {}

def process_order_requests(requests):
    """
    Process a list of order requests, applying request_id-based idempotency
    and quantity validation, returning one structured result per request
    in the same order as the input.
    """
    results = []
    for req in requests:
        # TODO: validate that req["quantity"] is an int strictly greater than 0;
        # if invalid, append an error result and continue without storing anything
        if req['quantity']<= 0:
            results.append(f"Error: Invalid quantity {req['quantity']}, must be greater than 0 for request_id {req['request_id']}")

        # TODO: if req["request_id"] is already in processed_orders, append a
        # "already processed, duplicate tool call" success result using the
        # previously stored order, and continue
        elif req['request_id'] in processed_orders:
            results.append(f"Status: Success, already processed, duplicate tool call, order identical to result request_id {req['request_id']}")

        # TODO: otherwise build and store the new order keyed by request_id,
        # then append a success result containing it
        else:
            order = {
                "request_id": req["request_id"],
                "product": req["product"],
                "quantity": req["quantity"]
            }
            processed_orders[req["request_id"]] = order
            results.append(f"Status: Success, order processed, order: {req}")
    return results

if __name__ == "__main__":
    with open("order_requests.json",'r') as f:
       data=json.load(f)
    sample_requests = list(data)
    result = process_order_requests(sample_requests)
    for res in result:
            print(res)

    print(len(result))
