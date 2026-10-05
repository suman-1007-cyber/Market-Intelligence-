def scenario(base, growth_rates):
    return {
        str(name): float(base) * (1.0 + float(rate))
        for name, rate in growth_rates.items()
    }
