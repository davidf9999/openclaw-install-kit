# Calendar-First Google Test Run

Use this for the smallest useful Google validation slice on a local OpenClaw install.

## Goal

Validate Google Calendar only. Do not enable Gmail or Drive in this run.

## Before you start

- OpenClaw is already installed and running locally
- `deployment-brief.md` lists Calendar as selected
- You have a dedicated Google test account or Workspace identity
- You know which Google account owns Calendar for this test
- A browser is available for OAuth

## Scope

- Enable only `Google Calendar API`
- Use `Google Workspace` -> `Calendar: yes`
- Leave `Contacts`, `Gmail`, and `Drive` out of this run
- Keep OAuth files local under `~/.openclaw/`

## Steps

1. In Google Cloud Console, create or choose a test project.
2. Enable only `Google Calendar API`.
3. Create OAuth 2.0 credentials for a Desktop app.
4. Download `credentials.json` and place it in `~/.openclaw/`.
5. Lock down the file:

```bash
chmod 600 ~/.openclaw/credentials.json
```

6. Run the Google auth flow:

```bash
export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
openclaw auth google
```

7. Confirm `token.json` is created in `~/.openclaw/`.
8. Ask OpenClaw for a read-only calendar query through Telegram or the dashboard.
9. Confirm the result matches the test account's calendar.

## Pass criteria

- OAuth completes successfully
- Calendar query works
- No Gmail or Drive scopes were added
- `credentials.json` and `token.json` remain local and locked down

## Stop criteria

- If Gmail or Drive looks necessary, stop and treat it as a separate stage
- If the installed OpenClaw version does not expose a working Calendar path, stop and report the exact output

## After the run

- Revoke the OAuth grant if the test account will not be reused
- Record the account used, scopes enabled, and result in `TESTING.md`

