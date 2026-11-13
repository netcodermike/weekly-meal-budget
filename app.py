def analyze(data):
    target = data['protein']
    days = data['days']
    if type(target) is not int or not 0<=target<=10000 or not 1<=len(days)<=31:
        raise ValueError('Invalid target or day count')
    plans = {0:(0,0,[])}
    for day in days:
        if not 1<=len(day)<=30:
            raise ValueError('Each day needs 1–30 choices')
        new = {}
        for name,cost,protein in day:
            if not isinstance(name,str) or not name or type(cost) is not int or type(protein) is not int or min(cost,protein)<0:
                raise ValueError('Invalid meal')
            for price,total,picks in plans.values():
                candidate = (price+cost,total+protein,picks+[name])
                key = min(target,candidate[1])
                if key not in new or candidate < new[key]:
                    new[key] = candidate
        plans = new
    cost,protein,meals = plans.get(target,(None,None,None))
    return {'cost':cost,'protein':protein,'meals':meals}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
