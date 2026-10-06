"""M02.L01 — Mastering Version Control with Git and GitHub.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 3, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Version Control with Git and GitHub"

MODULE_DESCRIPTION = (
    "Learn how Git models project history, create focused commits, synchronize "
    "with remotes, collaborate safely with branches and GitFlow, use GitHub pull "
    "requests and code reviews, and resolve merge conflicts confidently."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Page numbers not provided in supplied chapter export"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Mastering Version Control with Git and GitHub",

    "slug": "mastering-git-github-m02-l01",

    "description": (
        "Build a practical mental model of Git, then use it in a realistic GitHub "
        "collaboration workflow involving commits, remotes, branches, pull requests, "
        "code review, and merge-conflict resolution."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "git",
        "github",
        "version-control",
        "branching",
        "gitflow",
        "pull-requests",
        "code-review",
        "merge-conflicts",
        "collaboration",
        "module-02",
    ],

    "prerequisite_ids": ["M01.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Mastering Version Control with Git and GitHub",

        "content": r"""
# Mastering Version Control with Git and GitHub

> **Course:** Cloud & DevOps Foundations  
> **Lesson:** M02.L01  
> **Module:** Version Control with Git and GitHub  
> **Source alignment:** BOOK-XXX, Chapter 3. Page numbers were not provided in the supplied chapter export. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain Git as a snapshot-based distributed version control system.
- Distinguish the working directory, staging area, and local repository.
- Use `git status`, `git add`, and `git commit` to create focused project history.
- Explain the purpose of `git diff` and `git log` before sharing changes.
- Distinguish local repositories from remote repositories.
- Explain what `git push`, `git pull`, and `git fetch` do.
- Describe why branches allow teams to work safely in parallel.
- Explain the main, develop, feature, release, and hotfix branches used in GitFlow.
- Clone a GitHub repository and create a feature branch.
- Push a feature branch to GitHub and open a pull request.
- Explain why code review improves quality, knowledge sharing, and consistency.
- Resolve a basic merge conflict by reading Git's conflict markers and choosing the intended final content.
- Apply a professional Git checklist that reduces common collaboration mistakes.

---

## 1. Git is a history system, not just a save button

A normal folder remembers only its current state.

If you edit `index.html`, save it, and close the editor, the operating system gives you the latest file. Unless you created backups manually, it does not naturally provide a structured story of how that file evolved.

Git adds that history.

A useful beginner definition is:

> **Git is a distributed version control system that records meaningful snapshots of a project's state over time.**

This matters because software is constantly changing.

A team may need to answer:

- Who changed this line?
- Why was this file modified?
- Which version introduced a bug?
- What did the project look like last week?
- Can we safely experiment without damaging the stable version?
- How do several developers combine their work?

Git provides a structured way to answer those questions.

### Git thinks in snapshots

The source emphasizes that Git's mental model is closer to a sequence of snapshots than a simple list of independent file edits.

Imagine a small project:

```text
Snapshot A
README.md
index.html

        ↓ new commit

Snapshot B
README.md
index.html
style.css

        ↓ new commit

Snapshot C
README.md
index.html
style.css
app.js
```

Each commit identifies a meaningful project state.

That does **not** mean Git blindly copies the entire folder in an inefficient way every time. The important learner-facing idea is that Git lets you reason about each commit as a project snapshot.

### Local history is already useful

You do not need GitHub for Git to work.

A local Git repository can already:

- record commits,
- create branches,
- inspect history,
- compare versions,
- merge work.

GitHub becomes important when you want a hosted remote repository and collaboration features such as pull requests and code review.

This distinction will matter throughout the lesson:

```text
Git    = version-control system
GitHub = hosted collaboration platform built around Git repositories
```

---

## 2. The three trees: how changes move through Git

One of the most important Git concepts is that your work exists in three main areas.

They are often called Git's **three trees**:

1. Working Directory
2. Staging Area
3. Repository

{{image:git-three-trees}}

### 2.1 Working Directory

The **working directory** is the project folder you actually edit.

Suppose your project contains:

```text
my-project/
├── README.md
├── index.html
└── style.css
```

When you open `index.html` in VS Code and change a heading, that modification exists in the working directory.

At this point, Git can detect the change, but the change is not yet part of the next committed snapshot.

Think:

> **Working directory = what I am currently editing.**

### 2.2 Staging Area

The **staging area**, also called the **index**, lets you choose exactly what should enter the next commit.

This is one of Git's most useful features.

Suppose you changed two files:

```text
index.html  -> finished feature
style.css   -> unfinished experiment
```

You do not have to commit both.

You can stage only:

```bash
git add index.html
```

Now your next commit can contain the completed HTML change while the unfinished CSS work stays outside the commit.

