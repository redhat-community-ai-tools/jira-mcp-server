# JIRA MCP Server

**A production-ready Model Context Protocol server that provides comprehensive JIRA operations to AI assistants.**

[![License](https://img.shields.io/badge/license-Internal-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io)

## Table of Contents

- [Overview](#overview)
- [What is MCP?](#what-is-mcp)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Usage Examples](#usage-examples)
- [Deployment](#deployment)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Support](#support)

---

## Overview

The JIRA MCP Server is a **generic, production-ready** tool that brings JIRA's full power to AI assistants through the Model Context Protocol. It enables natural language interaction with your JIRA instance while maintaining security, auditability, and organizational standards.

**Compatible with:**
- **Claude Desktop** - GUI application for AI assistance
- **Claude Code** - CLI tool for development workflows
- Any other MCP-compatible client

### Why This Matters

**Before:** Teams spend hours each week on repetitive JIRA tasks
- Creating similar issues repeatedly
- Searching for related tickets
- Bulk operations requiring manual UI clicks
- Context switching between code and JIRA

**After:** AI-assisted JIRA operations through natural language
- "Create a story for feature X with standard labels"
- "Close all QE tracker tickets as duplicates"
- "Find all open bugs assigned to my team"
- Seamless integration with development workflow

**Result:** 80-90% reduction in JIRA administrative overhead

---

## What is MCP?

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open standard that enables AI assistants to securely connect to external tools and data sources. Think of it as a universal adapter that lets Claude interact with your enterprise systems.

### How It Works

```
+-----------------+          +------------------+         +-------------+ 
|     Claude      |          |                  |         |             | 
|  Desktop/Code   |   MCP    |  MCP Server      |  REST   |  Jira API   |
|                 |<-------> | (This Project)   |<------->|             |
|                 | Protocol |                  |   API   |             |
+-----------------+          +------------------+         +-------------+
         ↑                           ↑  
         |                           |
         |                           | 
         ↓                           ↓
+-----------------+         +------------------+
|  Natural        |         | Uses jira CLI    |
|  Language:      |<------->| for auth & API   |
|                 |         |                  |
| "Create a story |         +------------------+
|  in PROJECT-X   |                  
|  called 'Add    |                  
|  Feature Y'"    |
+-----------------+
```

### Key Benefits

- **Standardized**: Works with any MCP-compatible client
- **Secure**: Uses your existing JIRA credentials
- **Auditable**: All operations logged in JIRA
- **Extensible**: Easy to add custom tools for your organization

---

## Features

### Core Operations

-  **Issue Management**
  - Create issues (Story, Task, Bug, Epic, Sub-task)
  - Edit issue fields
  - Add labels and metadata
  - View detailed issue information

-  **Search & Discovery**
  - JQL (JIRA Query Language) search
  - Filter by project, status, assignee, labels
  - Structured result formatting

-  **Issue Relationships**
  - Link issues (blocks, relates to, duplicates, depends on)
  - Create issue hierarchies
  - Maintain traceability

-  **Workflow Operations**
  - Transition issues through workflow
  - Close issues with resolution
  - Add comments during transitions

-  **Batch Operations**
  - Close multiple issues at once
  - Bulk label updates
  - Mass transitions

### Technical Features

- **Generic Design**: Works with any JIRA instance
- **Project Agnostic**: Supports all project types
- **Error Handling**: Comprehensive retry logic and error reporting
- **Timeout Management**: Configurable operation timeouts
- **JSON Responses**: Structured, parseable output
- **CLI Integration**: Leverages battle-tested jira-cli tool

---

## Architecture

### System Design

```
+-----------------------------------------------------------------+
|                         User Layer                              |
|                                                                 |
|  +--------------+     +--------------+     +--------------+     |
|  |   Claude     |     |   Other MCP  |     |   Future     |     |
|  | Desktop/code |     |   Clients    |     |   Clients    |     |
|  +------+-------+     +------+-------+     +------+-------+     |
|         |                    |                    |             |
+---------+--------------------+--------------------+-------------+
          |                    |                    |
          +--------------------+--------------------+
                               |
                   Model Context Protocol
                               |
+------------------------------+----------------------------------+
|                   MCP Server Layer                              |
|                              |                                  |
|  +---------------------------v----------------------------+     |
|  |             FastMCP Server (server.py)                  |    |
|  |                                                         |    |
|  |  +-------------+  +-------------+  +-------------+      |    |
|  |  |create_issue()|  |search_issues|  |link_issues()|     |    |
|  |  +-------------+  +-------------+  +-------------+      |    |
|  |                                                         |    |
|  |  +-------------+  +-------------+  +-------------+      |    |
|  |  |transition() |  |add_labels() |  |batch_close()|      |    |
|  |  +-------------+  +-------------+  +-------------+      |    |
|  |                                                         |    |
|  |  +-------------+                                        |    |
|  |  |view_issue() |         7 Tools Total                  |    |
|  |  +-------------+                                        |    |
|  +--------------------------+------------------------------+    |
|                             |                                   |
|                    run_jira_command()                           |
|                             |                                   |
+-----------------------------+-----------------------------------+
                              |
+-----------------------------v------------------------------------+
|                    Integration Layer                             |
|                                                                  |
|  +----------------------------------------------------------+    |
|  |         jira-cli (ankitpokhrel/jira-cli)                 |    |
|  |                                                          |    |
|  |  - Authentication management                             |    |
|  |  - Secure credential storage                             |    |
|  |  - REST API abstraction                                  |    |
|  +---------------------------+------------------------------+    |
|                              |                                   |
+------------------------------+-----------------------------------+
                               |
                          HTTPS/TLS
                               |
+------------------------------v-----------------------------------+
|                      JIRA Instance                               |
|                                                                  |
|  +-----------------------------------------------------------+   |
|  |                    JIRA REST API                          |   |
|  |                                                           |   |
|  |  - Issue operations     - Search (JQL)                    |   |
|  |  - Workflow transitions - Link management                 |   |
|  |  - Field updates        - Audit logging                   |   |
|  +-----------------------------------------------------------+   |
|                                                                  |
+------------------------------------------------------------------+
```

### Data Flow

1. **User Request**: Natural language query to Claude Desktop
2. **Tool Selection**: Claude determines appropriate MCP tool to use
3. **MCP Protocol**: Tool invocation sent to MCP server via stdio
4. **Command Execution**: Server translates to jira-cli command
5. **API Call**: jira-cli makes authenticated REST API call to JIRA
6. **Response Processing**: Parse and structure JIRA API response
7. **Result Return**: JSON-formatted result back through MCP protocol
8. **User Presentation**: Claude formats result for user in natural language

### Security Model

```
+-------------------------------------------------------------+
|                    Security Boundaries                      |
|                                                             |
|  User Credentials  --->  jira-cli Storage  --->  JIRA API   |
|  (Initial Setup)         (Encrypted)            (TLS 1.2+)  |
|                                                             |
|  +------------------------------------------------------+   |
|  |  Permissions Model                                   |   |
|  |                                                      |   |
|  |  - Server runs with user's JIRA permissions          |   |
|  |  - No privilege escalation                           |   |
|  |  - All operations audited in JIRA                    |   |
|  |  - No credential storage in MCP server               |   |
|  +------------------------------------------------------+   |
+-------------------------------------------------------------+
```

---

## Prerequisites

### Required

1. **Python 3.10 or higher**
   ```bash
   python3 --version  # Should be 3.10+
   ```

2. **JIRA CLI** ([ankitpokhrel/jira-cli](https://github.com/ankitpokhrel/jira-cli))
   ```bash
   # macOS
   brew install ankitpokhrel/jira-cli/jira-cli

   # Linux
   curl -L https://github.com/ankitpokhrel/jira-cli/releases/download/v1.4.0/jira_1.4.0_linux_x86_64.tar.gz | tar xz
   sudo mv bin/jira /usr/local/bin/

   # Windows
   scoop install jira-cli
   ```

3. **JIRA Access**
   - Valid JIRA account
   - API token or credentials
   - Appropriate project permissions

### Optional

- **Claude Desktop** - For AI-assisted JIRA operations
- **Virtual Environment** - Recommended for Python isolation

---

## Quick Start

Get up and running in under 5 minutes.

**Works with:**
-  **Claude Desktop** (GUI application)
-  **Claude Code** (CLI tool)

### Using Makefile (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/rrasouli/jira-mcp-server.git ~/Documents/GitHub/jira-mcp-server
cd ~/Documents/GitHub/jira-mcp-server

# 2. Install everything (jira-cli + Python dependencies)
make install

# 3. Configure jira CLI
jira init

# 4. Run interactive setup
make setup

# 5. Restart Claude Desktop

# 6. Test it out
# Ask Claude: "Create a test story in PROJECT-X called 'MCP Integration Test'"
```

### Using Setup Script

```bash
cd ~/Documents/GitHub/jira-mcp-server
./setup.sh
```

The setup will:
- Check prerequisites
- Create Python virtual environment
- Install dependencies
- Configure JIRA CLI
- Update Claude Desktop configuration
- Validate installation

---

## Makefile Commands

The project includes a comprehensive Makefile for easy setup and development:

```bash
make help              # Show all available commands
make status            # Show installation status
make install           # Full installation (jira-cli + Python deps)
make install-jira-cli  # Install jira CLI only
make setup             # Run interactive setup
make run               # Start the MCP server
make test              # Run tests
make lint              # Check code style
make format            # Format code with black
make clean             # Clean build artifacts
```

**Common Workflows:**

```bash
# First-time setup
make install
make setup

# Development
make dev-setup         # Install development dependencies
make test              # Run tests
make lint              # Check code style
make format            # Format code

# Check what's installed
make status
```

---

## Installation

### Option 1: Using Makefile (Recommended)

```bash
cd ~/Documents/GitHub/jira-mcp-server
make install    # Installs jira-cli and Python dependencies
make setup      # Interactive configuration
```

The Makefile automatically detects your OS (macOS/Linux) and installs prerequisites accordingly.

### Option 2: Using Setup Script

```bash
cd ~/Documents/GitHub/jira-mcp-server
./setup.sh
```

Follow the interactive prompts to configure your JIRA instance and default project.

### Option 3: Manual Installation

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip
pip install mcp

# 3. Configure JIRA CLI
jira init
# Provide:
# - JIRA server URL (e.g., https://jira.company.com)
# - Authentication method (Personal Access Token recommended)
# - Your credentials

# 4. Make server executable
chmod +x server.py

# 5. Test the server
python server.py
# Server starts and waits for MCP protocol messages
```

### Option 4: Package Installation

```bash
cd ~/jira-mcp-server
pip install -e .
```

This installs the server as a Python package, making it available system-wide.

---

## Configuration

This JIRA MCP server works with **both Claude Desktop (GUI) and Claude Code (CLI)**.

### Quick Reference: Claude Desktop vs Claude Code

| Aspect | Claude Desktop | Claude Code |
|--------|---------------|-------------|
| **Config file** | `~/Library/Application Support/Claude/claude_desktop_config.json` | `~/.claude.json` |
| **Config scope** | Global (all conversations) | Per-project (each directory) |
| **MCP location** | `mcpServers` at root level | `projects.<path>.mcpServers` |
| **Server name** | Usually `jira` | Can be `jira` or `jira-prod` |
| **Restart required** | Yes (restart app) | Yes (exit/restart in directory) |

**Key difference:** Claude Desktop has **global** MCP configuration, while Claude Code has **per-project** configuration. This means you must configure jira-prod separately for each working directory in Claude Code.

### Configuration Priority

Settings are loaded in the following order:
1. **Environment variables** (highest priority)
2. **Persistent config file** `~/.jira-mcp-config.json`
3. **Default values** (lowest priority)

### Quick Start: Interactive Configuration

Run the configuration wizard to save your settings persistently:

```bash
python server.py --configure
```

This creates `~/.jira-mcp-config.json` with secure permissions (0600) containing:
- **JIRA_URL**: Your JIRA instance URL (required)
- **JIRA_API_TOKEN**: Your API token (required)
- **JIRA_ENABLE_WRITE**: Enable write operations - true/false (optional, default: false)
- **JIRA_EMAIL**: For legacy basic_auth only (optional, not needed for modern JIRA)

**Benefits:**
- Settings persist between sessions
- No need to set environment variables every time
- Secure file permissions (owner-only read/write)
- View current config: `python server.py --show-config`
- Reset config: `python config.py reset`

### Environment Variables

You can override the persistent config with environment variables:

```bash
# Required
export JIRA_URL="https://jira.your-company.com"
export JIRA_API_TOKEN="your-api-token-here"

# Optional
export JIRA_ENABLE_WRITE="true"  # Enable write operations (default: false)

# Legacy only (not needed for modern JIRA)
export JIRA_EMAIL="your.email@company.com"  # Only for old basic_auth
```

### Option 1: Claude Desktop Configuration (GUI)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["/absolute/path/to/jira-mcp-server/server.py"],
      "env": {
        "JIRA_URL": "https://jira.your-company.com",
        "JIRA_DEFAULT_PROJECT": "YOUR_PROJECT"
      }
    }
  }
}
```

**Important:**
- Use absolute paths (not `~` or `$HOME`)
- Replace placeholders with your actual values
- Restart Claude Desktop after configuration changes

**Configuration File Locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

---

### Option 2: Claude Code Configuration (CLI)

**IMPORTANT:** Claude Code uses **per-project MCP configuration**, not global configuration.

#### Understanding Claude Code's Configuration Model

Unlike Claude Desktop, Claude Code does **not** support global MCP server configuration. MCP servers are configured per-project in `~/.claude.json` under each project's directory path.

**Key differences:**
- **Claude Desktop**: Uses `~/Library/Application Support/Claude/claude_desktop_config.json` (global)
- **Claude Code**: Uses `~/.claude.json` with per-project `mcpServers` sections (no global option)

This means:
- MCP servers must be configured separately for each working directory
- Sessions in different directories won't share MCP server configuration
- You'll need to duplicate MCP server config across projects where you want it available

#### Per-Project Configuration in `~/.claude.json`

Claude Code stores project-specific settings in `~/.claude.json`. Each project directory has its own `mcpServers` section:

```json
{
  "projects": {
    "/Users/YOUR_USERNAME/Documents": {
      "mcpServers": {
        "jira-prod": {
          "type": "stdio",
          "command": "/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/venv/bin/python",
          "args": [
            "/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/server.py"
          ],
          "env": {}
        }
      }
    },
    "/Users/YOUR_USERNAME/Documents/GitHub/my-project": {
      "mcpServers": {
        "jira-prod": {
          "type": "stdio",
          "command": "/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/venv/bin/python",
          "args": [
            "/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/server.py"
          ],
          "env": {}
        }
      }
    }
  }
}
```

**To add jira-prod to a project:**

1. Find your project's section in `~/.claude.json`
2. Locate the `mcpServers` object (will be empty `{}` if not configured)
3. Add the jira-prod configuration:

```json
"mcpServers": {
  "jira-prod": {
    "type": "stdio",
    "command": "/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/venv/bin/python",
    "args": [
      "/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/server.py"
    ],
    "env": {}
  }
}
```

4. Exit and restart Claude Code in that directory

**To add jira-prod to multiple projects:**

You'll need to duplicate the `jira-prod` configuration in each project's `mcpServers` section. For example:

```json
{
  "projects": {
    "/Users/YOUR_USERNAME/Documents": {
      "mcpServers": {
        "jira-prod": { ... }
      }
    },
    "/Users/YOUR_USERNAME/Documents/GitHub/project-a": {
      "mcpServers": {
        "jira-prod": { ... }
      }
    },
    "/Users/YOUR_USERNAME/Documents/GitHub/project-b": {
      "mcpServers": {
        "jira-prod": { ... }
      }
    }
  }
}
```

**Why per-project configuration?**
- Different projects may need different MCP servers
- Isolates tool availability by working directory
- Prevents MCP servers from loading in irrelevant contexts

**Verify MCP Server is Loaded:**
```bash
# When you start Claude Code in a configured directory, you should see:
# "MCP server jira-prod initialized"

# In an unconfigured directory, jira-prod won't be available
```

**After configuration:**
1. Exit Claude Code if running
2. Restart Claude Code in the configured directory
3. Ask Claude: "Create a test story in YOUR_PROJECT called 'MCP Integration Test'"

### Option 3: Cursor Configuration

Cursor is a popular AI-powered code editor that supports MCP servers. This section provides complete setup instructions.

#### Prerequisites for Cursor

1. **Get a Jira API Token:**
   - Visit https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Give it a descriptive name (e.g., "Cursor MCP Server")
   - Copy and securely save the token

2. **Know your paths:**
   ```bash
   # Find absolute path to jira-mcp-server
   cd ~/Documents/GitHub/jira-mcp-server
   pwd
   # Copy this path - you'll need it for configuration
   ```

#### Configuration Steps

**Create or edit `~/.cursor/mcp.json`** (global configuration):

```json
{
  "mcpServers": {
    "jira-prod": {
      "command": "/absolute/path/to/jira-mcp-server/venv/bin/python",
      "args": ["/absolute/path/to/jira-mcp-server/server.py"],
      "env": {
        "JIRA_URL": "https://your-instance.atlassian.net",
        "JIRA_DEFAULT_PROJECT": "MYPROJECT",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

**Example with specific paths:**

```json
{
  "mcpServers": {
    "jira-prod": {
      "command": "/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/venv/bin/python",
      "args": ["/Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/server.py"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_DEFAULT_PROJECT": "MYPROJECT",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

**Important Configuration Notes:**
- Use **absolute paths** (e.g., `/Users/username/...` not `~/...`)
- Replace `YOUR_USERNAME` with your actual username
- Replace `YOUR-PROJECT-KEY` with your default Jira project
- Replace `your-email@company.com` with your Jira account email
- Replace `your-api-token-here` with the API token from step 1
- The `JIRA_EMAIL` and `JIRA_API_TOKEN` fields are **required** for Cursor

**Alternative: Workspace-specific configuration**

Create `.cursor/mcp.json` in your project directory for project-specific settings:

```json
{
  "mcpServers": {
    "jira-prod": {
      "command": "/absolute/path/to/jira-mcp-server/venv/bin/python",
      "args": ["/absolute/path/to/jira-mcp-server/server.py"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_DEFAULT_PROJECT": "MYPROJECT",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-token"
      }
    }
  }
}
```

#### After Configuration

1. **Restart Cursor completely** (not just reload window)
2. **Verify the MCP server is connected:**
   - Look for a green indicator or "MCP" status in Cursor
   - The server should show as "jira-prod" (connected)
3. **Test the integration:**
   - Ask Cursor: "Show me all open issues in [YOUR-PROJECT]"
   - Ask Cursor: "Create a test task in [YOUR-PROJECT] called 'MCP Integration Test'"

#### Troubleshooting Cursor Setup

**Issue: MCP Server Shows as Red/Disconnected**

**Symptoms:**
- Red circle next to "jira-prod" in Cursor
- Error: `401 Unauthorized` or authentication failures
- Server appears as disconnected

**Solutions:**

1. **Verify credentials are set in `env` section:**
   ```json
   "env": {
     "JIRA_URL": "https://your-instance.atlassian.net",
     "JIRA_DEFAULT_PROJECT": "PROJECT",
     "JIRA_EMAIL": "your-email@company.com",      // Required!
     "JIRA_API_TOKEN": "your-token-here"          // Required!
   }
   ```

2. **Test credentials manually:**
   ```bash
   curl -u "your-email@company.com:your-api-token" \
     "https://your-instance.atlassian.net/rest/api/3/myself"
   ```
   Should return your user info, not a 401 error.

3. **Verify absolute paths:**
   ```json
   // CORRECT
   "command": "/Users/username/Documents/GitHub/jira-mcp-server/venv/bin/python"
   
   // WRONG - do not use these
   "command": "~/Documents/GitHub/jira-mcp-server/venv/bin/python"
   "command": "./venv/bin/python"
   "command": "python"
   ```

4. **Check virtual environment exists:**
   ```bash
   ls -la /Users/YOUR_USERNAME/Documents/GitHub/jira-mcp-server/venv/bin/python
   # Should show the Python interpreter, not "No such file"
   ```

5. **Regenerate API token if expired:**
   - Visit https://id.atlassian.com/manage-profile/security/api-tokens
   - Delete old token
   - Create new token
   - Update `~/.cursor/mcp.json` with new token
   - Restart Cursor

**Issue: "Python jira library basic_auth mode failing with 401"**

This is a known issue with the Python `jira` library's handling of redirects. The library may strip authentication headers on redirects, while curl preserves them.

**Solution:**
Ensure both `JIRA_EMAIL` and `JIRA_API_TOKEN` are set in the `env` section. This allows the server to use proper authentication headers.

**Issue: Configuration file not found**

If Cursor can't find `~/.cursor/mcp.json`:

```bash
# Create the directory if it doesn't exist
mkdir -p ~/.cursor

# Create the configuration file
cat > ~/.cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "jira-prod": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "JIRA_URL": "https://your-instance.atlassian.net",
        "JIRA_DEFAULT_PROJECT": "PROJECT",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-token"
      }
    }
  }
}
EOF
```

**Issue: Changes not taking effect**

1. Ensure you saved `~/.cursor/mcp.json`
2. Completely quit and restart Cursor (not just reload)
3. Check Cursor's logs for MCP server initialization errors

#### Security Notes for Cursor

- `~/.cursor/mcp.json` contains sensitive credentials
- **DO NOT commit this file to version control**
- Add to `.gitignore` if using workspace-specific `.cursor/mcp.json`
- File permissions should be user-only (600):
  ```bash
  chmod 600 ~/.cursor/mcp.json
  ```

#### Usage Example with Cursor

Once configured, you can use natural language in Cursor:

```
You: "Show me all open bugs in PROJECT assigned to me"

Cursor: [Uses jira-prod MCP server]
Found 3 open bugs:
- PROJECT-101: Bug description here
- PROJECT-102: Another bug description
- PROJECT-103: Yet another bug
```

```
You: "Create a story in PROJECT called 'Add new feature X'"

Cursor: [Uses jira-prod MCP server]
Created story PROJECT-150: Add new feature X
URL: https://your-instance.atlassian.net/browse/PROJECT-150
```

---

## Available Tools

### 1. create_issue

Create a new JIRA issue with comprehensive metadata.

**Parameters:**
- `summary` (required): Issue title
- `issue_type` (required): Story, Task, Bug, Epic, Sub-task
- `project` (optional): Project key, uses `JIRA_DEFAULT_PROJECT` if not specified
- `description` (optional): Detailed issue description
- `labels` (optional): Comma-separated labels

**Returns:**
```json
{
  "issue_key": "PROJECT-1234",
  "url": "https://jira.company.com/browse/PROJECT-1234",
  "success": true
}
```

**Example Usage:**
```
"Create a story in PLATFORM called 'Add OAuth2 authentication support'
with description 'Implement OAuth2 flow for third-party integrations'
and labels security,authentication,oauth"
```

---

### 2. search_issues

Search for issues using JIRA Query Language (JQL).

**Parameters:**
- `jql` (required): JQL query string
- `max_results` (optional): Maximum results to return (default: 50)

**Returns:**
```json
{
  "jql": "project = PLATFORM AND status = Open",
  "count": 12,
  "issues": [
    {
      "key": "PLATFORM-1234",
      "summary": "Add OAuth2 support",
      "status": "Open",
      "assignee": "john.doe",
      "url": "https://jira.company.com/browse/PLATFORM-1234"
    }
  ]
}
```

**Example Queries:**
```
"Search for all critical bugs assigned to me"
→ JQL: assignee = currentUser() AND priority = Critical AND type = Bug

"Find open issues in PLATFORM project with label 'security'"
→ JQL: project = PLATFORM AND status = Open AND labels = security

"Show all stories created this week"
→ JQL: type = Story AND created >= startOfWeek()
```

---

### 3. link_issues

Create relationships between issues.

**Parameters:**
- `inward_issue` (required): First issue key
- `outward_issue` (required): Second issue key
- `link_type` (required): blocks, Related, Duplicate, Depend

**Link Types:**
- `blocks`: outward_issue blocks inward_issue
- `Related`: Issues are related
- `Duplicate`: outward_issue duplicates inward_issue
- `Depend`: inward_issue depends on outward_issue

**Example:**
```
"Link PLATFORM-1234 and PLATFORM-1235 where 1235 blocks 1234"
```

---

### 4. transition_issue

Move an issue through your workflow.

**Parameters:**
- `issue_key` (required): Issue to transition
- `state` (required): Target state (In Progress, Done, Closed, etc.)
- `resolution` (optional): Resolution type (Done, Won't Fix, Duplicate, etc.)
- `comment` (optional): Comment to add during transition

**Example:**
```
"Close PLATFORM-1234 as Duplicate with comment 'Duplicate of PLATFORM-999'"
```

---

### 5. add_labels

Add labels to existing issues.

**Parameters:**
- `issue_key` (required): Issue to update
- `labels` (required): Comma-separated labels

**Example:**
```
"Add labels urgent,customer-facing,security to PLATFORM-1234"
```

---

### 6. view_issue

Get detailed information about an issue.

**Parameters:**
- `issue_key` (required): Issue to view

**Returns:** Full issue details including description, comments, attachments, and metadata.

**Example:**
```
"Show me details of PLATFORM-1234"
```

---

### 7. batch_close_issues

Close multiple issues at once with the same resolution.

**Parameters:**
- `issue_keys` (required): Comma-separated issue keys
- `resolution` (optional): Resolution type (default: "Duplicate")
- `comment` (optional): Comment to add to all issues

**Returns:**
```json
{
  "total": 3,
  "results": [
    {
      "issue_key": "QE-100",
      "state": "Closed",
      "resolution": "Duplicate",
      "success": true
    }
  ]
}
```

**Example:**
```
"Close QE-100, QE-101, QE-102 as duplicates with comment 'Consolidated into QE-99'"
```

---

## Usage Examples

### Using with Claude Desktop vs Claude Code

The same MCP server works with both clients, but the user experience differs:

#### Claude Desktop (GUI) Example

1. Open Claude Desktop application
2. Start a conversation
3. Ask in natural language:

```
You: "Create a story in MYTEAM project called 'Add RuntimeClass support for Windows workloads'
with labels windows,winc,runtimeclass"

Claude: I'll create that story for you using the JIRA MCP server.
[Uses create_issue() tool]

Created story MYTEAM-1234: Add RuntimeClass support for Windows workloads
View at: https://issues.myorg.com/browse/MYTEAM-1234
Labels: windows, winc, runtimeclass
```

#### Claude Code (CLI) Example

```bash
$ claude

You: Create a story in MYTEAM project called 'Add RuntimeClass support'

Claude: I'll create that JIRA story for you.
[MCP server jira initialized]
[Uses jira.create_issue tool]

Created story MYTEAM-1234: Add RuntimeClass support
URL: https://issues.myorg.com/browse/MYTEAM-1234

You: Now search for all open issues in MYTEAM with label 'windows'

Claude: Searching JIRA...
[Uses jira.search_issues tool]

Found 12 open issues:
- MYTEAM-1234: Add RuntimeClass support
- MYTEAM-1230: Fix container isolation
- MYTEAM-1225: Update Windows node configuration
...
```

**Key Differences:**
- **Claude Desktop**: Graphical interface, richer formatting, persistent conversations
- **Claude Code**: Terminal-based, faster for developers, integrates with shell workflow

**Both support the same MCP tools and capabilities!**

---

### Example 1: Create Feature Epic with Subtasks

**User:** "Create an epic for Q2 authentication improvements in PLATFORM project"

**Claude uses:** `create_issue()`
```json
{
  "summary": "Q2 Authentication Improvements",
  "issue_type": "Epic",
  "project": "PLATFORM",
  "description": "Enhance authentication system with OAuth2, 2FA, and session management",
  "labels": "q2-2024,security,authentication"
}
```

**Follow-up:** "Create three subtasks: OAuth2 implementation, 2FA setup, and session timeout"

Claude creates three linked subtasks automatically.

---

### Example 2: Close Duplicate QE Trackers

**User:** "Find all open QE tracker tickets and close them as duplicates"

**Claude workflow:**
1. Uses `search_issues()` with JQL: `type = "QE Tracker" AND status = Open`
2. Extracts issue keys from results
3. Uses `batch_close_issues()` to close all at once

**Result:** 15 tickets closed in seconds instead of manual UI clicks.

---

### Example 3: Sprint Planning Automation

**User:** "Find all high-priority bugs in PLATFORM project and move them to In Progress"

**Claude workflow:**
1. Search: `project = PLATFORM AND priority = High AND type = Bug`
2. For each issue: `transition_issue(key, "In Progress")`
3. Add label: `add_labels(key, "sprint-12")`

---

### Example 4: Release Tracking

**User:** "Create a release tracker for v2.5.0 with standard release tasks"

**Custom tool** (you can add this):
```python
@mcp.tool()
def create_release_tracker(version: str, target_date: str) -> str:
    """Create standardized release tracker with subtasks"""
    # Create epic
    epic = create_issue(f"Release {version}", "Epic", description=f"Release {version} - Target: {target_date}")

    # Create standard subtasks
    tasks = [
        "Code freeze",
        "QE testing complete",
        "Documentation review",
        "Release notes published",
        "Production deployment"
    ]

    for task in tasks:
        subtask = create_issue(task, "Sub-task", ...)
        link_issues(epic["issue_key"], subtask["issue_key"], "Related")
```

---

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for comprehensive deployment strategies.

### Quick Deployment Options

**Option 1: Internal Git Repository** (Recommended)
```bash
git remote add origin https://github.com/your-org/jira-mcp-server.git
git push -u origin main
```

**Option 2: Internal PyPI**
```bash
python -m build
twine upload --repository-url https://pypi.your-org.com dist/*
```

**Option 3: Shared Network Drive**
```bash
cp -r ~/jira-mcp-server /shared/network/tools/
```

**Option 4: Container Registry**
```bash
docker build -t your-registry.com/jira-mcp-server:1.0.0 .
docker push your-registry.com/jira-mcp-server:1.0.0
```

---

## Security

### Credential Management

** Recommended: jira-cli Credential Storage**
- Credentials stored securely by jira-cli
- System keychain integration (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- No credentials in MCP server code or configuration

** Not Recommended: Environment Variables**
- Credentials visible in process list
- Risk of accidental commit to version control
- Less secure than keychain storage

### Permission Model

The MCP server operates with **your JIRA permissions**:
- Cannot escalate privileges
- Respects project-level permissions
- Subject to JIRA's security policies
- All operations audited in JIRA

### API Token Best Practices

1. **Rotate Regularly**: Change API tokens every 90 days
2. **Least Privilege**: Grant minimum required permissions
3. **Never Commit**: Add tokens to `.gitignore`
4. **Audit Access**: Review JIRA audit logs monthly
5. **Revoke Unused**: Delete tokens when no longer needed

### Network Security

- All JIRA API calls over HTTPS/TLS 1.2+
- Certificate validation enforced
- No proxy credential storage
- Respects corporate network policies

---

## Troubleshooting

### Common Issues

#### "jira CLI not found"

**Problem:** jira-cli not installed or not in PATH

**Solution:**
```bash
# macOS
brew install ankitpokhrel/jira-cli/jira-cli

# Linux
curl -L https://github.com/ankitpokhrel/jira-cli/releases/latest/download/jira_linux_x86_64.tar.gz | tar xz
sudo mv bin/jira /usr/local/bin/

# Verify installation
jira version
```

---

#### "Command timed out"

**Problem:** JIRA API call taking longer than 30 seconds

**Solution:** Increase timeout in `server.py`:
```python
# Line 48
timeout=60  # Increase from 30 to 60 seconds
```

For slow JIRA instances, consider 90-120 second timeout.

---

#### "Project required"

**Problem:** No default project configured

**Solution:**
```bash
# Set in Claude Desktop config
export JIRA_DEFAULT_PROJECT="YOUR_PROJECT"

# Or always specify project in requests
"Create a story in PLATFORM called ..."
```

---

#### "Authentication failed"

**Problem:** JIRA credentials invalid or expired

**Solution:**
```bash
# Reconfigure jira-cli
jira init

# Test authentication
jira issue list --jql "assignee = currentUser()"

# Regenerate API token if using PAT
# Visit: https://your-jira.com/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens
```

---

#### "MCP server not responding"

**Problem:** Server process not starting or crashing

**Solution:**
```bash
# Test server directly
cd ~/jira-mcp-server
source venv/bin/activate
python server.py

# Check for errors in output
# Verify Python version
python --version  # Must be 3.10+

# Reinstall dependencies
pip install --upgrade mcp
```

---

#### "Claude Desktop doesn't see the server"

**Problem:** Configuration not loaded correctly

**Solution:**
1. Verify config file location (see Configuration section)
2. Check JSON syntax (use [jsonlint.com](https://jsonlint.com))
3. Ensure absolute paths (not `~` or `$HOME`)
4. Restart Claude Desktop completely
5. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Linux: `~/.config/Claude/logs/`

---

#### "jira-prod not available in some Claude Code sessions"

**Problem:** MCP server works in one directory but not others

**Cause:** Claude Code uses **per-project MCP configuration**, not global configuration. The server is only available in directories where you've configured it.

**Solution:**

1. **Check which directory you're in:**
   ```bash
   pwd
   # Example: /Users/yourname/Documents/GitHub/release
   ```

2. **Edit `~/.claude.json` and find your project's section:**
   ```bash
   # Open the config file
   code ~/.claude.json  # or your editor of choice
   
   # Find the section for your current directory
   # Look for: "/Users/yourname/Documents/GitHub/release": {
   ```

3. **Add jira-prod to that project's `mcpServers`:**
   ```json
   "/Users/yourname/Documents/GitHub/release": {
     "mcpServers": {
       "jira-prod": {
         "type": "stdio",
         "command": "/Users/yourname/Documents/GitHub/jira-mcp-server/venv/bin/python",
         "args": [
           "/Users/yourname/Documents/GitHub/jira-mcp-server/server.py"
         ],
         "env": {}
       }
     }
   }
   ```

4. **Exit and restart Claude Code in that directory**

**To make jira-prod available everywhere:**

Unfortunately, there's no global MCP configuration for Claude Code. You must add the `jira-prod` configuration to each project's `mcpServers` section in `~/.claude.json`.

**Common directories to configure:**
- Your home directory: `/Users/yourname/Documents`
- Each Git repository you work in
- Any worktree directories

**Example multi-project configuration:**
```json
{
  "projects": {
    "/Users/yourname/Documents": {
      "mcpServers": {
        "jira-prod": { ... }
      }
    },
    "/Users/yourname/Documents/GitHub/repo-a": {
      "mcpServers": {
        "jira-prod": { ... }
      }
    },
    "/Users/yourname/Documents/GitHub/repo-b": {
      "mcpServers": {
        "jira-prod": { ... }
      }
    }
  }
}
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test thoroughly
4. Commit: `git commit -m "Add amazing feature"`
5. Push: `git push origin feature/amazing-feature`
6. Open Pull Request

### Adding Custom Tools

```python
@mcp.tool()
def your_custom_tool(param1: str, param2: int) -> str:
    """
    Description of your custom tool.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        JSON string with structured result
    """
    # Your implementation
    result = run_jira_command(["your", "command", "here"])

    return json.dumps({
        "success": result["success"],
        "data": result["output"]
    })
```

---

## Support

### Resources

- **JIRA CLI Documentation**: https://github.com/ankitpokhrel/jira-cli
- **MCP Protocol Specification**: https://modelcontextprotocol.io
- **JIRA REST API Reference**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/

### Reporting Issues

Report bugs or request features at: https://github.com/rrasouli/jira-mcp-server/issues

---

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

---

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release
- 7 core JIRA tools
- Generic JIRA instance support
- FastMCP integration
- Automated setup script
- Comprehensive documentation

---

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Uses [jira-cli](https://github.com/ankitpokhrel/jira-cli) for JIRA integration
- Implements [Model Context Protocol](https://modelcontextprotocol.io)

---

**Questions?** Reach out to the MCP team at mcp-support@your-company.com
