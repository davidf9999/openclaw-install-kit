# Google Integration Test Plan

This plan validates Google services in the safest practical order for `openclaw-install-kit`.

## Goals

- Validate Google integrations on the local OpenClaw install first
- Keep account scope and OAuth permissions as small as possible
- Separate services when the user already keeps them separate in real life
- Avoid treating Google as one monolithic integration

## Recommended order

1. Calendar
2. Contacts
3. Gmail
4. Drive only after a supported path is confirmed

## Security baseline

- Use a dedicated Google test account or Workspace identity when possible
- Prefer separate Google accounts for separate services if the user already split them that way
- Enable only the APIs/scopes explicitly selected in `deployment-brief.md`
- Keep OAuth files under `~/.openclaw/`
- Lock down `credentials.json` and `token.json` with `chmod 600`
- Revoke test tokens after validation

## Preconditions

- OpenClaw is already installed and running locally
- `deployment-brief.md` lists the Google services to test
- A browser is available on the local machine for OAuth
- The Google account or Workspace identity is ready

## Test 1: Calendar

### Setup

1. Create or choose a dedicated Google test account.
2. Create a Google Cloud project for the test account.
3. Enable only `Google Calendar API`.
4. Create OAuth Desktop App credentials.
5. Place `credentials.json` in `~/.openclaw/`.
6. Run:

```bash
chmod 600 ~/.openclaw/credentials.json
openclaw auth google
```

### Verify

- Confirm `token.json` is created in `~/.openclaw/`
- Confirm `openclaw status --deep` reports Google/Calendar as healthy if the current build exposes that status
- Ask OpenClaw for a calendar query through the dashboard or Telegram

### Acceptance criteria

- OAuth completes without error
- Calendar query returns the expected results
- Token and credential files remain restricted to the local host

## Test 2: Contacts

Repeat the Calendar flow, but enable only `People API` if the installed build supports Contacts as a separate scope.

### Acceptance criteria

- Contact lookup returns the expected result
- No additional Google APIs were enabled beyond the selected scope

## Test 3: Gmail

Treat Gmail as a separate, more sensitive stage.

### Recommended caution

- Use a mail-specific test account if possible
- Enable only the minimum Gmail scope required by the installed OpenClaw build
- Keep inbox access separate from Calendar/Contacts if the real-world account split demands it

### Acceptance criteria

- The installed build exposes a supported Gmail flow
- Mailbox access or webhook behavior works as documented
- The OAuth token is scoped only to the Gmail test case

## Test 4: Drive

Do not claim Drive as supported until a documented OpenClaw path exists and a full test passes.

### Acceptance criteria

- The OpenClaw version in use exposes a supported Drive flow
- The workflow can be completed end to end
- Scope is explicitly documented as read-only, upload, or folder-limited

## Logging

Record each test with:

- Date
- Google account used
- Services enabled
- Scopes selected
- Result
- Any security concerns
- Any deviations from the documented flow

## Outcome categories

- `pass` - service works end to end with the documented scope
- `partial` - service starts but scope or behavior is not yet acceptable
- `fail` - service does not work or requires unsupported assumptions
- `pending` - service has no confirmed supported path yet

