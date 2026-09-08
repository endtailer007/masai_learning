orders = [
    {"order_id": "ORD1001", "customer_name": "Priya Sharma", "order_amount": 2500},
    {"order_id": "ORD1002", "customer_name": "Rahul Verma",  "order_amount": 1200},
    {"order_id": "ORD1003", "customer_name": "Ananya Iyer",  "order_amount": 4000},
    {"order_id": "ORD1004", "customer_name": "Karthik Rao",  "order_amount": 800},
    {"order_id": "ORD1005", "customer_name": "Meera Nair",   "order_amount": 3200},
]

# 1. Tool schema definition
process_refund_schema = {
    "name": "process_refund",
    "description": "Processes a refund for a given order if the amount is valid.",
    "parameters": {
        "order_id": {"type": "string", "required": True},
        "amount": {"type": "number", "required": True},
    },
}

# 2. Mock decision function (stands in for a real paid LLM call)
def mock_llm_decide(user_query, call_counter=[0]):
    call_counter[0] += 1
    return {
        "finish_reason": "tool_calls",
        "tool_name": "process_refund",
        "arguments": {"order_id": "ORD1001", "amount": 2500},
        "tool_call_id": "call_abc123",  # same id simulates a retry
    }

# 3. Execution function with business-logic validation, instrumented with an
#    explicit execution counter so a duplicate-processing claim can be proven, not just asserted
refund_execution_count = 0

def process_refund(order_id, amount):
    global refund_execution_count
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if order is None:
        return {"status": "failed", "reason": "unknown order_id"}
    if amount <= 0:
        return {"status": "failed", "reason": "amount must be positive"}
    if amount > order["order_amount"]:
        return {"status": "failed", "reason": "amount exceeds original order amount"}
    refund_execution_count += 1  # only increments on the validated success path
    return {"status": "success", "order_id": order_id, "refunded_amount": amount}

# 4. Idempotency layer keyed by tool_call_id
_processed_calls = {}

def call_tool_idempotent(tool_call_id, order_id, amount):
    if tool_call_id in _processed_calls:
        print(f"Duplicate tool_call_id {tool_call_id} detected - returning cached result, no refund re-processed.")
        return _processed_calls[tool_call_id]
    result = process_refund(order_id, amount)
    _processed_calls[tool_call_id] = result
    return result

# 5. Demonstrate idempotency across a retry
decision = mock_llm_decide("Please refund my order ORD1001")
first_call = call_tool_idempotent(decision["tool_call_id"], decision["arguments"]["order_id"], decision["arguments"]["amount"])
second_call = call_tool_idempotent(decision["tool_call_id"], decision["arguments"]["order_id"], decision["arguments"]["amount"])

print("First call result:", first_call)
print("Second call result:", second_call)

# Explicit proof: both calls agree AND the side effect only actually ran once
assert first_call == second_call
assert refund_execution_count == 1
print("Refund processed exactly once:", first_call == second_call, "| execution count:", refund_execution_count)
