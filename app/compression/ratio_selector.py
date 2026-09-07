class RatioSelector:

    def select(self, difficulty):
        if difficulty < 0.30:
            return 0.30

        elif difficulty < 0.60:
            return 0.50

        else:
            return 0.70