Think:

> **Staging area = what I have selected for the next snapshot.**

### 2.3 Repository

The local **repository** is stored inside the hidden `.git` directory.

It contains Git's project history and metadata, including:

- commits,
- branches,
- tags,
- references.

When you run:

```bash
git commit
```

Git records the staged content as a new commit in the repository.

Think:

> **Repository = what I have permanently recorded in local project history.**

### The flow

```text
Edit files
   ↓
Working Directory
   |
   | git add
   v
Staging Area
   |
   | git commit
   v
Local Repository
```

This mental model prevents a huge amount of beginner confusion.

A file can be:

- untracked,
- modified but unstaged,
- staged,
- committed and clean.

The command that helps you understand the current state is `git status`.

---

## 3. Your core local workflow: init, status, add, commit

Let's turn a normal folder into a Git repository.

### 3.1 Initialize a repository

Navigate to a project folder:

```bash
cd ~/devops-book-projects/my-first-website
```

Then run:

```bash
git init
```

This creates the hidden `.git` directory.

Conceptually:

```text
Before:
ordinary folder

After git init:
ordinary working files
+
.git history database
```

Your project is now a Git repository.

### 3.2 Inspect first with `git status`

Run:

```bash
git status
```

This command tells you things such as:

- your current branch,
- untracked files,
- modified files,
- staged files,
- whether your working tree is clean.

The source describes `git status` as a command you will use constantly.

That is good practice because Git commands often depend on **where you are and what state the repository is in**.

Before changing repository state, first inspect it.

### `main` versus `master`

You may encounter repositories whose default branch is named:

```text
main
```

and older repositories using:

```text
master
```

The branch behaves the same way in Git; the important thing is to use the name the repository actually has.

This course uses `main`.

### 3.3 Stage changes with `git add`

To stage everything under the current directory:

```bash
git add .
```

To stage one file:

```bash
git add index.html
```

Then inspect again:

```bash
git status
```

A disciplined workflow looks like this:

```text
edit
 ↓
git status
 ↓
git add selected files
 ↓
git status
```

The second status check confirms that the correct changes are staged.

### 3.4 Create a commit

Once the staging area contains one logical unit of work:

```bash
git commit -m "Initial commit: Add project structure and README"
```

A commit message should explain the change clearly enough that future readers can understand the project history.

Poor message:

```text
stuff
```

Better message:

```text
feat: add homepage navigation
```

Another good message:

```text
fix: handle missing user profile
```

The source later introduces prefixes such as:

- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation

These conventions can make history easier to scan.

### What does "clean" mean?

After committing all current changes:

```bash
git status
```

may report:

```text
nothing to commit, working tree clean
```

That means there are no new working-directory or staging-area changes waiting to be committed.

### Review before sharing

Two commands from the source are especially helpful.

#### `git diff`

```bash
git diff
```

Use it to inspect unstaged line-by-line changes.

#### `git log`

```bash
git log
```

Use it to inspect commit history, including information such as commit hashes, authors, dates, and messages.

A strong habit is:

```text
status → diff → stage → status → commit → log
```

{{exercise:M02.L01.EX01}}

---

## 4. Local and remote repositories: push, pull, and fetch

Local Git history is powerful, but collaboration needs a shared location.

A **remote repository** is another copy of the repository stored elsewhere, commonly on a platform such as GitHub.

A common relationship is:

```text
Your machine
Local repository
      ⇅
GitHub
Remote repository
```

### 4.1 Push: send your commits outward

`git push` sends local commits to a remote repository.

Think:

```text
local commits → remote
```

For example, after setting up a remote:

```bash
git push
```

or, for a new branch:

```bash
git push -u origin feature/add-homepage
```

The source explains that `-u` establishes a tracking relationship between your local branch and the corresponding remote branch.

### 4.2 Pull: bring remote changes into your branch

`git pull` updates your current local branch with remote work.

Think:

```text
remote changes → local current branch
```

The source explains `git pull` conceptually as:

```text
git fetch
    +
merge
```

That means Git downloads remote changes and then integrates them into your current branch.

### 4.3 Fetch: download without immediately merging

If you want to inspect remote changes first:

```bash
git fetch
```

This updates remote-tracking information without immediately changing your current working branch.

The source gives an example of reviewing remote history such as:

```bash
git log origin/main
```

This is useful when you want to understand what changed before integrating it.

### Pull versus fetch

| Command | Downloads remote changes? | Immediately integrates into current branch? |
|---|---:|---:|
| `git fetch` | Yes | No |
| `git pull` | Yes | Yes |

### A note about merge and rebase

The chapter introduces **rebase** only briefly.

The key distinction presented is:

- **merge** preserves the histories of the branches and combines them,
- **rebase** replays commits onto another base to create a more linear history.

