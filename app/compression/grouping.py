import re


class TokenGrouper:

    def group(self, tokens):

        groups = []
        i = 0

        while i < len(tokens):

            token = tokens[i]

            # Number + unit
            if (
                i + 1 < len(tokens)
                and re.search(r"\d", token)
                and tokens[i + 1].lower().strip(".,!?") in {
                    "km", "m", "cm", "mm",
                    "kg", "g",
                    "hour", "hours", "hr", "hrs",
                    "minute", "minutes", "min",
                    "second", "seconds", "sec"
                }
            ):
                groups.append(
                    [token, tokens[i + 1]]
                )
                i += 2
                continue

            # Percentage + following context
            if "%" in token:

                group = [token]

                # Keep "of"
                if (
                    i + 1 < len(tokens)
                    and tokens[i + 1].lower() == "of"
                ):
                    group.append(tokens[i + 1])
                    i += 1

                # Keep following number
                if (
                    i + 1 < len(tokens)
                    and re.search(r"\d", tokens[i + 1])
                ):
                    group.append(tokens[i + 1])
                    i += 1

                groups.append(group)
                i += 1
                continue

            groups.append([token])

            i += 1

        return groups