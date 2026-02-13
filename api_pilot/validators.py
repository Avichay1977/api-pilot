"""API key validators using stdlib only."""
import urllib.request
import urllib.error
import json


def validate_key(key_name, key_value):
    """Validate an API key.
    
    Returns:
        (bool, str): (success, message)
    """
    validators = {
        "openai": _validate_openai,
        "anthropic": _validate_anthropic,
        "github": _validate_github,
        "stripe": _validate_stripe,
    }
    
    validator = validators.get(key_name.lower())
    if not validator:
        return False, f"No validator for {key_name}"
    
    return validator(key_value)


def _validate_openai(key):
    try:
        req = urllib.request.Request(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {key}"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            models = [m["id"] for m in data.get("data", [])]
            return True, f"Valid (models: {', '.join(models[:3])}...)"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def _validate_anthropic(key):
    try:
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/models",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return True, "Valid"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def _validate_github(key):
    try:
        req = urllib.request.Request(
            "https://api.github.com/user",
            headers={"Authorization": f"token {key}"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            return True, f"Valid (user: {data.get('login')})"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def _validate_stripe(key):
    try:
        req = urllib.request.Request(
            "https://api.stripe.com/v1/customers?limit=1",
            headers={"Authorization": f"Bearer {key}"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return True, "Valid"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)
