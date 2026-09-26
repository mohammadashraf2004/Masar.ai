# Local MCP servers with Node.js / npx

Source basis: BOOK-012 Appendix B.

Many local MCP reference/community servers are distributed as npm packages.

## Verify Node tooling

Use Node.js 20+ and confirm:

```bash
node --version
npm --version
npx --version
```

## npx launch pattern

```bash
npx -y <package-name> [server-arguments...]
```

The `-y` flag matters when an MCP client launches the process non-interactively; without it, `npx` may wait for an install confirmation that the client cannot answer.

Example filesystem server pattern:

```bash
npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/directory
```

A client config commonly stores `command: "npx"` and puts `-y`, the package name, and server arguments in the args list.

## Troubleshooting

- `npx: command not found`: reopen the shell and verify Node/PATH.
- Permission errors: fix the Node installation ownership; a version manager is generally safer than a root-owned global install.
- MCP server exits immediately: run the exact `npx` command directly in a terminal to expose stderr.
- MCP client hangs at startup: check whether `-y` was omitted.
- Suspected stale npm cache: inspect/pin the package version before using broad cache-clearing commands.

Treat filesystem paths, network access, and credentials as security boundaries. An MCP server should receive only the scope it needs.
