"""M16.L01 — Building MLOps Command Line Tools and Microservices.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 11, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M16.L01"

MODULE_ORDER = 16

MODULE_TITLE = "Building MLOps Command Line Tools and Microservices"

MODULE_DESCRIPTION = (
    "Learn how Python packaging, virtual environments, requirements files, Click-based "
    "command-line tools, modular design, serverless microservices, authenticated HTTP APIs, "
    "managed cloud ML services, and cloud-backed CLI workflows can automate repetitive "
    "MLOps tasks and make production systems more reusable."
)

SOURCE_CHAPTER = 11

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Building MLOps Command Line Tools and Microservices",

    "slug": "practical-mlops-m16-l01-cli-tools-microservices",

    "description": (
        "A practical lesson on deciding when shell scripts stop being enough, packaging "
        "Python command-line tools, using virtual environments and dependency files, "
        "building a Click-based dataset linter, modularizing growing tools, designing "
        "microservices, deploying authenticated cloud functions, consuming managed ML APIs, "
        "building cloud-backed CLIs, and distributing ML command-line applications."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 5.5,

    "skill_tags": [
        "mlops",
        "automation",
        "command-line-tools",
        "python-packaging",
        "virtual-environments",
        "requirements-txt",
        "setup-py",
        "setuptools",
        "entry-points",
        "click",
        "pandas",
        "dataset-linting",
        "data-quality",
        "modularization",
        "microservices",
        "serverless",
        "cloud-functions",
        "http",
        "json",
        "authentication",
        "identity-token",
        "service-account",
        "oauth2",
        "managed-ml-services",
        "translation-api",
        "cloud-cli",
        "pypi",
        "container-registry",
        "ml-cli-workflows",
    ],

    "prerequisite_ids": ["M15.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Building MLOps Command Line Tools and Microservices",

        "content": (
            "# Building MLOps Command Line Tools and Microservices\n"
            "\n"
            "> **Lesson:** M16.L01  \n"
            "> **Module:** Building MLOps Command Line Tools and Microservices  \n"
            "> **Source alignment:** Chapter 11. Page numbers were not included in the supplied source. "
            "The Python packaging examples, framework versions, Google Cloud interfaces, and commands reflect "
            "the source's timeframe. This lesson preserves the chapter's engineering ideas and example flow.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain when a short shell script is sufficient and when Python becomes a better automation tool.\n"
            "- Explain why command-line tools are a useful bridge between software development and MLOps.\n"
            "- Decide when a Python script should become a packaged project.\n"
            "- Create and reason about isolated Python virtual environments.\n"
            "- Explain the role of `requirements.txt` and version constraints.\n"
            "- Explain the distinct role of `setup.py` in the source's packaging workflow.\n"
            "- Define a console-script entry point conceptually.\n"
            "- Use Click-style commands, arguments, validation, help output, and terminal messages conceptually.\n"
            "- Explain the three data-quality problems the source's CSV linter detects.\n"
            "- Design functions that detect zero-count columns, unnamed columns, and carriage returns.\n"
            "- Explain why dataset validation before ML platform ingestion is valuable.\n"
            "- Explain the difference between development installation and a standalone install in the source's setup workflow.\n"
            "- Modularize a growing CLI into a package with separate responsibilities.\n"
            "- Explain why reusable components improve maintainability.\n"
            "- Compare monolithic applications and microservices using the chapter's Jenga analogy.\n"
            "- Explain why serverless can be a practical microservice deployment mechanism.\n"
            "- Explain how cloud-managed ML APIs reduce the need to build every model from scratch.\n"
            "- Deploy an HTTP-triggered cloud function conceptually.\n"
            "- Explain why unauthenticated cloud functions create security and financial risk.\n"
            "- Explain the role of JSON in HTTP API communication.\n"
            "- Diagnose a disabled cloud API from the resulting permission error and logs.\n"
            "- Explain how a cloud function can call a managed translation API.\n"
            "- Construct the components of an authenticated HTTP request conceptually.\n"
            "- Explain the difference between a quick local authentication hack and a production authentication strategy.\n"
            "- Explain why service accounts/OAuth-style authentication are better suited to production automation.\n"
            "- Build a cloud-backed CLI conceptually using Click, HTTP requests, and authentication.\n"
            "- Explain several ways ML CLI tools can be distributed.\n"
            "- Explain why a CLI can sometimes be a more direct ML interface than a microservice.\n"
            "- Connect packaging, CLI design, HTTP services, cloud APIs, and automation into one MLOps workflow.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Use shell scripts for tiny jobs; use a general-purpose language when complexity grows\n"
            "\n"
            "The chapter starts from the author's systems-administration background, where shell scripting was the natural automation tool.\n"
            "\n"
            "Shell scripts are excellent when a task is genuinely small.\n"
            "\n"
            "The source's example copies a public SSH key to a remote machine using only a few lines.\n"
            "\n"
            "For a task like that, rewriting the solution in Python would add unnecessary code and dependencies.\n"
            "\n"
            "But shell scripts become less attractive as requirements grow around:\n"
            "\n"
            "- error handling,\n"
            "- reporting,\n"
            "- logging,\n"
            "- debugging,\n"
            "- testing,\n"
            "- reuse.\n"
            "\n"
            "The source gives a rough rule of thumb: once the solution grows beyond a small number of shell lines, consider a language such as Python.\n"
            "\n"
            "[[IMAGE_NEEDED: Shell script to Python growth path | "
            "A tiny one-purpose shell script on the left and a larger Python CLI with logging, tests, modules, and dependencies on the right | "
            "Learner should notice that tool choice changes as complexity and maintainability needs grow]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Command-line tools turn repetitive work into learnable automation\n"
            "\n"
            "The author describes learning Python by automating repetitive tasks that had direct practical value.\n"
            "\n"
            "That learning strategy maps naturally to MLOps.\n"
            "\n"
            "A useful process is:\n"
            "\n"
            "```text\n"
            "Notice repetitive manual work\n"
            "      ↓\n"
            "Create a small CLI\n"
            "      ↓\n"
            "Use it repeatedly\n"
            "      ↓\n"
            "Discover edge cases\n"
            "      ↓\n"
            "Improve the tool\n"
            "```\n"
            "\n"
            "Automation is valuable because it converts fragile human memory into a repeatable operation.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. CLI tools, containers, and microservices share a portability goal\n"
            "\n"
            "The chapter connects command-line tooling with containers and microservices.\n"
            "\n"
            "A well-installed command-line tool should be easy to invoke consistently.\n"
            "\n"
            "A container bundles dependencies so the application can run consistently wherever the appropriate runtime exists.\n"
            "\n"
            "A microservice isolates a small responsibility behind a network interface.\n"
            "\n"
            "All three aim to make useful functionality easier to reuse and operate.\n"
            "\n"
            "Serverless extends the idea further by hiding the operating system and runtime-management burden from the developer.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Package a Python tool when it grows beyond one dependency-free script\n"
            "\n"
            "A tiny Python script with no external dependencies can remain a single file.\n"
            "\n"
            "Packaging becomes more valuable when the tool:\n"
            "\n"
            "- depends on external libraries,\n"
            "- contains several files,\n"
            "- needs to be installed by others,\n"
            "- should expose an executable command,\n"
            "- may eventually be distributed through a package index.\n"
            "\n"
            "The chapter notes that Python packaging has historically been complicated, but it still recommends learning proper packaging techniques early.\n"
            "\n"
            "The operational payoff is that users of your tool can install dependencies consistently rather than reconstructing your development environment manually.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Virtual environments isolate dependency problems\n"
            "\n"
            "The source recommends virtual environments throughout Python development.\n"
            "\n"
            "The basic source-aligned commands are:\n"
            "\n"
            "```bash\n"
            "python -m venv venv\n"
            "source venv/bin/activate\n"
            "```\n"
            "\n"
            "After activation, the Python executable should come from the virtual environment rather than the system installation.\n"
            "\n"
            "Why is that useful?\n"
            "\n"
            "- project dependencies stay isolated,\n"
            "- system packages remain untouched,\n"
            "- a broken environment can be discarded and recreated,\n"
            "- project behavior becomes easier to reproduce.\n"
            "\n"
            "[[IMAGE_NEEDED: Python virtual environment isolation | "
            "System Python outside and two isolated project environments containing different dependency versions | "
            "Learner should notice that project dependencies no longer collide with the system or each other]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. `requirements.txt` declares installable dependencies\n"
            "\n"
            "The chapter shows dependencies listed one per line.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "click\n"
            "pytest==5.1.0\n"
            "```\n"
            "\n"
            "An unconstrained dependency lets the installer choose an available/latest version under the normal rules.\n"
            "\n"
            "A pinned dependency such as `pytest==5.1.0` asks for that exact version.\n"
            "\n"
            "Installation uses:\n"
            "\n"
            "```bash\n"
            "pip install -r requirements.txt\n"
            "```\n"
            "\n"
            "Projects may use several requirements files when development and production dependencies differ.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. In the source's packaging model, `setup.py` turns code into a distributable Python package\n"
            "\n"
            "The chapter distinguishes two jobs:\n"
            "\n"
            "- `requirements.txt` can declare/install project dependencies,\n"
            "- `setup.py` can package the project for distribution and can also declare dependencies.\n"
            "\n"
            "The source warns against abusing `setup.py` for unrelated tasks because it is executed during installation.\n"
            "\n"
            "Some projects read requirements from `requirements.txt` and reuse them in `setup.py`, but understanding the different roles helps avoid confusion.\n"
            "\n"
            "The key question is:\n"
            "\n"
            "> Is this merely a project/service that needs dependencies, or is it a Python package/tool intended to be installed and distributed?\n"
            "\n"
            "{{exercise:M16.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Start a CLI with a specific repetitive problem\n"
            "\n"
            "The chapter recommends identifying a concrete situation that needs automation rather than inventing a CLI without a purpose.\n"
            "\n"
            "The first major example comes from a real dataset-cleaning problem.\n"
            "\n"
            "The author had a wine-rating dataset with several anomalies that later caused confusing behavior in an ML platform.\n"
            "\n"
            "That pain becomes the specification for a dataset-linting CLI.\n"
            "\n"
            "This is good MLOps practice:\n"
            "\n"
            "> **Turn a failure you already experienced into an automated check that prevents the same failure later.**\n"
            "\n"
            "---\n"
            "\n"

            "## 9. The wine dataset revealed three concrete quality problems\n"
            "\n"
            "The chapter identifies three issues worth automating.\n"
            "\n"
            "### Problem 1: zero-count / unusable column\n"
            "\n"
            "The `grape` column contained no usable values.\n"
            "\n"
            "### Problem 2: unwanted `Unnamed` columns\n"
            "\n"
            "Repeated CSV saving introduced index-like unnamed columns.\n"
            "\n"
            "### Problem 3: carriage returns inside text fields\n"
            "\n"
            "Hidden carriage-return/newline characters caused another platform to interpret one logical field incorrectly.\n"
            "\n"
            "These examples show why a dataset can look visually reasonable but still violate downstream assumptions.\n"
            "\n"
            "[[IMAGE_NEEDED: Three CSV quality failures | "
            "A table illustrating an all-null column, an unwanted Unnamed index column, and hidden carriage-return characters inside a text field | "
            "Learner should notice how small formatting/data issues can break downstream ML workflows]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Package the CSV linter before adding real behavior\n"
            "\n"
            "The source creates a new `csv-linter` project and defines packaging metadata.\n"
            "\n"
            "A simplified source-aligned structure is:\n"
            "\n"
            "```python\n"
            "from setuptools import setup, find_packages\n"
            "\n"
            "setup(\n"
            "    name=\"csv-linter\",\n"
            "    packages=find_packages(),\n"
            "    entry_points=\"\"\"\n"
            "    [console_scripts]\n"
            "    csv-linter=csv_linter:main\n"
            "    \"\"\",\n"
            "    install_requires=[\"click==7.1.2\", \"pandas==1.2.0\"],\n"
            ")\n"
            "```\n"
            "\n"
            "The `entry_points` configuration maps an installed terminal command to a Python function.\n"
            "\n"
            "The executable name does not have to match the Python filename.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Click turns a Python function into a CLI command\n"
            "\n"
            "The first command is intentionally empty:\n"
            "\n"
            "```python\n"
            "import click\n"
            "\n"
            "@click.command()\n"
            "def main():\n"
            "    return\n"
            "```\n"
            "\n"
            "After installing the package in development mode, Click automatically provides a help interface.\n"
            "\n"
            "This demonstrates one benefit of a CLI framework: common command-line behavior does not need to be implemented manually.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Development installation keeps the executable connected to source changes\n"
            "\n"
            "The source uses:\n"
            "\n"
            "```bash\n"
            "python setup.py develop\n"
            "```\n"
            "\n"
            "The chapter contrasts this with a standalone install.\n"
            "\n"
            "In development mode, source-code edits become available to the installed command without repeatedly rebuilding a separate copy.\n"
            "\n"
            "That short feedback loop is convenient while actively developing the tool.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Let the CLI framework validate inputs early\n"
            "\n"
            "The source updates the command to accept a file path:\n"
            "\n"
            "```python\n"
            "@click.command()\n"
            "@click.argument(\"filename\", type=click.Path(exists=True))\n"
            "def main(filename):\n"
            "    ...\n"
            "```\n"
            "\n"
            "If the user passes a path that does not exist, Click produces a helpful error before Pandas is called.\n"
            "\n"
            "This is an important design principle:\n"
            "\n"
            "> **Validate inputs as close to the interface boundary as possible.**\n"
            "\n"
            "Clear early failures are easier to understand than deep runtime exceptions.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. A useful CLI wraps existing libraries rather than reinventing them\n"
            "\n"
            "The linter uses Pandas for CSV loading and analysis.\n"
            "\n"
            "A first useful version simply loads the file and prints `df.describe()`.\n"
            "\n"
            "That output is still too generic for the specific problems the author wants to prevent.\n"
            "\n"
            "So the next step is not to replace Pandas—it is to build focused checks on top of it.\n"
            "\n"
            "This illustrates a broader MLOps pattern: small tools often become valuable by combining mature libraries with domain-specific validation rules.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Check 1: detect columns with no usable values\n"
            "\n"
            "The source isolates the first check into a function:\n"
            "\n"
            "```python\n"
            "def zero_count_columns(df):\n"
            "    bad_columns = []\n"
            "    for key in df.keys():\n"
            "        if df[key].count() == 0:\n"
            "            bad_columns.append(key)\n"
            "    return bad_columns\n"
            "```\n"
            "\n"
            "The CLI then reports each returned column as a warning.\n"
            "\n"
            "The important architectural choice is the separation between:\n"
            "\n"
            "- **check logic** — identify bad columns,\n"
            "- **interface logic** — tell the user what was found.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Check 2: detect unwanted `Unnamed` columns\n"
            "\n"
            "The source adds another function that scans column names for the string `Unnamed`.\n"
            "\n"
            "Instead of returning every name, this function returns the number of matching columns.\n"
            "\n"
            "The CLI then emits a warning such as:\n"
            "\n"
            "```text\n"
            "Warning: found 1 columns that are Unnamed\n"
            "```\n"
            "\n"
            "The exact reporting format is less important than the automated guardrail: the tool catches a CSV artifact that was previously easy to forget.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Check 3: inspect text fields for carriage returns\n"
            "\n"
            "The third check is more expensive because it iterates through rows and fields.\n"
            "\n"
            "The source searches for `\\r\\n` inside string values, ignores incompatible field types by catching `TypeError`, and returns after finding the first occurrence.\n"
            "\n"
            "A simplified version is:\n"
            "\n"
            "```python\n"
            "def carriage_returns(df):\n"
            "    for index, row in df.iterrows():\n"
            "        for column, field in row.iteritems():\n"
            "            try:\n"
            "                if \"\\r\\n\" in field:\n"
            "                    return index, column, field\n"
            "            except TypeError:\n"
            "                continue\n"
            "```\n"
            "\n"
            "The CLI prints only the first portion of the problematic field so one huge text value does not flood the terminal.\n"
            "\n"
            "{{exercise:M16.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 18. The dataset linter demonstrates the core DevOps loop\n"
            "\n"
            "The final linter is small and not optimized for maximum performance.\n"
            "\n"
            "Yet it would have prevented hours of confusion for the author.\n"
            "\n"
            "That is the chapter's core automation lesson:\n"
            "\n"
            "```text\n"
            "Encounter problem manually\n"
            "      ↓\n"
            "Understand failure pattern\n"
            "      ↓\n"
            "Encode check in a tool\n"
            "      ↓\n"
            "Run check automatically next time\n"
            "```\n"
            "\n"
            "Automation is valuable when it captures operational knowledge before that knowledge is forgotten.\n"
            "\n"
            "[[IMAGE_NEEDED: Failure-to-automation feedback loop | "
            "A manual dataset failure becoming a reusable linter rule that protects later ML workflows | "
            "Learner should notice that automation stores lessons learned from past incidents]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Split a CLI when responsibilities become hard to reason about\n"
            "\n"
            "The chapter then moves from a single Python file to a package directory.\n"
            "\n"
            "The structure becomes conceptually:\n"
            "\n"
            "```text\n"
            "csv_linter/\n"
            "  __init__.py\n"
            "  main.py\n"
            "requirements.txt\n"
            "setup.py\n"
            "```\n"
            "\n"
            "Moving the module breaks the original entry point because `setup.py` still points to the old location.\n"
            "\n"
            "The entry point must therefore be updated to something like:\n"
            "\n"
            "```text\n"
            "csv-linter=csv_linter.main:main\n"
            "```\n"
            "\n"
            "This is a useful packaging lesson: installed commands depend on the package/module/function path remaining correct.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Move reusable checks out of the interface module\n"
            "\n"
            "The source next creates `checks.py` and moves the data-quality functions into it.\n"
            "\n"
            "The result is a clearer responsibility split:\n"
            "\n"
            "```text\n"
            "main.py\n"
            "  - CLI arguments\n"
            "  - user-facing output\n"
            "\n"
            "checks.py\n"
            "  - zero-count detection\n"
            "  - unnamed-column detection\n"
            "  - carriage-return detection\n"
            "```\n"
            "\n"
            "The author recommends grouping code by common responsibility, especially when reuse or readability benefits from separation.\n"
            "\n"
            "This is a direct bridge from CLI design into microservice thinking: isolate responsibilities so components can evolve and be reused independently.\n"
            "\n"
            "{{exercise:M16.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Microservices reduce coupling between responsibilities\n"
            "\n"
            "The chapter uses a Jenga analogy.\n"
            "\n"
            "A tightly coupled monolith is like a very tall unstable tower: touching one piece may disturb the whole structure.\n"
            "\n"
            "Well-separated components are easier to remove, reuse, and relocate.\n"
            "\n"
            "For MLOps, responsibility isolation is valuable because production ML contains many distinct concerns:\n"
            "\n"
            "- data validation,\n"
            "- preprocessing,\n"
            "- model prediction,\n"
            "- metadata operations,\n"
            "- API handling,\n"
            "- automation.\n"
            "\n"
            "Not every one of these must live inside one giant application.\n"
            "\n"
            "[[IMAGE_NEEDED: Monolith versus reusable microservice pieces | "
            "An unstable tall Jenga-like monolith beside smaller independent service blocks that can be rearranged and reused | "
            "Learner should notice how reducing coupling improves maintainability and reuse]]\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Serverless is a high-level way to create small microservices\n"
            "\n"
            "The source describes serverless as a way to write and deploy small applications without manually managing the operating system or its dependencies.\n"
            "\n"
            "Typical cloud providers let the developer:\n"
            "\n"
            "1. choose a runtime,\n"
            "2. write/upload the function,\n"
            "3. define a trigger,\n"
            "4. deploy.\n"
            "\n"
            "The provider handles much of the infrastructure beneath the function.\n"
            "\n"
            "This is especially useful for ML because a small serverless function can call cloud computer-vision, NLP, or recommendation services without building those models from scratch.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Use cloud ML capabilities when they are not your core competency\n"
            "\n"
            "The chapter strongly argues against recreating mature infrastructure or ML capabilities unnecessarily.\n"
            "\n"
            "Its email-server story illustrates the operational cost of maintaining a difficult commodity service in-house.\n"
            "\n"
            "The ML version of the principle is:\n"
            "\n"
            "> **If state-of-the-art computer vision is not your company's core competency, consider using an existing cloud capability rather than rebuilding it from scratch.**\n"
            "\n"
            "The source frames this as 'standing on the shoulders of giants.'\n"
            "\n"
            "The engineering benefit can be speed, robustness, and reproducibility.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Cloud microservices exist on an abstraction spectrum\n"
            "\n"
            "The source places technologies along a rough spectrum:\n"
            "\n"
            "```text\n"
            "More infrastructure control/complexity\n"
            "Kubernetes\n"
            "    ↓\n"
            "Cloud functions / serverless\n"
            "    ↓\n"
            "High-level managed app services\n"
            "e.g. App Runner / Cloud Run\n"
            "More platform abstraction/simplicity\n"
            "```\n"
            "\n"
            "The correct choice depends on the organization's real needs.\n"
            "\n"
            "The chapter repeatedly recommends resisting the urge to reinvent lower-level infrastructure when a high-level service already solves the problem well enough.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Build an authenticated HTTP-triggered cloud function first\n"
            "\n"
            "The chapter's serverless example uses Google Cloud Functions.\n"
            "\n"
            "The function is configured with an HTTP trigger and authentication enabled.\n"
            "\n"
            "The source specifically warns against deploying public unauthenticated functions because abuse can create direct financial cost for the account owner.\n"
            "\n"
            "The function receives JSON and uses a chosen Python entry point.\n"
            "\n"
            "A minimal conceptual handler is:\n"
            "\n"
            "```python\n"
            "def main(request):\n"
            "    request_json = request.get_json()\n"
            "    if request_json and \"message\" in request_json:\n"
            "        return request_json[\"message\"]\n"
            "    return \"No message was provided\"\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Authenticated Cloud Function request path | "
            "Client sending an authenticated HTTP POST with JSON into a serverless function, with billing/security boundary highlighted | "
            "Learner should notice that HTTP convenience does not remove the need for authentication]]\n"
            "\n"
            "{{exercise:M16.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 26. JSON is the common payload language of the chapter's HTTP examples\n"
            "\n"
            "The source describes JSON as a common language for web development because many languages can create and consume it naturally.\n"
            "\n"
            "A serverless ML request often has a shape such as:\n"
            "\n"
            "```json\n"
            "{\"message\": \"translate this text\"}\n"
            "```\n"
            "\n"
            "The HTTP layer can restrict:\n"
            "\n"
            "- allowed methods,\n"
            "- authentication,\n"
            "- content type,\n"
            "- body structure.\n"
            "\n"
            "This gives a small cloud function a clear software contract.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Managed cloud APIs often must be enabled explicitly\n"
            "\n"
            "The chapter modifies the function to use Google's translation service.\n"
            "\n"
            "Before the API is enabled, the function fails with a permission-style error and returns an HTTP 500 response to the caller.\n"
            "\n"
            "The logs explain that the Translation API has not been used or is disabled for the project.\n"
            "\n"
            "This is a useful debugging lesson:\n"
            "\n"
            "> **Cloud integration failures may come from project/service configuration, not from your function logic.**\n"
            "\n"
            "The chapter also notes that a user without sufficient administrative permissions may be unable to enable the API themselves.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Compose your function with a managed translation API\n"
            "\n"
            "After enabling the API and adding the required Python library, the source introduces a `translator()` helper.\n"
            "\n"
            "Its inputs include:\n"
            "\n"
            "- text,\n"
            "- project ID,\n"
            "- target language.\n"
            "\n"
            "The main HTTP function extracts the `message` value from JSON and passes it to the translator.\n"
            "\n"
            "The architecture is:\n"
            "\n"
            "```text\n"
            "HTTP JSON request\n"
            "      ↓\n"
            "main(request)\n"
            "      ↓\n"
            "translator(...)\n"
            "      ↓\n"
            "managed translation service\n"
            "      ↓\n"
            "translated response\n"
            "```\n"
            "\n"
            "The source's lesson is larger than translation: small application logic can compose powerful managed ML services quickly.\n"
            "\n"
            "---\n"
            "\n"

            "## 29. An authenticated HTTP request has several explicit pieces\n"
            "\n"
            "The source uses `curl` to make the required pieces visible.\n"
            "\n"
            "A successful call includes:\n"
            "\n"
            "1. HTTP method — POST,\n"
            "2. JSON body,\n"
            "3. `Content-Type: application/json`,\n"
            "4. authorization header containing an identity token,\n"
            "5. cloud-function URL.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```bash\n"
            "curl -X POST \\\n"
            "  --data '{\"message\": \"from the terminal\"}' \\\n"
            "  -H 'Content-Type: application/json' \\\n"
            "  -H 'Authorization: bearer <identity-token>' \\\n"
            "  <function-url>\n"
            "```\n"
            "\n"
            "This explicit form is useful for understanding what higher-level SDK commands are doing on your behalf.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Higher-level SDK commands can simplify authenticated invocation\n"
            "\n"
            "The source next uses `gcloud functions call` to invoke the same function.\n"
            "\n"
            "That command hides some of the lower-level HTTP/token construction while still performing an authenticated request.\n"
            "\n"
            "This flexibility matters because different environments may prefer:\n"
            "\n"
            "- raw HTTP,\n"
            "- command-line SDK,\n"
            "- application code.\n"
            "\n"
            "Understanding the underlying request makes it easier to move between those interfaces.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. A quick authentication demo is not necessarily a production authentication design\n"
            "\n"
            "The chapter demonstrates Python code that calls the `gcloud auth print-identity-token` command through `subprocess`, then sends the token with `requests`.\n"
            "\n"
            "The source explicitly warns that this is a quick demonstration, not a robust production approach.\n"
            "\n"
            "For production, it recommends creating a service account and using appropriate Google API authentication/OAuth tooling.\n"
            "\n"
            "This distinction is important:\n"
            "\n"
            "> **A prototype can teach the protocol, but production automation needs a stable machine identity and proper credential lifecycle.**\n"
            "\n"
            "{{exercise:M16.L01.EX05}}\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Package the remote cloud workflow into a user-friendly CLI\n"
            "\n"
            "The source then combines the earlier ideas into a `cloud-translate` command.\n"
            "\n"
            "`setup.py` creates an executable mapped to a Click `main()` function.\n"
            "\n"
            "The CLI accepts text as an argument, obtains authentication, sends an HTTP request, and prints the translated response.\n"
            "\n"
            "A source-aligned usage example is:\n"
            "\n"
            "```bash\n"
            "cloud-translate \"today is a wonderful day\"\n"
            "```\n"
            "\n"
            "The user does not need to know the internal HTTP details every time.\n"
            "\n"
            "This is one of the chapter's strongest MLOps patterns:\n"
            "\n"
            "```text\n"
            "Complex cloud interaction\n"
            "      ↓\n"
            "package + automate once\n"
            "      ↓\n"
            "simple repeatable CLI command\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Cloud-backed CLI architecture | "
            "A terminal command calling a packaged Click CLI, which authenticates and sends HTTP JSON to a cloud function that invokes a managed ML API | "
            "Learner should notice how packaging hides repetitive cloud plumbing behind one stable command]]\n"
            "\n"
            "---\n"
            "\n"

            "## 33. ML command-line workflows can support many modeling styles\n"
            "\n"
            "The chapter emphasizes that a CLI can wrap many kinds of ML behavior.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- unsupervised training on demand,\n"
            "- using a trained nightly model stored in object storage,\n"
            "- calling AutoML systems,\n"
            "- calling managed AI APIs,\n"
            "- using third-party pretrained models.\n"
            "\n"
            "Problem domains mentioned include:\n"
            "\n"
            "- text,\n"
            "- computer vision,\n"
            "- behavioral analytics,\n"
            "- customer analysis.\n"
            "\n"
            "A CLI is therefore not tied to one model-serving pattern.\n"
            "\n"
            "---\n"
            "\n"

            "## 34. CLI applications have many distribution targets\n"
            "\n"
            "The source lists several ways to distribute ML command-line tools:\n"
            "\n"
            "- shared filesystems mounted across a cluster,\n"
            "- Python Package Index (PyPI),\n"
            "- public/private container registries,\n"
            "- Linux packages such as Debian or RPM packages.\n"
            "\n"
            "A CLI is a complete application, so it can sometimes be deployed in more ways than a network microservice.\n"
            "\n"
            "The right choice depends on who will consume the tool and what environment they already use.\n"
            "\n"
            "---\n"
            "\n"

            "## 35. The chapter's CLI examples show different ML applications\n"
            "\n"
            "The source points to several example project types:\n"
            "\n"
            "- developer/GitHub organization analysis,\n"
            "- the Python MLOps Cookbook,\n"
            "- clustering cloud spot-instance types by attributes such as memory, CPU, and price.\n"
            "\n"
            "The important lesson is that command-line tools are not limited to data cleanup.\n"
            "\n"
            "They can become lightweight interfaces to analytics, ML predictions, clustering, retraining, or cloud services.\n"
            "\n"
            "---\n"
            "\n"

            "## 36. Put the chapter together as one reusable MLOps automation system\n"
            "\n"
            "The chapter's pieces form a coherent progression:\n"
            "\n"
            "```text\n"
            "Manual repetitive task\n"
            "      ↓\n"
            "small Python script\n"
            "      ↓\n"
            "virtual environment + dependencies\n"
            "      ↓\n"
            "packaged Click CLI\n"
            "      ↓\n"
            "domain checks / model logic\n"
            "      ↓\n"
            "modular reusable components\n"
            "      ↓\n"
            "HTTP/serverless microservice\n"
            "      ↓\n"
            "managed ML API\n"
            "      ↓\n"
            "authenticated cloud-backed CLI\n"
            "      ↓\n"
            "distribution and reuse\n"
            "```\n"
            "\n"
            "The chapter's conclusion calls the ability to connect applications and services an MLOps 'superpower.'\n"
            "\n"
            "The point is not merely to know Click or Cloud Functions.\n"
            "\n"
            "The point is to turn tricky operational work into small, composable, reusable automation.\n"
            "\n"
            "{{exercise:M16.L01.EX06}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Every shell script should be rewritten in Python\n"
            "\n"
            "The source explicitly keeps shell scripting for small, portable tasks where a few lines are sufficient.\n"
            "\n"
            "### Misconception 2: A Python script only needs packaging if it will be open source\n"
            "\n"
            "Packaging is useful whenever dependencies, multiple files, installation, or reuse become important.\n"
            "\n"
            "### Misconception 3: Virtual environments are optional ceremony\n"
            "\n"
            "The chapter recommends them as a robust way to isolate dependencies and recover from dependency problems.\n"
            "\n"
            "### Misconception 4: `requirements.txt` and `setup.py` have identical purposes\n"
            "\n"
            "Both can participate in dependency installation, but the source uses `setup.py` for packaging/distribution and console entry points.\n"
            "\n"
            "### Misconception 5: A CLI framework only saves a few lines of parsing code\n"
            "\n"
            "Click also provides validation, help generation, arguments, output helpers, and a cleaner interface boundary.\n"
            "\n"
            "### Misconception 6: Dataset quality problems are always obvious in a dataframe preview\n"
            "\n"
            "The chapter's carriage-return and extra-column problems were subtle enough to break downstream ML tooling.\n"
            "\n"
            "### Misconception 7: One giant CLI file is easier because there are fewer files\n"
            "\n"
            "As responsibility grows, modular separation improves readability, reuse, and maintenance.\n"
            "\n"
            "### Misconception 8: Microservices are just containers\n"
            "\n"
            "The source discusses responsibility isolation, reusability, serverless functions, and HTTP services in addition to containers.\n"
            "\n"
            "### Misconception 9: Public unauthenticated cloud functions are harmless for small prototypes\n"
            "\n"
            "The source warns that unauthorized usage can create security and financial consequences.\n"
            "\n"
            "### Misconception 10: Calling `gcloud` from Python is the recommended final production authentication architecture\n"
            "\n"
            "The source calls it a quick demonstration and recommends service-account/OAuth-based authentication for production.\n"
            "\n"
            "### Misconception 11: Every ML capability should be built from scratch\n"
            "\n"
            "The chapter strongly encourages leveraging mature cloud ML services when the capability is not the organization's core competency.\n"
            "\n"
            "### Misconception 12: A CLI is always less deployable than a microservice\n"
            "\n"
            "The source lists package repositories, filesystems, containers, and OS packages as CLI distribution targets.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Shell script | Command-language automation useful for small, direct tasks. |\n"
            "| Python package | Installable/distributable Python project containing code and metadata. |\n"
            "| Virtual environment | Isolated Python environment used to keep project dependencies separate. |\n"
            "| requirements.txt | Plain-text dependency list consumed by installers such as pip. |\n"
            "| setup.py | Packaging configuration used by the source to define metadata, dependencies, and console scripts. |\n"
            "| Entry point | Mapping from an installed command name to a Python function/module path. |\n"
            "| Click | Python CLI framework used throughout the chapter's command-line examples. |\n"
            "| Dataset linter | Tool that performs automated checks to warn about problematic dataset properties. |\n"
            "| Zero-count column | Column whose usable value count is zero in the source's Pandas check. |\n"
            "| Unnamed column | Unexpected column name pattern created in the CSV workflow described by the source. |\n"
            "| Carriage return | Hidden control/newline character that caused downstream parsing problems in the example dataset. |\n"
            "| Modularization | Separating code by responsibility into multiple modules/files. |\n"
            "| Microservice | Small independently focused application/service built around a limited responsibility. |\n"
            "| Serverless | Cloud execution model that abstracts much of the server/OS/runtime management. |\n"
            "| HTTP trigger | Network request that invokes a serverless function. |\n"
            "| JSON | Common structured data format used for request/response payloads in the chapter. |\n"
            "| Identity token | Token included in authenticated function requests in the source example. |\n"
            "| Service account | Machine identity recommended by the source for more robust production authentication. |\n"
            "| Managed ML API | Cloud-provided ML capability such as translation that can be called instead of building a model from scratch. |\n"
            "| Cloud-backed CLI | Local command-line application that invokes a remote cloud service behind a simplified command. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "1. When does the source recommend keeping a solution as a shell script?\n"
            "2. Which programming concerns become easier in Python than in a growing shell script?\n"
            "3. Why does the author recommend learning through personally useful automation tasks?\n"
            "4. How are CLI tools, containers, and microservices connected conceptually?\n"
            "5. When is a single unpackaged Python script still acceptable?\n"
            "6. When should packaging be considered?\n"
            "7. Why are virtual environments recommended?\n"
            "8. How do you create and activate the virtual environment shown in the source?\n"
            "9. What does `requirements.txt` contain?\n"
            "10. What is the difference between an unpinned and an exactly pinned dependency in the source example?\n"
            "11. What additional distribution role does `setup.py` play?\n"
            "12. Why does the source recommend keeping `setup.py` focused on packaging tasks?\n"
            "13. Why does the chapter begin CLI design from a real repetitive problem?\n"
            "14. What three problems motivated the CSV linter?\n"
            "15. What does the console-script entry point do?\n"
            "16. What does Click provide automatically even before the command does real work?\n"
            "17. What is the development-installation behavior described by `setup.py develop`?\n"
            "18. Why is `click.Path(exists=True)` useful?\n"
            "19. Why was `df.describe()` not enough for the author's needs?\n"
            "20. How does the zero-count-column function work?\n"
            "21. What does the unnamed-column check report?\n"
            "22. Why is the carriage-return scan potentially expensive?\n"
            "23. Why does the source stop after the first carriage-return match?\n"
            "24. Why does the warning truncate the problematic field?\n"
            "25. What DevOps principle does the CSV linter demonstrate?\n"
            "26. Why did moving the CLI into a package initially break the installed command?\n"
            "27. How is the entry-point path updated after modularization?\n"
            "28. Why move check functions into `checks.py`?\n"
            "29. What does the Jenga analogy communicate about monoliths and reusable services?\n"
            "30. Why is serverless useful for microservices?\n"
            "31. Why does the chapter recommend using existing cloud ML capabilities where appropriate?\n"
            "32. How does Kubernetes differ from a high-level managed service such as Cloud Run/App Runner in the source's abstraction spectrum?\n"
            "33. Why does the source insist on authentication for cloud functions?\n"
            "34. Why is JSON useful for HTTP service integration?\n"
            "35. What happened when the translation API had not been enabled?\n"
            "36. What inputs does the translation helper use?\n"
            "37. Which pieces are visible in the source's authenticated curl request?\n"
            "38. Why is understanding the raw HTTP request useful even when an SDK exists?\n"
            "39. Why is the subprocess-based token example not the final production recommendation?\n"
            "40. What production authentication approach does the source recommend considering instead?\n"
            "41. What does the `cloud-translate` CLI hide from the end user?\n"
            "42. Which ML patterns can a CLI wrap according to the chapter?\n"
            "43. What distribution targets are named for ML command-line tools?\n"
            "44. Why can a CLI be an effective full application rather than merely a helper script?\n"
            "45. What is the chapter's main MLOps lesson about connecting tools, services, HTTP, and cloud APIs?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A strong MLOps engineer turns repeated operational pain into reusable automation. Start small, package the tool when complexity grows, "
            "separate responsibilities, expose functionality through clean CLI or HTTP boundaries, authenticate cloud services correctly, and reuse mature "
            "managed capabilities instead of rebuilding everything from scratch.**\n"
        ),

        "estimated_minutes": 330,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "shell-vs-python", "title": "Use shell scripts for tiny jobs; use a general-purpose language when complexity grows", "order": 1},
            {"id": "learn-by-automation", "title": "Command-line tools turn repetitive work into learnable automation", "order": 2},
            {"id": "cli-containers-microservices", "title": "CLI tools, containers, and microservices share a portability goal", "order": 3},
            {"id": "when-package", "title": "Package a Python tool when it grows beyond one dependency-free script", "order": 4},
            {"id": "virtualenv", "title": "Virtual environments isolate dependency problems", "order": 5},
            {"id": "requirements", "title": "requirements.txt declares installable dependencies", "order": 6},
            {"id": "setup-py", "title": "In the source's packaging model, setup.py turns code into a distributable Python package", "order": 7},
            {"id": "cli-problem-first", "title": "Start a CLI with a specific repetitive problem", "order": 8},
            {"id": "dataset-problems", "title": "The wine dataset revealed three concrete quality problems", "order": 9},
            {"id": "package-csv-linter", "title": "Package the CSV linter before adding real behavior", "order": 10},
            {"id": "click-first-command", "title": "Click turns a Python function into a CLI command", "order": 11},
            {"id": "develop-install", "title": "Development installation keeps the executable connected to source changes", "order": 12},
            {"id": "click-path-validation", "title": "Let the CLI framework validate inputs early", "order": 13},
            {"id": "pandas-description", "title": "A useful CLI wraps existing libraries rather than reinventing them", "order": 14},
            {"id": "zero-count", "title": "Check 1: detect columns with no usable values", "order": 15},
            {"id": "unnamed-columns", "title": "Check 2: detect unwanted Unnamed columns", "order": 16},
            {"id": "carriage-returns", "title": "Check 3: inspect text fields for carriage returns", "order": 17},
            {"id": "automate-pain", "title": "The dataset linter demonstrates the core DevOps loop", "order": 18},
            {"id": "modularize", "title": "Split a CLI when responsibilities become hard to reason about", "order": 19},
            {"id": "separate-checks", "title": "Move reusable checks out of the interface module", "order": 20},
            {"id": "microservices-jenga", "title": "Microservices reduce coupling between responsibilities", "order": 21},
            {"id": "serverless-microservices", "title": "Serverless is a high-level way to create small microservices", "order": 22},
            {"id": "dont-reinvent", "title": "Use cloud ML capabilities when they are not your core competency", "order": 23},
            {"id": "microservice-spectrum", "title": "Cloud microservices exist on an abstraction spectrum", "order": 24},
            {"id": "create-cloud-function", "title": "Build an authenticated HTTP-triggered cloud function first", "order": 25},
            {"id": "json-http", "title": "JSON is the common payload language of the chapter's HTTP examples", "order": 26},
            {"id": "enable-api", "title": "Managed cloud APIs often must be enabled explicitly", "order": 27},
            {"id": "translation-api", "title": "Compose your function with a managed translation API", "order": 28},
            {"id": "authenticated-http", "title": "An authenticated HTTP request has several explicit pieces", "order": 29},
            {"id": "gcloud-auth", "title": "Higher-level SDK commands can simplify authenticated invocation", "order": 30},
            {"id": "python-auth-demo", "title": "A quick authentication demo is not necessarily a production authentication design", "order": 31},
            {"id": "cloud-cli", "title": "Package the remote cloud workflow into a user-friendly CLI", "order": 32},
            {"id": "ml-cli-workflows", "title": "ML command-line workflows can support many modeling styles", "order": 33},
            {"id": "cli-distribution", "title": "CLI applications have many distribution targets", "order": 34},
            {"id": "examples", "title": "The chapter's CLI examples show different ML applications", "order": 35},
            {"id": "chapter-system", "title": "Put the chapter together as one reusable MLOps automation system", "order": 36},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M16.L01.EX01",
            "title": "Choose script, project, or package",
            "lesson_code": "M16.L01",
            "section_id": "setup-py",
            "placement": "after_section",
            "description": (
                "Decide when a task should remain a shell script, become a Python script, or become a packaged CLI."
            ),
            "instructions": (
                "Classify each scenario and justify your decision:\n\n"
                "1. A five-line command that copies one config file to a remote server.\n"
                "2. A Python script with no dependencies that renames files in one directory.\n"
                "3. A CLI that uses Click and Pandas, has several modules, and must be installed by teammates.\n"
                "4. A tool intended for distribution through a Python package repository.\n\n"
                "For each case explain the role—if any—of a virtual environment, requirements file, and packaging metadata."
            ),
            "expected_output": (
                "Four justified classifications showing when packaging overhead becomes worthwhile."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "python-packaging",
                "virtual-environments",
                "automation-design",
                "dependency-management",
            ],
        },

        {
            "id": "M16.L01.EX02",
            "title": "Design the CSV linter checks",
            "lesson_code": "M16.L01",
            "section_id": "carriage-returns",
            "placement": "after_section",
            "description": (
                "Reconstruct the source's data-quality guardrails as an automated CLI design."
            ),
            "instructions": (
                "Design three functions for a CSV linter:\n\n"
                "1. return names of zero-count columns,\n"
                "2. count columns containing `Unnamed`,\n"
                "3. detect the first field containing a carriage return.\n\n"
                "Then define the user-facing warning for each check and explain why the carriage-return output should be truncated."
            ),
            "expected_output": (
                "Three check functions/pseudocode blocks plus concise warning behavior."
            ),
            "type": "code",
            "language": "python",
            "starter_code": (
                "def zero_count_columns(rows: list[dict[str, str]]) -> list[str]:\n"
                "    # TODO: return columns whose values are empty in every row.\n"
                "    pass\n\n"
                "def count_unnamed_columns(fieldnames: list[str]) -> int:\n"
                "    # TODO: count field names containing 'Unnamed'.\n"
                "    pass\n\n"
                "def first_carriage_return(rows: list[dict[str, str]]):\n"
                "    # TODO: return {'column': name, 'preview': truncated_value}\n"
                "    # for the first string containing a carriage return, else None.\n"
                "    pass\n"
            ),
            "solution_code": (
                "def zero_count_columns(rows: list[dict[str, str]]) -> list[str]:\n"
                "    if not rows:\n"
                "        return []\n"
                "    return [\n"
                "        column\n"
                "        for column in rows[0]\n"
                "        if all(row.get(column, '') == '' for row in rows)\n"
                "    ]\n\n"
                "def count_unnamed_columns(fieldnames: list[str]) -> int:\n"
                "    return sum('Unnamed' in name for name in fieldnames)\n\n"
                "def first_carriage_return(rows: list[dict[str, str]]):\n"
                "    for row in rows:\n"
                "        for column, value in row.items():\n"
                "            if isinstance(value, str) and '\\r' in value:\n"
                "                return {'column': column, 'preview': value[:40]}\n"
                "    return None\n"
            ),
            "hint": "Use all() for empty columns, sum() for Unnamed fields, and nested loops for the first carriage return.",
            "success_message": "Correct! All three CSV data-quality checks return the expected result.",
            "tests": [
                {
                    "id": "zero_count_columns",
                    "type": "return_value_equals",
                    "function": "zero_count_columns",
                    "args": [[
                        {"name": "Ada", "empty": ""},
                        {"name": "Lin", "empty": ""},
                    ]],
                    "expected": ["empty"],
                    "feedback": {
                        "en": "Return only columns that are empty in every row.",
                        "ar": "أعد فقط الأعمدة الفارغة في جميع الصفوف.",
                    },
                },
                {
                    "id": "unnamed_columns",
                    "type": "return_value_equals",
                    "function": "count_unnamed_columns",
                    "args": [["name", "Unnamed: 0", "age"]],
                    "expected": 1,
                    "feedback": {
                        "en": "Count field names containing `Unnamed`.",
                        "ar": "احسب أسماء الحقول التي تحتوي على `Unnamed`.",
                    },
                },
                {
                    "id": "carriage_return",
                    "type": "return_value_equals",
                    "function": "first_carriage_return",
                    "args": [[{"notes": "ok", "bio": "line 1\rline 2"}]],
                    "expected": {"column": "bio", "preview": "line 1\rline 2"},
                    "feedback": {
                        "en": "Return the first field containing `\\r` with a short preview.",
                        "ar": "أعد أول حقل يحتوي على `\\r` مع معاينة قصيرة.",
                    },
                },
                {
                    "id": "no_carriage_return",
                    "type": "return_value_equals",
                    "function": "first_carriage_return",
                    "args": [[{"notes": "clean"}]],
                    "expected": None,
                    "feedback": {
                        "en": "Return None when no carriage return is present.",
                        "ar": "أعد None عند عدم وجود carriage return.",
                    },
                },
            ],
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "dataset-linting",
                "pandas",
                "data-quality",
                "cli-design",
            ],
        },

        {
            "id": "M16.L01.EX03",
            "title": "Modularize a growing CLI",
            "lesson_code": "M16.L01",
            "section_id": "separate-checks",
            "placement": "after_section",
            "description": (
                "Practice separating interface code from reusable domain checks."
            ),
            "instructions": (
                ('1. A single `csv_linter.py` file now contains 300 lines of Click code, data checks, formatting, and helper functions.\n'
                 '2. Propose a package structure with at least:\n'
                 '   - `__init__.py`,\n'
                 '   - `main.py`,\n'
                 '   - `checks.py`,\n'
                 '   - `setup.py`,\n'
                 '   - `requirements.txt`.\n'
                 '3. State which responsibilities belong in each file and show how the console entry point must change after moving `main()`.')
            ),
            "expected_output": (
                "A modular package tree with responsibility boundaries and an updated entry-point mapping."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "modularization",
                "setuptools",
                "entry-points",
                "maintainability",
            ],
        },

        {
            "id": "M16.L01.EX04",
            "title": "Design a secure serverless ML function",
            "lesson_code": "M16.L01",
            "section_id": "create-cloud-function",
            "placement": "after_section",
            "description": (
                "Combine HTTP, JSON, authentication, and a managed cloud ML capability."
            ),
            "instructions": (
                "Design an HTTP-triggered serverless function that receives JSON text and calls a managed language service.\n\n"
                "Specify:\n"
                "1. expected JSON schema,\n"
                "2. HTTP method,\n"
                "3. authentication requirement,\n"
                "4. runtime/entry point,\n"
                "5. cloud API that must be enabled,\n"
                "6. dependency added to requirements,\n"
                "7. expected response,\n"
                "8. one consequence of leaving the endpoint unauthenticated."
            ),
            "expected_output": (
                "A secure, source-aligned serverless microservice contract."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "serverless",
                "http",
                "json",
                "authentication",
                "managed-ml-services",
            ],
        },

        {
            "id": "M16.L01.EX05",
            "title": "Move from demo authentication to production authentication",
            "lesson_code": "M16.L01",
            "section_id": "python-auth-demo",
            "placement": "after_section",
            "description": (
                "Differentiate a quick local token demonstration from a robust production approach."
            ),
            "instructions": (
                "A Python script currently runs `gcloud auth print-identity-token` through `subprocess` for every request.\n\n"
                "Explain:\n"
                "1. why this is useful for demonstrating the HTTP protocol,\n"
                "2. why it is not a robust production design,\n"
                "3. what machine identity the source recommends creating,\n"
                "4. what type of API authentication tooling the source recommends considering,\n"
                "5. what should remain unchanged in the HTTP request after authentication is improved."
            ),
            "expected_output": (
                "A migration plan from local CLI-token dependency to proper production machine authentication."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "authentication",
                "service-account",
                "oauth2",
                "http",
            ],
        },

        {
            "id": "M16.L01.EX06",
            "title": "Build an ML automation interface",
            "lesson_code": "M16.L01",
            "section_id": "chapter-system",
            "placement": "after_section",
            "description": (
                "Integrate packaging, CLI, cloud services, and distribution into one reusable MLOps workflow."
            ),
            "instructions": (
                "Design a command-line tool that performs one ML-related task useful to a team.\n\n"
                "Your design must include:\n"
                "1. the repetitive problem being automated,\n"
                "2. package structure,\n"
                "3. dependencies,\n"
                "4. Click arguments/options,\n"
                "5. validation rules,\n"
                "6. whether ML runs locally or through a cloud API,\n"
                "7. authentication if remote,\n"
                "8. logging/error behavior,\n"
                "9. one distribution target such as PyPI or a container registry,\n"
                "10. one future modularization or microservice boundary.\n\n"
                "Explain why the design is simpler for the user than the manual process it replaces."
            ),
            "expected_output": (
                "A complete small-scale MLOps CLI architecture grounded in the chapter's patterns."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "command-line-tools",
                "mlops-automation",
                "cloud-integration",
                "packaging",
                "microservices",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M16.L01.QZ01",

        "title": "Building MLOps Command Line Tools and Microservices — Knowledge Check",

        "lesson_code": "M16.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M16.L01.Q01",
                "section_id": "shell-vs-python",
                "question": "When does the source prefer a shell script?",
                "options": [
                    "For a small, portable task that takes only a few lines.",
                    "For every application regardless of complexity.",
                    "Only when machine learning is involved.",
                    "Never.",
                ],
                "correct": 0,
                "explanation": (
                    "The source keeps shell scripting for very small tasks and recommends looking beyond it as complexity grows."
                ),
            },

            {
                "id": "M16.L01.Q02",
                "section_id": "shell-vs-python",
                "question": "Which need is one reason to move from shell scripting toward Python?",
                "options": [
                    "Better support for logging, testing, debugging, and error handling",
                    "Fewer programming-language features",
                    "No dependencies ever",
                    "No need for functions",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter contrasts shell limitations with richer application-development facilities."
                ),
            },

            {
                "id": "M16.L01.Q03",
                "section_id": "when-package",
                "question": "When does the chapter recommend considering Python packaging?",
                "options": [
                    "When a tool gains dependencies or multiple files and needs installation/distribution.",
                    "Only after one million lines of code.",
                    "Only for notebooks.",
                    "Only for shell scripts.",
                ],
                "correct": 0,
                "explanation": (
                    "Dependencies, complexity, and distribution are the source's main triggers for packaging."
                ),
            },

            {
                "id": "M16.L01.Q04",
                "section_id": "virtualenv",
                "question": "What is the main purpose of a Python virtual environment?",
                "options": [
                    "Isolate project dependencies from the system and other projects.",
                    "Train models faster automatically.",
                    "Replace `pip`.",
                    "Publish packages.",
                ],
                "correct": 0,
                "explanation": (
                    "The source recommends virtual environments as a robust dependency-isolation mechanism."
                ),
            },

            {
                "id": "M16.L01.Q05",
                "section_id": "requirements",
                "question": "What does `pytest==5.1.0` express in a requirements file?",
                "options": [
                    "Install that exact pytest version.",
                    "Install any future pytest version only.",
                    "Do not install pytest.",
                    "Run pytest as a shell command.",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts exact version pinning with an unconstrained dependency."
                ),
            },

            {
                "id": "M16.L01.Q06",
                "section_id": "setup-py",
                "question": "What capability does `setup.py` add in the source's workflow?",
                "options": [
                    "Packaging/distribution and console-script entry-point definition.",
                    "Only CSV reading.",
                    "Only virtual-environment creation.",
                    "Only cloud authentication.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter uses setup.py to make the CLI installable and distributable."
                ),
            },

            {
                "id": "M16.L01.Q07",
                "section_id": "dataset-problems",
                "question": "Which problem was NOT one of the CSV linter's three main checks?",
                "options": [
                    "Zero-count columns",
                    "Unnamed columns",
                    "Carriage returns",
                    "GPU memory utilization",
                ],
                "correct": 3,
                "explanation": (
                    "The linter is focused on three specific CSV/data-quality problems."
                ),
            },

            {
                "id": "M16.L01.Q08",
                "section_id": "package-csv-linter",
                "question": "What does the console-script entry point map?",
                "options": [
                    "An installed command name to a Python module/function.",
                    "A CSV row to a database record.",
                    "A cloud region to a model.",
                    "A virtual environment to Docker.",
                ],
                "correct": 0,
                "explanation": (
                    "The source maps `csv-linter` to a Python `main()` function."
                ),
            },

            {
                "id": "M16.L01.Q09",
                "section_id": "click-first-command",
                "question": "What does Click provide even for the initially empty command?",
                "options": [
                    "A generated help interface",
                    "Automatic model training",
                    "Automatic cloud deployment",
                    "Dataset versioning",
                ],
                "correct": 0,
                "explanation": (
                    "The first installed command already supports `--help`."
                ),
            },

            {
                "id": "M16.L01.Q10",
                "section_id": "click-path-validation",
                "question": "Why use `click.Path(exists=True)`?",
                "options": [
                    "To reject nonexistent input paths at the CLI boundary.",
                    "To create every missing file automatically.",
                    "To upload the file to the cloud.",
                    "To convert CSV to JSON.",
                ],
                "correct": 0,
                "explanation": (
                    "The framework produces a clear validation error before the application tries to use the file."
                ),
            },

            {
                "id": "M16.L01.Q11",
                "section_id": "zero-count",
                "question": "What does the zero-count check return?",
                "options": [
                    "Names of columns whose Pandas count is zero.",
                    "Every dataframe value.",
                    "Only the CSV filename.",
                    "A cloud token.",
                ],
                "correct": 0,
                "explanation": (
                    "The function accumulates problematic column names."
                ),
            },

            {
                "id": "M16.L01.Q12",
                "section_id": "unnamed-columns",
                "question": "What does the unnamed-column function return in the source?",
                "options": [
                    "The number of matching columns.",
                    "The entire dataset.",
                    "Only the first matching value.",
                    "The row count.",
                ],
                "correct": 0,
                "explanation": (
                    "The source returns the count because the exact similar names are not important for that warning."
                ),
            },

            {
                "id": "M16.L01.Q13",
                "section_id": "carriage-returns",
                "question": "Why does the carriage-return scan catch `TypeError`?",
                "options": [
                    "Some fields may not be strings, so a string containment check may be invalid.",
                    "Pandas cannot iterate rows.",
                    "Every carriage return raises TypeError.",
                    "Click requires it.",
                ],
                "correct": 0,
                "explanation": (
                    "The source skips nonstring fields that cannot be tested the same way."
                ),
            },

            {
                "id": "M16.L01.Q14",
                "section_id": "automate-pain",
                "question": "What is the main DevOps lesson of the CSV linter?",
                "options": [
                    "Encode previously discovered manual failures into reusable automated checks.",
                    "Avoid automation until the system is perfect.",
                    "Only inspect datasets visually.",
                    "Always rewrite Pandas.",
                ],
                "correct": 0,
                "explanation": (
                    "The linter exists specifically to prevent forgotten past data problems."
                ),
            },

            {
                "id": "M16.L01.Q15",
                "section_id": "modularize",
                "question": "Why did the installed CLI break after moving files into a package?",
                "options": [
                    "The console entry point still referenced the old module/function path.",
                    "Click cannot work in packages.",
                    "Python packages cannot have `__init__.py`.",
                    "Pandas had been removed.",
                ],
                "correct": 0,
                "explanation": (
                    "The setup metadata had to be updated to point to `csv_linter.main:main`."
                ),
            },

            {
                "id": "M16.L01.Q16",
                "section_id": "separate-checks",
                "question": "Why move check functions into `checks.py`?",
                "options": [
                    "To separate responsibilities and improve readability/reuse.",
                    "To make the CLI harder to install.",
                    "To avoid functions.",
                    "To remove validation.",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly recommends grouping related responsibilities."
                ),
            },

            {
                "id": "M16.L01.Q17",
                "section_id": "microservices-jenga",
                "question": "What does the Jenga analogy illustrate?",
                "options": [
                    "Tightly coupled systems are harder to change safely than well-isolated reusable components.",
                    "Every microservice must be physically stacked.",
                    "Containers require games.",
                    "Monoliths have fewer dependencies.",
                ],
                "correct": 0,
                "explanation": (
                    "The analogy contrasts fragile coupling with reusable components."
                ),
            },

            {
                "id": "M16.L01.Q18",
                "section_id": "serverless-microservices",
                "question": "Why is serverless attractive for small ML microservices?",
                "options": [
                    "It lets developers focus on function logic while the provider handles much of the runtime/infrastructure.",
                    "It eliminates HTTP.",
                    "It requires custom operating-system management.",
                    "It prevents access to cloud ML services.",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes runtime abstraction and easy access to provider services."
                ),
            },

            {
                "id": "M16.L01.Q19",
                "section_id": "dont-reinvent",
                "question": "What does the chapter recommend when advanced computer vision is not your company's core competency?",
                "options": [
                    "Consider using an existing cloud capability rather than rebuilding it from scratch.",
                    "Always train a state-of-the-art model internally.",
                    "Avoid ML entirely.",
                    "Use only shell scripts.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter repeatedly argues for leveraging mature cloud offerings."
                ),
            },

            {
                "id": "M16.L01.Q20",
                "section_id": "create-cloud-function",
                "question": "Why does the source recommend keeping authentication enabled for Cloud Functions?",
                "options": [
                    "Unauthenticated public use can create security and direct financial risk.",
                    "Authentication makes JSON valid.",
                    "Cloud Functions cannot run without OAuth in the browser console.",
                    "It automatically improves translation quality.",
                ],
                "correct": 0,
                "explanation": (
                    "The warning explicitly connects unauthorized use with account/budget impact."
                ),
            },

            {
                "id": "M16.L01.Q21",
                "section_id": "json-http",
                "question": "Why is JSON useful in the chapter's HTTP examples?",
                "options": [
                    "Many languages and services can create and consume it easily.",
                    "Only Python understands it.",
                    "It removes the need for authentication.",
                    "It replaces HTTP.",
                ],
                "correct": 0,
                "explanation": (
                    "The source calls JSON a common language of web development."
                ),
            },

            {
                "id": "M16.L01.Q22",
                "section_id": "enable-api",
                "question": "What happened when the translation API was not enabled?",
                "options": [
                    "The function produced a permission-style error visible in logs and returned an HTTP error.",
                    "The translation silently succeeded.",
                    "The CLI became a Docker image.",
                    "Pandas fixed the configuration.",
                ],
                "correct": 0,
                "explanation": (
                    "The source shows an API-disabled error and explains how to enable the service."
                ),
            },

            {
                "id": "M16.L01.Q23",
                "section_id": "translation-api",
                "question": "What does the HTTP function pass into the translation helper?",
                "options": [
                    "The message text extracted from the JSON payload.",
                    "A Pandas dataframe only.",
                    "A Dockerfile.",
                    "The package entry point.",
                ],
                "correct": 0,
                "explanation": (
                    "The source's `main()` reads the message and delegates to `translator()`."
                ),
            },

            {
                "id": "M16.L01.Q24",
                "section_id": "authenticated-http",
                "question": "Which pieces are required in the source's authenticated curl example?",
                "options": [
                    "POST method, JSON body, content-type header, authorization token, and URL",
                    "Only a URL",
                    "Only a token",
                    "Only a requirements file",
                ],
                "correct": 0,
                "explanation": (
                    "The curl example makes each HTTP/authentication component explicit."
                ),
            },

            {
                "id": "M16.L01.Q25",
                "section_id": "gcloud-auth",
                "question": "What advantage does `gcloud functions call` provide?",
                "options": [
                    "It simplifies authenticated function invocation compared with constructing the raw HTTP request manually.",
                    "It removes the cloud function.",
                    "It disables authentication.",
                    "It packages the CLI for PyPI.",
                ],
                "correct": 0,
                "explanation": (
                    "The SDK command hides some of the low-level request construction."
                ),
            },

            {
                "id": "M16.L01.Q26",
                "section_id": "python-auth-demo",
                "question": "Why is invoking `gcloud auth print-identity-token` from Python presented only as a demonstration?",
                "options": [
                    "The source recommends a service account and proper API authentication tooling for production.",
                    "Python cannot run subprocesses.",
                    "Tokens are never needed.",
                    "Cloud Functions only support anonymous access.",
                ],
                "correct": 0,
                "explanation": (
                    "The source explicitly calls the subprocess method non-robust for production authentication."
                ),
            },

            {
                "id": "M16.L01.Q27",
                "section_id": "cloud-cli",
                "question": "What does the `cloud-translate` CLI accomplish for the user?",
                "options": [
                    "It hides repeated authentication/HTTP details behind one packaged command.",
                    "It trains a translation model locally.",
                    "It removes packaging.",
                    "It replaces Click with Bash.",
                ],
                "correct": 0,
                "explanation": (
                    "The CLI combines packaging, arguments, authentication, HTTP, and cloud service invocation."
                ),
            },

            {
                "id": "M16.L01.Q28",
                "section_id": "ml-cli-workflows",
                "question": "Which ML style can a command-line tool support according to the source?",
                "options": [
                    "On-the-fly training",
                    "Using a stored trained model",
                    "Calling AutoML or managed AI APIs",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": (
                    "The source presents CLI workflows across several model and service patterns."
                ),
            },

            {
                "id": "M16.L01.Q29",
                "section_id": "cli-distribution",
                "question": "Which is a CLI distribution target named in the source?",
                "options": [
                    "PyPI",
                    "Container registries",
                    "Linux packages",
                    "All of the above",
                ],
                "correct": 3,
                "explanation": (
                    "The chapter lists all of these, plus shared filesystems."
                ),
            },

            {
                "id": "M16.L01.Q30",
                "section_id": "chapter-system",
                "type": "open",
                "question": (
                    "Design an MLOps command-line application that automates a repeated ML or data task. "
                    "Include packaging, dependency isolation, Click arguments/validation, modularized domain logic, "
                    "either local ML or an authenticated cloud ML service, clear error behavior, and a distribution target. "
                    "Explain which parts should remain a CLI and which—if any—would benefit from becoming a microservice."
                ),
            },
        ],

        "passing_score": 70,
    },
}
