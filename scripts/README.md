# Publishing Scripts

Automated scripts to publish reinvent-2025-mcp packages to NPM and PyPI.

## 🚀 Quick Start

### First Time Setup
```bash
./scripts/setup-publishing.sh
```

### Publish Both Packages
```bash
./scripts/publish-all.sh
```

## 📋 Account Creation

### NPM Account
1. Go to https://www.npmjs.com/signup
2. Create account with email/username/password
3. Verify email address
4. Run `npm login` in terminal

### PyPI Account  
1. Go to https://pypi.org/account/register/
2. Create account with email/username/password
3. Verify email address
4. Create API token at https://pypi.org/manage/account/token/
5. Set environment variables:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=your-api-token
   ```

## 📜 Individual Scripts

### `setup-publishing.sh`
- Installs required tools (build, twine, uvx)
- Checks authentication for both NPM and PyPI
- Makes other scripts executable
- Guides through account setup

### `publish-npm.sh`
- Publishes Node.js package to NPM
- Runs tests before publishing
- Checks package name availability
- Tests installation after publishing

### `publish-pypi.sh`
- Publishes Python package to PyPI
- Runs tests before publishing
- Optionally uploads to Test PyPI first
- Tests installation after publishing

### `publish-all.sh`
- Master script that runs both NPM and PyPI publishing
- Checks prerequisites
- Publishes both packages sequentially

## 🔧 Prerequisites

- Node.js 18+ and npm
- Python 3.11+ and pip
- NPM account and login
- PyPI account and credentials

## 📦 Package Names

Make sure these names are available:
- **NPM**: `reinvent-2025-mcp`
- **PyPI**: `reinvent-2025-mcp`

If names are taken, update:
- `npx/package.json` → `"name"` field
- `uvx/pyproject.toml` → `name` field

## 🎯 Usage Flow

1. **Setup** (first time only):
   ```bash
   ./scripts/setup-publishing.sh
   ```

2. **Publish**:
   ```bash
   ./scripts/publish-all.sh
   ```

3. **Test Installation**:
   ```bash
   npx reinvent-2025-mcp
   uvx reinvent-2025-mcp
   ```

## 🔍 Troubleshooting

### Package Name Conflicts
- Change package names in `package.json` and `pyproject.toml`
- Or increment version if you own the packages

### Authentication Issues
- NPM: Run `npm login` again
- PyPI: Check environment variables or create ~/.pypirc:
  ```bash
  # Environment variables (recommended)
  export TWINE_USERNAME=__token__
  export TWINE_PASSWORD=your-api-token
  
  # Or create ~/.pypirc file:
  [pypi]
  username = __token__
  password = your-api-token
  ```

### Build Failures
- Ensure all tests pass: `npm test` and `pytest`
- Check dependencies are correctly specified
- Verify entry points in configuration files
