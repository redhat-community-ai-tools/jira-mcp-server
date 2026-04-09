#!/usr/bin/env python

import os
import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".jira-mcp-config.json"


def load_config():
    """Load configuration from file if it exists."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)  # Secure permissions


def get_setting(key, default=None, prompt=None):
    """
    Get a setting from environment, config file, or prompt user.

    Priority:
    1. Environment variable
    2. Config file
    3. User prompt (if provided)
    4. Default value
    """
    # Check environment variable first
    env_value = os.getenv(key)
    if env_value:
        return env_value

    # Check config file
    config = load_config()
    if key in config:
        return config[key]

    # Prompt user if interactive
    if prompt and os.isatty(0):
        user_input = input(f"{prompt}: ").strip()
        if user_input:
            config[key] = user_input
            save_config(config)
            return user_input

    return default


def configure_interactive():
    """Interactive configuration wizard."""
    print("Jira MCP Server Configuration")
    print("=" * 40)
    print("Press Enter to keep existing values.\n")

    config = load_config()

    # JIRA URL (required)
    current_url = config.get("JIRA_URL", "")
    jira_url = input(f"JIRA URL [{current_url}]: ").strip()
    if jira_url:
        config["JIRA_URL"] = jira_url

    # JIRA API Token (required)
    current_token = config.get("JIRA_API_TOKEN", "")
    masked_token = f"{current_token[:8]}..." if current_token else ""
    jira_token = input(f"JIRA API Token [{masked_token}]: ").strip()
    if jira_token:
        config["JIRA_API_TOKEN"] = jira_token

    # Enable write operations
    current_write = config.get("JIRA_ENABLE_WRITE", "false")
    enable_write = input(f"Enable write operations? (true/false) [{current_write}]: ").strip().lower()
    if enable_write:
        config["JIRA_ENABLE_WRITE"] = enable_write

    # Advanced: JIRA Email (only for legacy basic_auth - most users don't need this)
    print("\nAdvanced settings (press Enter to skip):")
    current_email = config.get("JIRA_EMAIL", "")
    if current_email:
        jira_email = input(f"JIRA Email (legacy basic_auth only) [{current_email}]: ").strip()
        if jira_email:
            config["JIRA_EMAIL"] = jira_email
        else:
            # User pressed enter - keep existing
            pass
    else:
        # Not set, ask if user wants to add it
        print("JIRA_EMAIL (only needed for legacy basic_auth - most users don't need this)")
        jira_email = input("JIRA Email (leave empty to skip): ").strip()
        if jira_email:
            config["JIRA_EMAIL"] = jira_email

    save_config(config)
    print(f"\nConfiguration saved to {CONFIG_FILE}")
    print("\nRequired settings: JIRA_URL, JIRA_API_TOKEN")
    print("Optional settings: JIRA_ENABLE_WRITE, JIRA_EMAIL (legacy only)")


def show_config():
    """Display current configuration."""
    config = load_config()
    if not config:
        print("No saved configuration found.")
        return

    print("Current Configuration:")
    print("=" * 40)
    for key, value in config.items():
        if "TOKEN" in key or "PASSWORD" in key:
            # Mask sensitive values
            masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"{key}: {masked_value}")
        else:
            print(f"{key}: {value}")
    print(f"\nConfig file: {CONFIG_FILE}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "show":
            show_config()
        elif sys.argv[1] == "reset":
            if CONFIG_FILE.exists():
                CONFIG_FILE.unlink()
                print(f"Configuration deleted: {CONFIG_FILE}")
            else:
                print("No configuration file found.")
        else:
            print("Usage: python config.py [show|reset]")
            print("  (no args): Interactive configuration")
            print("  show:      Display current configuration")
            print("  reset:     Delete configuration file")
    else:
        configure_interactive()
