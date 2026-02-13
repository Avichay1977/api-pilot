# api-pilot

**Deterministic, CI-safe API key resolution with optional runtime validation (stdlib-only)**

## What it does

- **Deterministic resolution**: ENV → .env → local vault (like 1Password CLI)
- **Optional runtime validation**: Probe APIs (OpenAI, Anthropic, etc.) before your code runs
- **CI-safe defaults**: Automatically skips .env in CI environments
- **MCP integration**: Works with Claude Desktop and other MCP-compatible tools
- **Zero dependencies**: Python stdlib only

## Installation

```bash
pip install api-pilot
```

## Quick example

```python
from api_pilot import require
from openai import OpenAI

# Resolves from ENV → .env → vault, validates the key works
client = OpenAI(api_key=require("openai", validate=True))

# Strict mode: fails if .env is used (CI safety)
key = require("anthropic", strict=True)
```

## CLI: Doctor command

Check all your API keys at once:

```bash
$ api-pilot doctor --validate

✓ openai        [ENV]      valid (gpt-4 available)
✓ anthropic     [.env]     valid (claude-3-opus available)
✗ github        [missing]  not found
⚠ stripe        [.env]     found but validation skipped
```

## Modes

### Default mode
Resolves from ENV → .env → vault. No validation.

```python
key = require("openai")
```

### Validation mode
Probes the API to confirm the key works:

```python
key = require("openai", validate=True)
```

### Strict mode
Fails if key comes from .env (forces ENV or vault):

```python
key = require("openai", strict=True)  # Good for CI
```

## FAQ

**Q: Why not just use `python-dotenv`?**  
A: `dotenv` loads .env files great. `api-pilot` adds deterministic fallback order, optional validation, and CI-safe strict mode.

**Q: Does this replace secret managers?**  
A: No. Use proper secret managers in production. This is for dev/CI environments where you want consistent resolution + optional validation.

**Q: How does validation work?**  
A: Sends minimal API calls (e.g., `GET /v1/models` for OpenAI). Never logs keys. Opt-in only.

**Q: What about security?**  
A: Validation is opt-in and never logs keys. Keys are never sent anywhere except the provider's API for validation. All validation calls use HTTPS.

---

⭐ **If this is useful in your CI or AI workflow, consider starring the repo.**

## License

MIT
