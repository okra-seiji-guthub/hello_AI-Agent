# Repair Git Worktrees After a Dev Container Rebuild

After rebuilding or restarting a Dev Container, `git worktree list` may mark linked worktrees as pruneable even though the directories still exist. This usually means the worktree path pointers still use the Windows host path instead of the Linux path inside the container.

Do **not** run `git worktree prune`. That only removes Git's worktree registration. The working trees remain on disk, but Git no longer tracks them.

## Symptom

```text
git worktree list -v
```

Example:

```text
/workspaces/hello_AI-Agent                                          ... [main]
C:/gm/work/AiWork/03-AIAgent/hello_AI-Agent/.worktrees/chore-001    ... [chore/001-use-uv-instead-of-pip]
	prunable: gitdir file points to non-existent location
C:/gm/work/AiWork/03-AIAgent/hello_AI-Agent/.worktrees/feature-001  ... [feature/001-multi-agents]
	prunable: gitdir file points to non-existent location
```

The directories under `.worktrees/` are still present. Only the recorded absolute paths are wrong.

## Cause

Git stores absolute paths in two administrative files for each linked worktree:

- `.worktrees/<name>/.git` points at `.git/worktrees/<name>`
- `.git/worktrees/<name>/gitdir` points at `.worktrees/<name>/.git`

If those worktrees were created on Windows, the files keep host paths such as `C:/gm/work/...`. Inside the Dev Container those paths do not exist, so Git reports `gitdir file points to non-existent location`.

`git worktree move` cannot fix this, because the registered old path is already missing in the container.

## Repair

Use `git worktree repair` from the main repository and pass the **current Linux directories**.

```bash
cd /workspaces/hello_AI-Agent

git worktree repair \
  .worktrees/feature-001 \
  .worktrees/chore-001
```

Git updates both sides of the path mapping. Add or remove arguments to match the worktrees you actually have.

Git 2.36 or later is required. This environment uses Git 2.43.0.

## Verify

```bash
git worktree list -v
git -C .worktrees/feature-001 status
git -C .worktrees/chore-001 status
```

Success looks like this (`prunable` is gone, paths are under `/workspaces`):

```text
/workspaces/hello_AI-Agent                         ... [main]
/workspaces/hello_AI-Agent/.worktrees/chore-001    ... [chore/001-use-uv-instead-of-pip]
/workspaces/hello_AI-Agent/.worktrees/feature-001  ... [feature/001-multi-agents]
```

## Avoid

- `git worktree prune` while the directories still exist and you want to keep them linked
- `git worktree move` from a Windows path that the container cannot see
- Creating worktrees on the Windows host if you mainly work inside the Dev Container

To reduce recurrence, create and manage worktrees from inside the container so Git records `/workspaces/...` paths.

## Fallback

If `repair` fails, rewrite the two pointer files for each worktree, then re-run `git worktree list -v`.

```bash
printf 'gitdir: /workspaces/hello_AI-Agent/.git/worktrees/feature-001\n' \
  > .worktrees/feature-001/.git
printf '/workspaces/hello_AI-Agent/.worktrees/feature-001/.git\n' \
  > .git/worktrees/feature-001/gitdir
```

Prefer `git worktree repair` when it works.