For this beginner lesson, use merging as the primary workflow. Rebase is best understood after you are comfortable with branches, commits, and merges.

### Authentication concept

The source notes that GitHub HTTPS authentication does not use a normal account password for Git operations.

The important learning point is:

> Git author identity and GitHub authentication are different things.

These configure commit identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

They do **not** log you into GitHub by themselves.

### If `code .` is unavailable

The source also notes that the VS Code command-line launcher must be available on your PATH for:

```bash
code .
```

to open the current directory in VS Code.

The exact setup can vary by operating system, but the concept is simple:

```text
code .
```

means:

> Open this current folder (`.`) as a VS Code workspace.

---

## 5. Branching: isolate work without destabilizing the main code

If commits answer:

> "How do I record history?"

branches answer:

> "How do several streams of work coexist?"

A **branch** is an independent line of development represented by a movable reference to commits.

### Why branches matter

Imagine three developers working directly on `main`:

```text
Developer A → half-finished payment feature
Developer B → urgent login fix
Developer C → large refactor
```

If all changes are mixed immediately into one shared branch, the code can become difficult to stabilize.

Branches isolate work.

```text
main
 |
 +---- feature/payment
 |
 +---- fix/login
 |
 +---- feature/refactor
```

Each branch can progress without immediately changing the stable main line.

After a branch is reviewed and ready, its changes can be merged.

### GitFlow as a structured branching model

The source introduces **GitFlow** as a structured strategy.

It also notes an important nuance: some modern teams, especially those optimized for continuous deployment, use simpler branch models.

So do not interpret GitFlow as the only correct strategy.

Its value here is that it teaches clear roles for different branch types.

{{image:gitflow}}

### 5.1 `main`

`main` represents stable released code in the GitFlow model described by the source.

A useful mental rule is:

> `main` should stay trustworthy.

That is why collaborative teams often avoid direct day-to-day feature commits to `main`.

### 5.2 `develop`

`develop` is the integration branch for work intended for the next release.

Feature work is integrated here before release preparation.

### 5.3 Feature branches

Example:

```text
feature/add-login-page
```

A feature branch:

- starts from `develop`,
- contains work for one feature,
- returns to `develop` when complete.

Conceptually:

```text
develop
   \
    feature/add-login-page
             |
             | work + commits
             v
         merge to develop
```

### 5.4 Release branches

Example:

```text
release/v1.2.0
```

A release branch is used to prepare a release.

The source emphasizes:

- no new features should be added,
- final bug fixes and release tasks happen here,
- the finished release merges into `main`,
- relevant fixes also return to `develop`.

### 5.5 Hotfix branches

Example:

```text
hotfix/fix-critical-bug
```

A hotfix starts from `main` because it addresses a production problem.

After the fix:

- merge into `main`,
- also merge into `develop`.

Why both?

Because the production fix should not disappear from future development.

### GitFlow summary

| Branch | Starts from | Main purpose | Usually merges into |
|---|---|---|---|
| `main` | Long-lived | Stable released code | — |
| `develop` | Long-lived | Integration for next release | — |
| `feature/*` | `develop` | New feature work | `develop` |
| `release/*` | `develop` | Stabilize next release | `main` and `develop` |
| `hotfix/*` | `main` | Urgent production repair | `main` and `develop` |

{{exercise:M02.L01.EX02}}

---

## 6. Hands-on GitHub workflow: clone, branch, commit, push

Now connect local Git to GitHub.

The source uses a simple repository named:

```text
my-devops-project
```

### 6.1 Create a GitHub repository

The chapter's example creates a new repository and initializes it with a README.

The important concept is that the remote repository now has an initial commit.

Once a remote repository exists, you can bring it to your machine.

[[IMAGE_NEEDED: GitHub new-repository screen | A GitHub repository-creation page showing repository name, description, visibility choice, README initialization option, and create button | Learner should notice the minimum settings needed to initialize a repository before cloning it]]

### 6.2 Clone the repository

Copy the repository's HTTPS URL and run:

```bash
git clone https://github.com/YourUsername/my-devops-project.git
```

`git clone` does more than download files.

It creates a local Git repository that already knows about the remote.

Git commonly names that remote:

```text
origin
```

So conceptually:

```text
origin = default nickname for the remote repository you cloned from
```

Then:

```bash
cd my-devops-project
```

### 6.3 Create a feature branch

The source uses:

```bash
git checkout -b feature/add-homepage
```

This both:

1. creates the branch,
2. switches to it.

Now your new work is isolated from `main`.

### 6.4 Add a simple file

For example:

```bash
touch index.html
```

Then edit it in VS Code:

```bash
code .
```

