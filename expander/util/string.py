import re


def from_humps(s: str) -> list[str]:
    def go(s: str) -> list[str]:
        if not s:  # Base case: empty string
            return [""]
        if len(s) == 1:  # Base case: single character
            return [s]

        # Check if the first character is uppercase
        if s[0].isupper():
            # Extract the leading uppercase sequence
            lhs = re.match(r'[A-Z]+', s).group()
            rhs = s[len(lhs):]

            if not rhs:  # If there's no remaining string
                return [lhs]
            else:
                cur_len = len(lhs) - 1
                cur = lhs[:cur_len]
                rec = go(rhs)
                nxt = lhs[cur_len:] + (rec[0] if rec else "")
                rem = rec[1:] if rec else []
                cur_l = [cur] if cur else []
                nxt_l = [nxt] if nxt else []
                return cur_l + nxt_l + rem
        else:
            # Handle non-uppercase part
            cur = re.match(r'[^A-Z]+', s).group()
            rem = s[len(cur):]
            if not rem:
                return [cur]
            else:
                return [cur] + go(rem)

    return go(s)
