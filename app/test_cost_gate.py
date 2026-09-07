from app.cost_gate import CostGate


gate = CostGate()


test_cases = [
    5,
    10,
    20,
    30,
    40,
    50,
    75,
    100,
    150,
    200
]


print("\n==============================")
print("COST MODEL V1 TEST")
print("==============================")


for tokens in test_cases:

    estimate = gate.estimate_savings(
        tokens
    )

    decision = gate.decision(
        tokens
    )

    print(
        f"\nTokens: {tokens}"
    )

    print(
        "Estimated compressed:",
        estimate["estimated_compressed_tokens"]
    )

    print(
        "Estimated saved:",
        estimate["estimated_saved_tokens"]
    )

    print(
        "Estimated net savings:",
        estimate["estimated_net_savings"]
    )

    print(
        "Decision:",
        decision
    )