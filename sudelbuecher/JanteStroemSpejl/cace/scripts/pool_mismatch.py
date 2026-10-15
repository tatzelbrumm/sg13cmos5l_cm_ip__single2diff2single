def postprocess(results, conditions):
    # CACE collates all Monte Carlo iterations, so each eXX entry is a list.
    pooled = []
    for k in range(1, 11):
        key = f"e{k:02d}"
        pooled.extend(float(x) for x in results[key])
    return {"error_all": pooled}
