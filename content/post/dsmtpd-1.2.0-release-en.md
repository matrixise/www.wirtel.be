---
tags:
- devops/debugging
- devops/testing
- python
title: "dsmtpd 1.2.0: Test Your Emails Risk-Free"
date: 2026-01-07
categories:
author: Stéphane Wirtel
draft: false
slug: dsmtpd-1-2-0-test-your-emails-risk-free

---

## The Test Email That Never Should Have Been Sent

You know that feeling? You're developing a new email feature, you run your test script, and *boom* — you realize 3 seconds too late that you used the production database. Your CEO just received an email with the subject "TEST - DO NOT READ - LOREM IPSUM".

Or worse: you configured a cloud SMTP server for testing, forgot to disable actual sending, and now your Mailgun account is suspended for "suspicious activity" because you sent 847 emails to `test@example.com` in 5 minutes.

There has to be a better way, right?

## The Problem with Email Testing

Testing email sending in development is like juggling knives: technically possible, but you'll probably end up in the emergency room.

The classic options all have their downsides:

**Option 1: Set up a "real" SMTP server**
- Heavy to install (Postfix, Sendmail...)
- SSL/TLS certificate management
- Risk of getting blacklisted if misconfigured
- Overkill for simple debugging

**Option 2: Use a cloud service (Mailgun, SendGrid...)**
- Requires an account and configuration
- Sending quotas
- Risk of accidentally sending to real addresses
- Network latency for each test

**Option 3: Mock SMTP calls in your tests**
- Doesn't test real integration
- Doesn't allow visual inspection of emails
- Complex to maintain

What we need is something **simple**, **local**, and **risk-free**.

## dsmtpd: An SMTP Server That Stays Home

That's exactly why I created [dsmtpd](https://github.com/matrixise/dsmtpd) in 2013. The concept? A minimalist SMTP server that runs locally, captures all your test emails, and never sends them anywhere.

Think of it as a **black hole for your test emails**: everything goes in, nothing comes out.

Installation and usage fit in 3 lines:

```bash
# Installation
pip install dsmtpd

# Launch (localhost:1025 by default)
dsmtpd

# In your code, point to localhost:1025
# That's it!
```

Your application thinks it's sending a real email. The SMTP server responds "OK, email received!". But in reality, the email is just logged in your terminal or saved in a local Maildir.

**Zero configuration. Zero risk. Zero latency.**

## What's New in Version 1.2.0

Since version 1.1 in September 2025, I hadn't made many changes to dsmtpd, until today, when I've added some new features for developers, clarifications around SMTPUTF8, and improvements to the complete development and release workflow.

### SMTPUTF8 Support: International Emails

