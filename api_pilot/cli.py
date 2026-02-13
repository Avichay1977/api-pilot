"""CLI interface for api-pilot."""
import sys
import argparse
from .resolver import resolve_key
from .validators import validate_key

def doctor():
    """Run diagnostics on API key configuration."""
    print("🔍 api-pilot doctor\n")
    
    # Check for .env file
    import os
    if os.path.exists('.env'):
        print("✓ .env file found")
    else:
        print("✗ .env file not found")
    
    # Check environment variables
    common_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GITHUB_TOKEN', 'STRIPE_API_KEY']
    for key_name in common_keys:
        if os.getenv(key_name):
            print(f"✓ {key_name} found in environment")
        else:
            print(f"✗ {key_name} not found")
    
    print("\n💡 Tip: Set keys in .env file or environment variables")

def validate_cli():
    """Validate API keys from CLI."""
    parser = argparse.ArgumentParser(description='Validate API keys')
    parser.add_argument('key_name', help='Name of the API key (openai, anthropic, github, stripe)')
    parser.add_argument('--key', help='API key value (or use env/vault)')
    parser.add_argument('--strict', action='store_true', help='Exit with error if validation fails')
    
    args = parser.parse_args()
    
    # Resolve key
    if args.key:
        key_value = args.key
    else:
        key_value = resolve_key(args.key_name)
    
    if not key_value:
        print(f"❌ Could not resolve key: {args.key_name}")
        sys.exit(1) if args.strict else sys.exit(0)
    
    # Validate
    success, message = validate_key(args.key_name, key_value)
    
    if success:
        print(f"✓ {args.key_name}: {message}")
        sys.exit(0)
    else:
        print(f"✗ {args.key_name}: {message}")
        sys.exit(1) if args.strict else sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'doctor':
        doctor()
    else:
        validate_cli()
