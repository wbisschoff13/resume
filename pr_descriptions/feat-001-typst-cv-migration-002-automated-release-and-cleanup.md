This PR completes the migration from LaTeX to Typst by cleaning up all legacy artifacts and replacing the LaTeX-based CI pipeline with a Typst-native release workflow.

**Why**

The repository has migrated its CV source from LaTeX (`awesome-cv.cls` + `.tex` files) to Typst (`.typ` files). Typst offers faster compilation, a simpler syntax, and a modern build pipeline. This PR removes the ~2,800 lines of LaTeX cruft and retools the CI pipeline to match the new toolchain — ensuring that releases are generated correctly and no stale LaTeX configuration remains to confuse future maintainers.

**What changed**

- **CI Pipeline** (`.github/workflows/release.yml`): Replaced `xu-cheng/latex-action@v3` with `typst-community/setup-typst@v5`. Added a matrix build strategy that compiles all four entry points (`cv.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, `cover_letter.typ`) in parallel. Narrowed the tag trigger to semantic versioning only (`v*.*.*`). Added a font installation step for custom fonts on the Ubuntu runner.

- **Legacy Cleanup**: Removed 35 `.tex` files, the `awesome-cv.cls` class file, Docker build infrastructure (`docker/Dockerfile`, `docker/build.sh`), and dev tooling configs (`.devcontainer/`, `.vscode/`). Deleted the `example/` directory and all LaTeX auxiliary content. Preserved `content/data.typ` and `lib/template.typ` (owned by ISS-001) and advisory files (`analysis/`, `amazon-lp-cheatsheet-draft.md`).

- **`.gitignore`**: Added Typst cache (`.typst/`) and build artifact patterns. Removed stale LaTeX auxiliary patterns (`*.aux`, `*.out`, `*.synctex.gz`).

**Outcome**

- 48 files changed, +388 / −2,778
- Zero `.tex` or `.cls` files remaining
- CI builds all CV variants on tag pushes and attaches them to a GitHub Release
- `mise run check` passes with no regressions