The big news is full support for **SMTPUTF8** ([RFC 6531](https://datatracker.ietf.org/doc/html/rfc6531)). This SMTP extension allows UTF-8 characters in email addresses and message content.

Concretely, you can now test emails with:
- International addresses: `用户@例え.jp`
- Accented characters: `françois@société.fr`
- Emojis in subjects (yes, really)

Support is **enabled by default** thanks to aiosmtpd. No configuration needed.

```bash
# Send an email with UTF-8 address
swaks --from user@example.com \
      --to 用户@例え.jp \
      --server localhost \
      --port 1025 \
      --data "Subject: Test UTF-8\n\nBonjour 世界 ! 🌍"
```

### --disable-smtputf8 Option: Test Legacy Compatibility

But sometimes you need to test that your application correctly handles **old SMTP clients** that don't support UTF-8.

The new `--disable-smtputf8` option disables this extension:

```bash
# Legacy mode: no UTF-8 support
dsmtpd --disable-smtputf8

# Now the server rejects UTF-8 emails
# Perfect for testing error handling
```

This is particularly useful if you're developing an application that must support legacy systems or if you want to reproduce a bug reported by a client using an old SMTP server.

### Python 3.14 and Modern Tooling

Version 1.2.0 officially supports **Python 3.14** (freshly released), in addition to Python 3.10, 3.11, 3.12, and 3.13.

On the development side, the project has adopted modern tools from the Python ecosystem:

- **ruff** for linting and formatting (ultra fast)
- **mypy** for type checking
- **pytest-cov** for test coverage (64%)
- **prek** for pre-commit hooks

If you want to contribute, everything is ready:

```bash
git clone https://github.com/matrixise/dsmtpd.git
cd dsmtpd
make install-dev  # Configures everything automatically
make test         # Runs tests
make lint         # Checks quality
```

### A Development Workflow That Welcomes Contributors

One of the major improvements in this version is the **complete development workflow** that transforms the contributor experience. Contributing to an open source project can be intimidating, especially when you have to spend 2-3 hours just figuring out how to set up your development environment.

With dsmtpd 1.2.0, this friction completely disappears.

#### The New Contributor Experience

**Before** (typical Python project):
1. Fork and clone the repository
2. Search the README for how to install dependencies
3. Manually create a virtualenv
4. Install pip, then requirements, then the package in editable mode
5. Figure out which quality tools are used (flake8? black? ruff?)
6. Manually configure pre-commit hooks (if mentioned)
7. Run tests and discover pytest-cov is missing
8. Make your modification
9. Commit and push
10. Discover that CI is red due to a formatting issue

**Total time: 2-3 hours to make a 5-line contribution.**

**After** (dsmtpd 1.2.0):
```bash
git clone https://github.com/matrixise/dsmtpd.git
cd dsmtpd
make install-dev  # Configures EVERYTHING automatically (2 minutes)
# Make your modification
git commit        # Pre-commit hooks check quality automatically
```

**Total time: 2 minutes setup, then you code.**

If your commit passes local hooks, it will pass CI. Guaranteed.

#### Smart Makefile with Automatic Environment Management

The heart of this smooth experience is the **modern Makefile** that automatically manages the entire environment:

```bash
# Complete installation with venv + dependencies + hooks
make install-dev

# Run tests (installs dependencies if needed)
make test

# Code quality checks
make lint         # Check with ruff
make lint-fix     # Auto-fix
make format       # Format code
make typecheck    # Check types with mypy

# Build and verify package
make build
make check-dist

# Cleanup
make clean        # Remove everything (build + venv)
make clean-build  # Remove only build artifacts
make clean-venv   # Remove only virtualenv
```

**The Makefile's intelligence**: It uses a `.venv/.install-timestamp` file to track dependency modifications. Concretely:

- You run `make test` → It installs dependencies if needed, then runs tests
- You run `make test` again → It detects nothing changed, runs tests directly (10x faster)
- You modify `requirements-dev.txt` → Next `make test` automatically reinstalls

No more wondering "Do I need to reinstall dependencies?". The Makefile knows for you.

The Makefile also automatically detects Python via `asdf` or `mise` if you use these Python version management tools, ensuring consistency between developers.

#### Pre-commit Hooks with prek: Zero CI Surprises

To maintain code quality, the project uses [prek](https://github.com/j178/prek), a modern wrapper around pre-commit. **Prek is installed automatically** with `make install-dev`, you don't need to do anything manually.

Hooks run **automatically before each commit** in this order:
1. **ruff linter** with `--fix`: Automatically fixes style issues
2. **ruff format**: Formats your code according to project conventions
3. **mypy**: Checks type consistency

If a hook fails, the commit is blocked with a clear message explaining the problem. You fix it, re-commit, and it passes.

**The benefit**: No back-and-forth with CI. If your commit passes locally, it will pass on GitHub. Pull requests can be merged directly without the "commit → red CI → fix → recommit" cycle.

You can also run hooks manually to check your code before committing:

```bash
prek run -a          # Run all hooks
prek run -a --verbose # With details
```

#### Tests and Coverage

The project now has a **suite of 28 tests** covering:
- CLI options (`--port`, `--interface`, `--max-size`, `--disable-smtputf8`)
- Maildir validation
- Complete SMTP server integration
- Multipart emails
- SMTPUTF8 support

Coverage is currently at **64%**, measured with pytest-cov:

```bash
make test
# Automatically generates a coverage report
# Output: Coverage HTML written to dir htmlcov
```

This coverage may seem modest, but it's **targeted at critical behaviors**: CLI parsing, Maildir validation, email handling. The remaining code (logging, formatting) is less critical to test.

#### A Professional Experience That Inspires Confidence

All these tools aren't there just to "look good". They create a **professional contribution experience**:

- You clone → `make install-dev` → You code → Hooks validate → You merge
- No ambiguity about code conventions (ruff decides)
- No surprises in CI (local hooks == CI)
- No time wasted configuring the environment

For a project maintained by a single person, this level of polish sends an important signal: "This project is maintained seriously, your contributions will be treated professionally."

Compare with a "typical" Python project where the README just says "pip install -r requirements.txt" and you discover code conventions by reading PR review comments. The difference is night and day.

### Automated Release: From Git Tag to PyPI in 2 Minutes

Another major improvement: the **release process is now fully automated** via GitHub Actions. For a solo maintainer, this is a radical transformation.

#### The Problem with Manual Releases

Publishing a new version of a Python package is **tedious and time-consuming**. Here's the typical manual process:

1. Verify all tests pass locally
2. Update `__version__` in `__init__.py`
3. Update `CHANGES.rst` with new features
4. Commit these changes
5. Create a git tag (`git tag v1.2.0`)
6. Push the tag (`git push origin v1.2.0`)
7. Build the package locally (`python -m build`)
8. Verify the package (`twine check dist/*`)
9. Upload to TestPyPI to verify (`twine upload --repository testpypi dist/*`)
10. Test installation from TestPyPI
11. Upload to production PyPI (`twine upload dist/*`)
12. Go to GitHub to manually create the release
13. Copy-paste changelog notes into the release

**Total time: 15-20 minutes.** And above all, plenty of opportunities for error:
- Forgetting to run tests on all Python versions
- Creating a mismatch between the tag and version in code
- Forgetting to create the GitHub Release
- Uploading an untested package

The worst part? This friction makes you **procrastinate releases**. You tell yourself "I'll publish when I have 10 features" instead of publishing regularly. Users wait longer for fixes.

#### The Automated Workflow Architecture

With version 1.2.0, this entire process is **scripted and secured**. The GitHub Actions workflow uses a **sequential pipeline** architecture with 5 distinct jobs:

```
git tag v1.2.0 && git push origin v1.2.0
         ↓
   [Job 1: test]
   Tests on Python 3.10, 3.11, 3.12, 3.13, 3.14
   (in parallel, fail-fast enabled)
         ↓ (only if all tests pass)
   [Job 2: build]
   • Version == tag verification
   • Package build
   • Twine verification
   • Artifacts upload
         ↓ (only if build is valid)
   [Job 3: publish-testpypi]
   Publish to TestPyPI (test)
         ↓ (only if TestPyPI OK)
   [Job 4: publish-pypi]
   Publish to production PyPI
         ↓ (only if PyPI OK)
   [Job 5: create-release]
   Create GitHub Release with auto-generated notes
```

**"Fail-fast" security**: If a job fails, the entire chain stops. Impossible to publish to PyPI if tests fail. Impossible to create the GitHub release if PyPI publication fails.

#### Detailed Workflow Steps

When I create a git tag (e.g., `v1.2.0`) and push it, here's what happens automatically:

**1. Multi-version tests (Job 1)**
```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12", "3.13", "3.14"]
```
All tests run **in parallel** on the 5 supported Python versions. If even one fails, the workflow stops.

**2. Version/tag verification (Job 2)**
```yaml
- name: Verify version matches tag
  run: |
    VERSION=$(python -c "import dsmtpd; print(dsmtpd.__version__)")
    TAG_VERSION=${GITHUB_REF_NAME#v}
    if [ "$VERSION" != "$TAG_VERSION" ]; then
      echo "Error: Version mismatch!"
      exit 1
    fi
```
This step prevents a classic error: tagging `v1.2.0` when `__init__.py` still says `1.1.0`. The workflow refuses to continue if versions don't match.

**3. Package build and verification (Job 2)**
```bash
python -m build           # Creates .tar.gz and .whl
twine check dist/*        # Verifies packages are valid
```

**4. TestPyPI publication (Job 3)**

Before publishing to production PyPI, the package is uploaded to [TestPyPI](https://test.pypi.org/) (PyPI's test instance). This allows detecting metadata or description issues before prod.

**5. PyPI publication (Job 4)**

Once TestPyPI is validated, publication to the real PyPI. This step uses **Trusted Publishers** (see next section).

**6. GitHub Release creation (Job 5)**
```bash
gh release create v1.2.0 \
  --title "v1.2.0" \
  --generate-notes
```

The `--generate-notes` option is magic: GitHub automatically generates release notes by listing all pull requests merged since the last release. No more manual copy-pasting.

**Total time: ~2 minutes**, end to end, without manual intervention.

#### Security with Trusted Publishers: Zero Tokens, Zero Leaks

One of the most important innovations in this workflow is the use of PyPI's **Trusted Publishers** (introduced in 2023).

**The problem with API tokens**:

Traditionally, to publish to PyPI from CI, you had to:
1. Create a PyPI API token
2. Store it as a GitHub secret (`PYPI_TOKEN`)
3. Use it in the workflow: `twine upload -u __token__ -p $PYPI_TOKEN`

**The risks**:
- If the GitHub secret leaks (repo compromise, insider threat), your PyPI account is compromised
- If you share the repo with other maintainers, they all have access to the token
- You must regularly revoke and recreate the token

**Trusted Publishers: Authentication without secrets**

With Trusted Publishers, **there's no token**. Authentication is done via **OIDC (OpenID Connect)**:

1. You declare on PyPI: "I trust the workflow `.github/workflows/publish.yml` from repository `matrixise/dsmtpd`"
2. When the GitHub Actions workflow executes, GitHub provides it with a **temporary JWT token** proving its identity
3. PyPI verifies the JWT: "OK, this workflow is indeed the one declared as trusted, I accept the publication"
4. The token expires after a few minutes

Configuration in the workflow:
```yaml
publish-pypi:
  environment: pypi
  permissions:
    id-token: write  # OIDC permission to retrieve JWT token
  steps:
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      # No password, no token, just OIDC trust
```

**The advantages**:
- ✅ **Zero secrets to manage**: no token that can leak
- ✅ **Security by default**: even if someone compromises the repo, they can't publish from their laptop (JWT only works in GitHub Actions)
- ✅ **Auditability**: PyPI knows exactly which workflow published which version
- ✅ **Automatic revocation**: if you remove the Trusted Publisher on PyPI, future publications fail immediately

This has become the **recommended method** by PyPI for all projects. And dsmtpd has been using it since version 1.2.0.

#### The Maintainer Experience: From Chore to Pleasure

**Before automation** (2013-2025):
- 15-20 minutes of manual work per release
- Constant stress: "Did I forget a step?"
- Procrastination: "I'll publish when I have more features"
- Spaced-out releases (every 6-12 months)
- Maintainer burnout: "Publishing a version is a chore"

**After automation** (since 1.2.0):
```bash
# Bump version in __init__.py, commit
git commit -am "Release version 1.2.0"

# Create and push tag
git tag v1.2.0
git push origin main v1.2.0

# Wait 2 minutes, watch GitHub Actions logs
# That's it.
```

- **1 command, 2 minutes**: Release time divided by 10
- **Zero stress**: Impossible to forget a step (everything is scripted)
- **Frequent releases**: No psychological friction, you can publish as soon as a bug is fixed
- **Transparency**: GitHub Actions logs show exactly what happened
- **Confidence**: If the workflow succeeds, the release is 100% valid

For a project maintained by a single person, this automation changes everything. Instead of dreading releases, **you can publish regularly** without mental effort.

#### Impact on the Project and Community

This automation doesn't just benefit the maintainer. It has a **positive impact on the entire ecosystem**:

**For users**:
- ✅ Fixes published faster (no procrastination)
- ✅ More frequent releases with incremental changes
- ✅ Increased confidence: "This project has a professional release pipeline"

**For contributors**:
- ✅ Your pull requests are published quickly after merge
- ✅ You see your contribution appear on PyPI in 2 minutes
- ✅ Quality signal: "This project is seriously maintained"

**For the maintainer**:
- ✅ Frees up time to code instead of managing releases
- ✅ Reduces burnout (fewer repetitive manual tasks)
- ✅ Encourages continuous maintenance instead of "big bang releases"

**For project health**:
- ✅ Faster feedback cycle with users
- ✅ Fewer divergent branches (frequent releases = less drift)
- ✅ Professional image that attracts more contributors

Looking at the [release graph on GitHub](https://github.com/matrixise/dsmtpd/releases), you can clearly see the impact: before automation, 1-2 releases per year. After? As soon as there's a feature or fix, it goes out.

That's what a modern CI/CD workflow is: **reducing friction to increase velocity**.

## How to Use It Concretely

### Case 1: Django/Flask Development

```python
# settings.py (Django) or config.py (Flask)
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False  # No TLS in dev

# In another terminal
$ dsmtpd
2026-01-07 14:30:00 INFO: Starting dsmtpd 1.2.0 at 127.0.0.1:1025

# Send your emails normally
# They appear in the console:
# INFO: 127.0.0.1:54321: app@example.com -> user@test.com [Welcome Email]
```

### Case 2: Automated Tests with Maildir

```bash
# Launch dsmtpd with a Maildir to save emails
dsmtpd -d /tmp/test-emails

# In your Python tests
import mailbox

def test_welcome_email_sent():
    # Your code that sends an email
    send_welcome_email(user)

    # Verify the email was captured
    mbox = mailbox.Maildir('/tmp/test-emails')
    assert len(mbox) == 1

    email = mbox[list(mbox.keys())[0]]
    assert email['Subject'] == 'Welcome to our app!'
    assert 'Click here to activate' in email.get_payload()
```

### Case 3: Debugging Complex HTML Emails

```bash
# Save emails to open in your mail client
dsmtpd -d ~/dev-emails

# Configure Apple Mail / Thunderbird to read ~/dev-emails
# You can now visually inspect your templates
```

## When to Use dsmtpd?

**✅ Perfect for:**
- Local web application development
- Automated integration tests
- Email template debugging
- CI/CD pipelines (avoid emails in staging)
- Demos without internet connection

**❌ Not suitable for:**
- Production environment (obviously)
- Email relay to real recipients
- Real deliverability testing
- Anti-spam analysis

## Alternatives and Complements

dsmtpd isn't the only tool in this space. Here's how it compares:

- **MailHog / MailCatcher**: More UI (web interface), but heavier to install
- **smtp4dev**: Similar, but for .NET/Windows
- **mailtrap.io**: Cloud service with UI, but requires Internet and an account

dsmtpd focuses on **simplicity**: a single Python binary, no heavy dependencies, no UI (just logs), no account required.

## Try It Now

Version 1.2.0 is available on [PyPI](https://pypi.org/project/dsmtpd/):

```bash
pip install dsmtpd
dsmtpd --help
```

The project is open source (BSD license) and contributions are welcome! You can:
- Report bugs on [GitHub Issues](https://github.com/matrixise/dsmtpd/issues)
- Propose improvements via Pull Requests
- Check the [complete changelog](https://github.com/matrixise/dsmtpd/blob/main/CHANGES.rst)

## In Summary

dsmtpd 1.2.0 brings significant improvements on three axes:

**For users**:
- ✅ SMTPUTF8 support (RFC 6531) for international emails
- ✅ `--disable-smtputf8` option for legacy compatibility testing
- ✅ Python 3.10, 3.11, 3.12, 3.13, and 3.14 supported

**For contributors**:
- ✅ Smart Makefile with 11 targets (install-dev, test, lint, lint-fix, format, typecheck...)
- ✅ Automatic pre-commit hooks with prek (ruff + mypy)
- ✅ 28 automated tests for 64% coverage
- ✅ Complete documentation of CLI options and make targets

**For the maintainer**:
- ✅ Automated PyPI release via GitHub Actions
- ✅ Multi-version Python tests in CI
- ✅ Complete workflow: tag → tests → build → PyPI → GitHub Release

Whether you're developing a Django, Flask, FastAPI application, or any Python project sending emails, dsmtpd makes email testing **simple, fast, and risk-free**.

No more crossing your fingers before running your test script. Never again a test email sent to the wrong recipient.

And if you want to contribute, the development workflow is now **professional and welcoming**: clone, run `make install-dev`, and you're ready.

Try it out, and don't hesitate to share your feedback!

---

*Stéphane Wirtel – Maintainer of dsmtpd since 2013*
*GitHub: [@matrixise](https://github.com/matrixise)*