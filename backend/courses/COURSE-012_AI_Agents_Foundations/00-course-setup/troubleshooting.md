# Setup troubleshooting

## Authentication errors
Verify the credential exists in the active environment and that the application actually loads that environment.

## `ModuleNotFoundError`
Confirm:
1. the virtual environment is active;
2. `python` points to that environment;
3. dependencies were installed into that same environment.

## `node` / `npx` not found
Open a new terminal and rerun the version checks. Confirm the Node installation path is present in the shell PATH.

## MCP process appears stuck
Run the server command directly. Check for an interactive npm prompt, bad path, missing environment variable, or server startup error.

## General rule
Debug the lowest independent layer first:
environment → server/tool → schema → agent connection → workflow.
