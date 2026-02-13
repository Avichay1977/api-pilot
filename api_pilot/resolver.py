"""Core resolution logic for api-pilot."""
import os
import subprocess
from pathlib import Path


class KeyNotFoundError(Exception):
    """Raised when API key cannot be resolved."""
    pass


class StrictModeError(Exception):
    """Raised when .env is used in strict mode."""
    pass


resolve_key(key_name, validate=False, strict=False):
    """
    Resolve API key from ENV -> .env -> vault.
    
    Args:
        key_name: Name of the key (e.g., 'openai', 'anthropic')
        validate: If True, validates the key works
        strict: If True, fails if .env is used (CI safety)
    
    Returns:
        str: The resolved API key
    
    Raises:
        KeyNotFoundError: If key not found
        StrictModeError: If .env used in strict mode
    """
    # Normalize key name
    env_key = f"{key_name.upper()}_API_KEY"
    
    # Try ENV first
    value = os.environ.get(env_key)
    if value:
        if validate:
            _validate_key(key_name, value)
        return value
    
    # Try .env file
    value, source = _resolve_from_dotenv(env_key)
    if value:
        if strict:
            raise StrictModeError(
                f"{env_key} found in .env but strict mode requires ENV or vault"
            )
        if validate:
            _validate_key(key_name, value)
        return value
    
    # Try vault (1Password CLI)
    value = _resolve_from_vault(env_key)
    if value:
        if validate:
            _validate_key(key_name, value)
        return value
    
    raise KeyNotFoundError(
        f"{env_key} not found in ENV, .env, or vault"
    )


def _resolve_from_dotenv(key):
    """Load from .env file."""
    env_file = Path.cwd() / ".env"
    if not env_file.exists():
        return None, None
    
    try:
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith(key + "="):
                    value = line.split("=", 1)[1].strip('"\'')
                    return value, ".env"
    except Exception:
        pass
    
    return None, None


def _resolve_from_vault(key):
    """Try 1Password CLI."""
    try:
        result = subprocess.run(
            ["op", "read", f"op://private/{key}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    
    return None


def _validate_key(key_name, key_value):
    """Validate key works (imported later to avoid circular import)."""
    try:
        from .validators import validate_key
        success, message = validate_key(key_name, key_value)
        if not success:
            raise ValueError(f"Key validation failed: {message}")
    except ImportError:
        # validators not available, skip validation
        pass

# Backward compatibility alias
require = resolve_key