The chapter uses simple HTML such as:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My DevOps Project</title>
</head>
<body>
    <h1>Welcome to My Project!</h1>
    <p>This is the new homepage.</p>
</body>
</html>
```

The important part is not the HTML.

The important part is the Git workflow around it.

### 6.5 Inspect, stage, and commit

```bash
git status
git add index.html
git commit -m "feat: Add initial index.html homepage"
```

Notice the order:

```text
inspect
  ↓
stage intentionally
  ↓
commit meaningfully
```

### 6.6 Push the branch

```bash
git push -u origin feature/add-homepage
```

Now GitHub has the branch and its commit.

At this point:

```text
Local feature branch
        |
        | push
        v
Remote feature branch on GitHub
```

But the change is still **not** part of `main`.

That is intentional.

The next step is review.

---

## 7. Pull requests and code review

A **Pull Request (PR)** is a proposal to merge changes from one branch into another.

In the chapter's example:

```text
feature/add-homepage
        ↓
      PR
        ↓
      main
```

A PR is not merely a "merge button."

It creates a collaboration space where the team can:

- explain the change,
- inspect the diff,
- discuss implementation choices,
- request revisions,
- run automated checks,
- approve or reject the merge.

{{image:pull-request}}

### 7.1 Write a useful PR description

A helpful PR explains:

- **what** changed,
- **why** it changed,
- **how** to test it.

For example:

```text
This PR adds the initial homepage for the project.

Why:
We need a basic landing page before adding navigation.

How to test:
Open index.html and confirm the heading and introductory text render correctly.
```

The description helps reviewers understand intent before reading implementation details.

### 7.2 Why code review matters

The source identifies several major benefits.

#### Improve code quality

Another person may catch:

- incorrect logic,
- bugs,
- unclear naming,
- performance issues,
- missing edge cases.

#### Share knowledge

Review spreads understanding across the team.

Without review, one developer may become the only person who understands a critical section of the system.

#### Maintain consistency

Review helps teams enforce shared patterns.

Examples:

- naming conventions,
- architecture decisions,
- formatting,
- testing expectations.

#### Strengthen collaboration

A PR turns code into a team conversation.

The chapter stresses that a good review should be constructive.

Less useful:

```text
This is wrong.
```

More useful:

```text
Could we extract this validation into a helper function?
It may make the handler easier to test and reuse.
```

The goal is not to "win" the review.

The goal is to improve the shared codebase.

### 7.3 Automated checks

The chapter also connects PRs to CI.

A repository may require automated checks such as:

- tests,
- linters,
- build verification,

before merging.

That creates a safety layer:

```text
Feature branch
      ↓
Pull Request
      ↓
Human review
      +
Automated checks
      ↓
