# Contributing

Thanks for contributing! Here's what you need to know.

## Setup
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
make install
```

## Workflow

1. Create a branch: `git checkout -b feat/your-feature`
2. Make your changes and write tests
3. Run `make check && make test`
4. Open a Pull Request against `main`

## Branch naming

| Prefix | Use for |
|--------|---------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation only |
| `chore/` | Tooling, deps, CI |
| `refactor/` | Code restructuring |

## Commit messages

Follow Conventional Commits:
- `feat: add data loader`
- `fix: handle missing values`
- `docs: update README`

## Code standards

- All code must pass `ruff` and `mypy`
- New features must include tests
- Public functions must have docstrings