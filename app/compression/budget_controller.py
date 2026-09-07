from app.utils.config import DEFAULT_INITIAL_BUDGET


class BudgetController:

    def __init__(self):

        # Fraction of original tokens to retain
        self.budgets = [
            0.50,
            0.70,
            1.00
        ]

    def initial_budget(self, difficulty=None):
        return DEFAULT_INITIAL_BUDGET

    def next_budget(self, current_budget):

        for budget in self.budgets:

            if budget > current_budget:
                return budget

        return current_budget