Merge allowed
```

### 7.4 Protected main branches

The source describes branch protection as a professional pattern.

A protected `main` can require:

- pull requests,
- approvals,
- successful CI checks,

instead of allowing unrestricted direct pushes.

This supports the DevOps goal of fast delivery **with guardrails**.

### 7.5 Merge and clean up

Once the PR is approved and required checks pass, merge it.

The completed feature becomes part of `main`.

The temporary feature branch can then be deleted to keep the branch list clean.

{{exercise:M02.L01.EX03}}

---

## 8. Merge conflicts: when Git needs a human decision

A merge conflict is not a sign that Git is broken.

It means Git has found two competing changes and cannot safely infer which final result you want.

### How a conflict happens

Suppose the original file contains:

```text
Welcome to our project
```

You create Branch A and change it to:

```text
Welcome to our awesome project
```

A teammate creates Branch B and changes the same line to:

```text
Welcome to our new project
```

If Branch B reaches `main` first, then your branch and `main` now disagree about the same original line.

Git can combine many independent changes automatically.

But here it must ask:

> Which text should survive?

### 8.1 Bring current `main` to your machine

The source's workflow begins by updating local `main`:

```bash
git checkout main
git pull origin main
```

Now your local `main` contains the teammate's merged change.

### 8.2 Return to your feature branch

```bash
git checkout feature/update-readme-A
```

### 8.3 Merge `main` into your feature

```bash
git merge main
```

Git may report a conflict in `README.md`.

The file can then contain markers like:

```text
<<<<<<< HEAD
Welcome to our awesome project.
=======
Welcome to our new project.
>>>>>>> main
```

Read these markers carefully.

The upper block is the current branch's version.

The lower block is the incoming version from `main`.

### 8.4 Resolve the meaning, not just the markers

Do **not** think:

> "Which button removes the error?"

Think:

> "What should the final file actually say?"

Possible result:

```text
Welcome to our new, awesome project.
```

You may:

- keep your version,
- keep the incoming version,
- combine both,
- write a new correct version.

Then remove the conflict markers.

VS Code can make this easier by highlighting conflicts and offering actions such as accepting the current, incoming, or both changes.

But you remain responsible for deciding the correct final content.

### 8.5 Stage the resolution

After editing:

```bash
git add README.md
```

This tells Git:

> I have resolved this file.

### 8.6 Complete the merge

```bash
git commit
```

Now the merge resolution is recorded.

### 8.7 Push the updated branch

```bash
git push origin feature/update-readme-A
```

The pull request can now reevaluate the branch with the conflict resolved.

[[IMAGE_NEEDED: Git merge-conflict markers | A code-editor view showing `<<<<<<< HEAD`, `=======`, and `>>>>>>> main`, with annotations identifying current change, incoming change, and the final manually resolved line | Learner should notice that Git presents both competing versions and requires a human to decide the intended final content]]

### Conflicts are normal

The correct response to a conflict is not panic.

Use a repeatable process:

```text
1. Inspect status
2. Identify conflicted files
3. Read both versions
4. Decide intended final content
5. Remove conflict markers
6. Stage resolved files
7. Commit resolution
8. Test
9. Push
```

{{exercise:M02.L01.EX04}}

---

## 9. Professional Git habits that prevent common mistakes

The chapter ends with a compact set of habits worth turning into muscle memory.

### Habit 1 — run `git status`

Before committing, merging, or switching context:

```bash
git status
```

Confirm:

- current branch,
- modified files,
- staged files,
- untracked files.

This simple check prevents many avoidable mistakes.

### Habit 2 — write meaningful commit messages

History is documentation.

Six months later:

```text
stuff
```

tells you almost nothing.

But:

```text
fix: resolve null handling in login flow
```

gives the future reader useful context.

### Habit 3 — keep your branch current before sharing

The source recommends pulling before pushing so conflicts can surface locally.

The underlying principle is:

> Integrate teammates' changes deliberately instead of assuming your branch is the only source of truth.

### Habit 4 — avoid direct feature work on `main`

Use dedicated branches.

Then merge through a reviewed pull request.

This keeps `main` predictable and gives changes a place for review.

### Habit 5 — make focused commits

A strong commit represents one understandable unit of change.

Less useful:

```text
Commit:
- add login
- change database schema
- rename 40 files
- rewrite README
- test random experiment
```

Better:

```text
commit 1: feat: add login form
commit 2: feat: validate login credentials
commit 3: docs: document login setup
```

Focused commits are easier to:

- review,
- understand,
- revert,
- debug.

### Habit 6 — inspect before you act

A practical Git loop is:

```text
git status
    ↓
git diff
    ↓
git add <intentional files>
    ↓
git status
    ↓
git commit
    ↓
git log
```

When collaborating:

```text
update branch
    ↓
make focused change
    ↓
commit
    ↓
push feature branch
    ↓
open PR
    ↓
review + checks
    ↓
