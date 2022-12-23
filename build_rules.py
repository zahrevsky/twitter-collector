def build_rules(infls):
    while len(infls):
        n = 1
        first_n = infls[:n]
        while not (rule_len(first_n) >= 512 or len(infls) < n):
            n += 1
            first_n = infls[:n]
        yield ' OR '.join(f'from:{infl}' for infl in first_n[:-1])
        infls = infls[(n-1):]


def rule_len(infls):
    return 9 * len(infls) - 4 + sum(len(infl) for infl in infls)
