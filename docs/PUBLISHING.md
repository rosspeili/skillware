# Publishing to PyPI

This repository is configured to automatically publish releases to PyPI using GitHub Actions.

## Prerequisites

1.  **PyPI Account**: You must have an account on [pypi.org](https://pypi.org/).
2.  **Package Name**: The package name `skillware` must be available, or you must own it.

## One-Time Setup

To allow GitHub Actions to publish on your behalf, you need to configure **Trusted Publishing** (recommended) or use an API Token.

### Option A: Trusted Publishing (Recommended)

1.  Go to [PyPI Publishing Management](https://pypi.org/manage/account/publishing/).
2.  Fille in the details:
    *   **PyPI Project Name**: `skillware` (or create it first if it doesn't exist).
    *   **Owner**: Your PyPI username.
    *   **GitHub Repository Owner**: `ARPAHLS` (or your username).
    *   **GitHub Repository Name**: `skillware`.
    *   **Workflow Filename**: `publish.yml`.
    *   **Environment Name**: `pypi`.
3.  Click **Add**.

### Option B: API Token (Classic)

1.  Go to [PyPI Account Settings](https://pypi.org/manage/account/).
2.  Scroll to **API Tokens** and click **Add API token**.
3.  Name it `GitHub Actions` and set Scope to "Entire account" (for new projects) or specific project.
4.  Copy the token (starts with `pypi-`).
5.  Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions**.
6.  Click **New repository secret**.
7.  Name: `PYPI_PASSWORD`.
8.  Value: Paste your token.
9.  **Note**: You will need to edit `.github/workflows/publish.yml` to use `password: ${{ secrets.PYPI_PASSWORD }}` instead of `permissions: id-token: write`.

## How to Publish a New Version

1.  **Update Version**: Bump the version number in `pyproject.toml` (e.g., `0.1.0` -> `0.1.1`).
2.  **Commit & Push**: Push the change to `main`.
3.  **Draft Release**:
    *   Go to GitHub -> **Releases** -> **Draft a new release**.
    *   Tag version: `v0.1.1` (matching `pyproject.toml`).
    *   Title: `v0.1.1`.
    *   Click **Publish release**.
4.  **Watch Magic**: The `Publish to PyPI` workflow will run automatically and upload your package.