merge
```

---

## Important misconceptions

### Misconception 1

> "Saving a file means Git saved it."

### Why this is wrong

Saving updates the working-directory file.

Git does not record the change in repository history until you stage and commit it.

---

### Misconception 2

> "`git add` permanently saves my work."

### Why this is wrong

`git add` places selected changes in the staging area.

`git commit` records the staged snapshot in local history.

---

### Misconception 3

> "Git and GitHub are the same product."

### Why this is wrong

Git is the version-control system.

GitHub hosts Git repositories and adds collaboration features such as pull requests, code reviews, issues, permissions, and automated checks.

---

### Misconception 4

> "`git pull` and `git fetch` do exactly the same thing."

### Why this is wrong

Both can download remote information, but `git pull` also integrates those changes into the current branch, while `git fetch` lets you inspect them first.

---

### Misconception 5

> "A merge conflict means one developer made a mistake."

### Why this is wrong

A conflict can happen during perfectly normal parallel development when two branches change overlapping content.

Git is asking for a human decision because intent cannot be inferred safely.

---

### Misconception 6

> "GitFlow is the only professional branching strategy."

### Why this is wrong

The source presents GitFlow as a valuable structured model, while also noting that some modern teams use simpler strategies, especially in continuous-deployment environments.

The important skill is understanding why a team uses its chosen branching model.

---

## Key terminology

| Term | Meaning |
|---|---|
| Version Control System (VCS) | System for tracking and managing changes to project files over time |
| Git | Distributed version control system used to track project history |
| GitHub | Hosted platform for Git repositories and team collaboration |
| Working Directory | The project files you are currently editing |
| Staging Area / Index | Selected changes prepared for the next commit |
| Repository | Git's stored project history and metadata |
| `.git` | Hidden directory containing the local Git repository data |
| Commit | Recorded snapshot in repository history |
| Commit hash | Unique identifier for a commit |
| `git status` | Command that reports branch and working/staging state |
| `git diff` | Command for inspecting line-level changes |
| `git log` | Command for browsing commit history |
| Remote | A repository location outside the current local repository |
| `origin` | Common default name for the remote repository created by cloning |
| Push | Send local commits to a remote |
| Pull | Download and integrate remote changes into the current local branch |
| Fetch | Download remote changes without immediately integrating them |
| Branch | Independent line of development represented by a movable reference |
| `main` | Common name for the primary stable branch |
| `develop` | GitFlow integration branch for upcoming development |
| Feature branch | Temporary branch for a new feature |
| Release branch | GitFlow branch for stabilizing a release |
| Hotfix branch | GitFlow branch for urgent production fixes |
| Clone | Create a local copy of a remote Git repository |
| Pull Request (PR) | Proposal and review workflow for merging one branch into another |
| Code review | Human examination and discussion of proposed code changes |
| Branch protection | Repository rule restricting how changes reach protected branches |
| Merge conflict | Situation where Git cannot automatically combine competing changes |
| `HEAD` | Reference to the currently checked-out position/branch context |

---

## Self-check

Before continuing, make sure you can answer:

1. What does it mean to say Git records project history as snapshots?
2. What is the difference between the working directory and staging area?
3. What happens when you run `git add index.html`?
4. What happens when you run `git commit`?
5. Why should you run `git status` frequently?
6. What information can `git diff` and `git log` help you inspect?
7. What is a remote repository?
8. What is the difference between `git fetch` and `git pull`?
9. Why do teams use feature branches?
10. In GitFlow, where does a feature branch normally start and where does it return?
11. Why does a hotfix merge into both `main` and `develop`?
12. What does `origin` usually refer to after cloning?
13. What problem does a pull request solve beyond simply merging code?
14. Why are code reviews useful even when automated tests pass?
15. What causes a merge conflict?
16. What do the `<<<<<<<`, `=======`, and `>>>>>>>` markers mean?
17. After manually fixing a conflicted file, why do you run `git add` again?
18. Why are small focused commits easier to maintain than one giant commit?

---

## Retain this idea

**Git lets you deliberately move work from editing, to staging, to history; branches and GitHub then extend that discipline into safe team collaboration.**
""",

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "git-mental-model",
                "title": "Git is a history system, not just a save button",
                "order": 1,
            },
            {
                "id": "three-trees",
                "title": "The three trees: how changes move through Git",
                "order": 2,
            },
            {
                "id": "local-workflow",
                "title": "Your core local workflow: init, status, add, commit",
                "order": 3,
            },
            {
                "id": "remotes",
                "title": "Local and remote repositories: push, pull, and fetch",
                "order": 4,
            },
            {
                "id": "branching-gitflow",
                "title": "Branching: isolate work without destabilizing the main code",
                "order": 5,
            },
            {
                "id": "github-workflow",
                "title": "Hands-on GitHub workflow: clone, branch, commit, push",
                "order": 6,
            },
            {
                "id": "pull-requests",
                "title": "Pull requests and code review",
                "order": 7,
            },
            {
                "id": "merge-conflicts",
                "title": "Merge conflicts: when Git needs a human decision",
                "order": 8,
            },
            {
                "id": "professional-habits",
                "title": "Professional Git habits that prevent common mistakes",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Build a Clean Local Commit",

            "lesson_code": "M02.L01",

            "section_id": "local-workflow",

            "placement": "after_section",

            "description": (
                "Practice moving changes deliberately through the working directory, "
                "staging area, and local repository."
            ),

            "instructions": (
                "1. Create a new directory named git-three-trees-lab and initialize it with git init.\n"
                "2. Create README.md and notes.txt.\n"
                "3. Add one line to each file.\n"
                "4. Run git status and record what Git reports.\n"
                "5. Stage only README.md.\n"
                "6. Run git status again and explain why README.md and notes.txt are now in different states.\n"
                "7. Commit README.md with a meaningful message.\n"
                "8. Run git status and git log.\n"
                "9. Explain where notes.txt exists in Git's three-tree mental model."
            ),

            "expected_output": (
                "A command transcript plus a short explanation of the working directory, "
                "staging area, and repository state after each major step."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "git-init",
                "git-status",
                "git-add",
                "git-commit",
                "three-trees",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Design a GitFlow Branch Map",

            "lesson_code": "M02.L01",

            "section_id": "branching-gitflow",

            "placement": "after_section",

            "description": (
                "Use the GitFlow model to decide where different kinds of work should begin "
                "and where they should merge."
            ),

            "instructions": (
                "Scenario: version 2.0 is being developed while version 1.9 is in production.\n"
                "1. A developer starts a new search feature. Choose its branch type and starting branch.\n"
                "2. The team is preparing version 2.0 for release. Choose the branch type and merge destinations.\n"
                "3. Production version 1.9 has a critical authentication bug. Choose the branch type and starting branch.\n"
                "4. Explain why the authentication fix must also reach future development.\n"
                "5. Draw a small text diagram showing main, develop, and the three supporting branches."
            ),

            "expected_output": (
                "A branch decision table plus a small GitFlow diagram showing correct branch origins "
                "and merge destinations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "branching",
                "gitflow",
                "feature-branches",
                "release-branches",
                "hotfix-branches",
            ],
        },

        {
            "id": "M02.L01.EX03",

            "title": "Complete a Feature-to-PR Workflow",

            "lesson_code": "M02.L01",

            "section_id": "pull-requests",

            "placement": "after_section",

            "description": (
                "Practice the complete collaboration path from cloning a repository to opening "
                "a reviewable pull request."
            ),

            "instructions": (
                "1. Create or use a practice GitHub repository initialized with a README.\n"
                "2. Clone it locally.\n"
                "3. Create feature/add-about-section.\n"
                "4. Add an ABOUT.md file with a short project description.\n"
                "5. Run git status and inspect the change.\n"
                "6. Stage and commit it with a descriptive message.\n"
                "7. Push the feature branch to origin and set upstream tracking.\n"
                "8. Open a pull request.\n"
                "9. In the PR description, write what changed, why, and how a reviewer can verify it.\n"
                "10. Explain why merging through the PR is safer than pushing the feature directly to main."
            ),

            "expected_output": (
                "A successful remote feature branch and pull request, plus a short written explanation "
                "of the review and safety benefits."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "git-clone",
                "feature-branch",
                "git-push",
                "pull-request",
                "code-review",
            ],
        },

        {
            "id": "M02.L01.EX04",

            "title": "Resolve a Merge Conflict Deliberately",

            "lesson_code": "M02.L01",

            "section_id": "merge-conflicts",

            "placement": "after_section",

            "description": (
                "Practice reading Git conflict markers and choosing the intended final content "
                "rather than mechanically accepting one side."
            ),

            "instructions": (
                "1. Start with a README line: 'Deployment status: pending'.\n"
                "2. On one branch, change it to 'Deployment status: ready for staging'.\n"
                "3. On another branch, change the same line to 'Deployment status: blocked by tests'.\n"
                "4. Merge one branch first, then attempt to merge the other so a conflict appears.\n"
                "5. Identify the HEAD block and incoming block.\n"
                "6. Resolve the file with a final sentence that accurately represents the state you choose.\n"
                "7. Remove all conflict markers.\n"
                "8. Stage the resolved file and complete the merge commit.\n"
                "9. Run git status and git log after resolution.\n"
                "10. Explain why Git could not safely choose the final text automatically."
            ),

            "expected_output": (
                "A resolved README, the conflict-resolution command sequence, and an explanation "
                "of why human intent was required."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "merge-conflicts",
                "git-merge",
                "conflict-markers",
                "resolution",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "Mastering Version Control with Git and GitHub — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",

                "section_id": "three-trees",

                "question": (
                    "Which Git area contains the files you are actively editing before you stage them?"
                ),

                "options": [
                    "The remote repository",
                    "The working directory",
                    "The staging area",
                    "The commit log",
                ],

                "correct": 1,

                "explanation": (
                    "The working directory contains the project files you edit directly. "
                    "You then select changes for the next commit by staging them."
                ),
            },

            {
                "id": "M02.L01.Q02",

                "section_id": "three-trees",

                "question": (
                    "What is the primary purpose of the staging area?"
                ),

                "options": [
                    "To host the repository on GitHub",
                    "To permanently store all previous releases",
                    "To choose which changes should be included in the next commit",
                    "To automatically merge remote branches",
                ],

                "correct": 2,

                "explanation": (
                    "The staging area lets you build a focused next snapshot instead of committing "
                    "every working-directory change together."
                ),
            },

            {
                "id": "M02.L01.Q03",

                "section_id": "local-workflow",

                "question": (
                    "After editing two files, you want only index.html in the next commit. Which command best supports that goal?"
                ),

                "options": [
                    "git add index.html",
                    "git add .",
                    "git push index.html",
                    "git commit index.html",
                ],

                "correct": 0,

                "explanation": (
                    "Staging only index.html lets you leave the other file as an unstaged working-directory change."
                ),
            },

            {
                "id": "M02.L01.Q04",

                "section_id": "remotes",

                "question": (
                    "Which statement correctly distinguishes git fetch from git pull?"
                ),

                "options": [
                    "fetch uploads commits while pull downloads them",
                    "fetch downloads remote information without immediately integrating it, while pull also integrates the changes",
                    "pull only works on GitHub but fetch works on any Git remote",
                    "They are two names for exactly the same operation",
                ],

                "correct": 1,

                "explanation": (
                    "The source presents pull conceptually as fetch plus integration, while fetch alone "
                    "lets you inspect remote updates before changing the current branch."
                ),
            },

            {
                "id": "M02.L01.Q05",

                "section_id": "branching-gitflow",

                "question": (
                    "In the GitFlow model described in the lesson, where does a normal feature branch begin?"
                ),

                "options": [
                    "main",
                    "develop",
                    "a hotfix branch",
                    "the remote origin reference only",
                ],

                "correct": 1,

                "explanation": (
                    "GitFlow feature branches start from develop and return to develop after the feature is completed."
                ),
            },

            {
                "id": "M02.L01.Q06",

                "section_id": "branching-gitflow",

                "question": (
                    "Why does a completed hotfix normally merge into both main and develop?"
                ),

                "options": [
                    "Because Git cannot merge into one branch at a time",
                    "Because the production fix must also be included in future development",
                    "Because develop is a backup of main",
                    "Because feature branches can only start from hotfix branches",
                ],

                "correct": 1,

                "explanation": (
                    "The production branch needs the urgent fix immediately, while the future development line "
                    "must also inherit that correction."
                ),
            },

            {
                "id": "M02.L01.Q07",

                "section_id": "github-workflow",

                "question": (
                    "After cloning a GitHub repository, what does origin commonly refer to?"
                ),

                "options": [
                    "The first local commit",
                    "The current working directory",
                    "The default nickname for the remote repository that was cloned",
                    "The protected main branch",
                ],

                "correct": 2,

                "explanation": (
                    "Git commonly creates origin as the remote name associated with the repository you cloned from."
                ),
            },

            {
                "id": "M02.L01.Q08",

                "section_id": "pull-requests",

                "question": (
                    "What is the main purpose of a pull request in the workflow taught here?"
                ),

                "options": [
                    "To replace Git commits with GitHub comments",
                    "To propose, review, discuss, check, and then merge branch changes",
                    "To download the repository for the first time",
                    "To delete old commit history",
                ],

                "correct": 1,

                "explanation": (
                    "A pull request creates a collaboration and review workflow around a proposed branch merge."
                ),
            },

            {
                "id": "M02.L01.Q09",

                "section_id": "pull-requests",

                "question": (
                    "Why can code review still be useful when automated tests pass?"
                ),

                "options": [
                    "Tests automatically approve architectural decisions",
                    "Human reviewers can evaluate clarity, design, maintainability, and context that tests may not cover",
                    "Passing tests mean the code has not been executed",
                    "Code review is only needed when tests fail",
                ],

                "correct": 1,

                "explanation": (
                    "Automated checks and human review solve different problems. Review adds design discussion, "
                    "knowledge sharing, consistency, and contextual judgment."
                ),
            },

            {
                "id": "M02.L01.Q10",

                "section_id": "merge-conflicts",

                "question": (
                    "What does a merge conflict mean?"
                ),

                "options": [
                    "Git detected competing changes it cannot combine safely without human intent",
                    "The Git repository has been permanently corrupted",
                    "A developer forgot to create a GitHub account",
                    "The remote repository has run out of storage",
                ],

                "correct": 0,

                "explanation": (
                    "A conflict simply means Git cannot infer the correct combined result for overlapping changes."
                ),
            },

            {
                "id": "M02.L01.Q11",

                "section_id": "merge-conflicts",

                "question": (
                    "After manually fixing a conflicted file, why do you run git add on it again?"
                ),

                "options": [
                    "To upload it directly to GitHub",
                    "To tell Git that the file's conflict has been resolved and stage the resolved content",
                    "To recreate the conflicting branch",
                    "To delete the merge commit",
                ],

                "correct": 1,

                "explanation": (
                    "Staging the edited file tells Git that you have resolved its conflict and want that final content "
                    "included in the merge result."
                ),
            },

            {
                "id": "M02.L01.Q12",

                "section_id": "professional-habits",

                "type": "open",

                "question": (
                    "You are about to commit a feature but git status shows one finished file, one experimental file, "
                    "and one unrelated documentation change. Explain how you would create a focused commit and why that "
                    "history would be better for future reviewers."
                ),
            },

            {
                "id": "M02.L01.Q13",

                "section_id": "pull-requests",

                "type": "open",

                "question": (
                    "Describe the complete collaboration flow from cloning a GitHub repository to getting a finished "
                    "feature into main, including the role of the feature branch, push, pull request, review, automated "
                    "checks, and merge."
                ),
            },
        ],

        "passing_score": 70,
    },
}
