def postprocess(results, conditions):
    pooled = []
    for k in range(1, 11):
        key = f"e{k:02d}"
        vals = results[key]
        if isinstance(vals, (list, tuple)):
            pooled.extend(float(x) for x in vals)
        else:
            pooled.append(float(vals))
    return {"error_all": pooled}
