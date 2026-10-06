# Python environment setup

Source basis: BOOK-012 Appendix A.

Recommended baseline:

```bash
python --version
python -m venv venv
```

Windows activation:

```powershell
venv\Scripts\activate
```

macOS/Linux activation:

```bash
source venv/bin/activate
```

If you use VS Code, select the interpreter from the project virtual environment.

Install dependencies required by your implementation:

```bash
pip install -r requirements.txt
```

Keep your project interpreter and package installation environment aligned; using system Python by accident is a common cause of import failures.
