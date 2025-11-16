# Claude Command: Commit

This command helps you create well-formatted commits with conventional commit messages and emoji.

## Usage

To create a commit, just type:
```
/commit
```

## What This Command Does

1. Checks which files are staged with `git status`
2. If no files are staged, automatically adds all modified and new files with `git add`
3. Performs a `git diff` to understand what changes are being committed
4. Analyzes the diff to determine if multiple distinct logical changes are present
5. If multiple distinct changes are detected, suggests breaking the commit into multiple smaller commits
6. For each commit (or the single commit if not split), creates a commit message using emoji conventional commit format

## Best Practices for Commits

- **Atomic commits**: Each commit should contain related changes that serve a single purpose
- **Split large changes**: If changes touch multiple concerns, split them into separate commits
- **Conventional commit format**: Use the format `emoji <type>: <description>`
- **Present tense, imperative mood**: Write commit messages as commands (e.g., "add feature" not "added feature")
- **Concise first line**: Keep the first line under 72 characters
- **No Claude attribution**: NEVER mention Claude or Claude Code in commit messages

## Commit Types and Emojis

Use ONE emoji per commit based on the primary type of change:

- ✨ `feat`: New feature or functionality
- 🐛 `fix`: Bug fix (non-critical)
- 🚑️ `fix`: Critical hotfix
- 📝 `docs`: Documentation changes
- 🎨 `style`: Code structure/formatting improvements
- ♻️ `refactor`: Code refactoring (no behavior change)
- 🚚 `refactor`: Move or rename files/resources
- ⚡️ `perf`: Performance improvements
- ✅ `test`: Add or update tests
- 🔧 `chore`: Configuration, tooling, maintenance
- 🔥 `chore`: Remove code or files
- 📦️ `chore`: Update dependencies or packages
- ➕ `chore`: Add a dependency
- ➖ `chore`: Remove a dependency
- 🚀 `ci`: CI/CD changes
- 💚 `fix`: Fix CI build
- 🔒️ `fix`: Security fixes
- ♿️ `feat`: Accessibility improvements

## Guidelines for Splitting Commits

When analyzing the diff, consider splitting commits based on these criteria:

1. **Different concerns**: Changes to unrelated parts of the codebase
2. **Different types of changes**: Mixing features, fixes, refactoring, etc.
3. **File patterns**: Changes to different types of files (e.g., source code vs documentation)
4. **Logical grouping**: Changes that would be easier to understand or review separately
5. **Size**: Very large changes that would be clearer if broken down

## Examples

**Good commit messages for this blog/CV project:**
- ✨ feat: add new blog post about Python decorators
- 🐛 fix: correct broken links in conference talks section
- 📝 docs: update README with new deployment instructions
- ♻️ refactor: simplify CV generation template logic
- 🎨 style: improve blog post formatting and readability
- 🔥 chore: remove deprecated Hugo shortcodes
- 📦️ chore: update Hugo theme to latest version
- ➕ chore: add frontmatter dependency for content processing
- 🚑️ fix: patch critical XSS vulnerability in contact form
- 🚀 ci: update Netlify build configuration for Hugo 0.148.2
- 💚 fix: resolve failing GitHub Actions workflow
- 🔒️ fix: update dependencies with security patches
- ♿️ feat: improve navigation accessibility for screen readers

**Example of splitting commits:**

If you modify both the CV template AND add a new blog post, split into:
1. ✨ feat: add blog post about Hugo migration
2. ♻️ refactor: update CV template structure

If you fix multiple unrelated issues, split into:
1. 🐛 fix: correct date formatting in blog posts
2. 🐛 fix: resolve broken image links in talks section
3. 💚 fix: update GitHub Actions Python version

## Important Notes

- If specific files are already staged, the command will only commit those files
- If no files are staged, it will automatically stage all modified and new files
- The commit message will be constructed based on the changes detected
- Before committing, the command will review the diff to identify if multiple commits would be more appropriate
- If suggesting multiple commits, it will help you stage and commit the changes separately
- **CRITICAL**: Never add "Generated with Claude Code" or similar attributions to commits
