import json


def check_errors(form):
    errorss = list(json.loads(form.errors.as_json()).values())
    errors = list((list(json.loads(form.errors.as_json()).values())[0][0]).values())[0]
    if len(errorss) > 1:
        errors2 = list((list(json.loads(form.errors.as_json()).values())[1][0]).values())[0]
        errors = errors + " & also " + errors2
    return errors
