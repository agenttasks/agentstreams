# DBeaver Community Edition — Neon Postgres Setup

Connect DBeaver CE to the agentstreams Neon Postgres instance (project `calm-paper-82059121`, database `neondb`, region `us-east-2`).

## Prerequisites

- DBeaver Community Edition 24.x or later — https://dbeaver.io/download/
- A Neon account with access to the `calm-paper-82059121` project
- The bundled PostgreSQL JDBC driver (DBeaver installs it automatically on first connection)

## Connection Details

Open the Neon Console at https://console.neon.tech/app/projects/calm-paper-82059121?database=neondb and click the **Connect** button in the top-right. Choose your branch and role, then copy the connection string. It has the form:

```
postgresql://<role>:<password>@ep-XXXX-XXXX-XXXXXX.us-east-2.aws.neon.tech/neondb?sslmode=require
```

You need four values from it:

| Field    | Where to find it                                               |
|----------|----------------------------------------------------------------|
| Host     | Everything between `@` and `/neondb` — e.g. `ep-XXXX.us-east-2.aws.neon.tech` |
| Port     | 5432 (standard Postgres; not shown in the string, use default) |
| Database | `neondb`                                                       |
| Username | The role name before the `:` in the connection string          |
| Password | The value between `:` and `@`                                  |

## Step-by-step Connection Setup

1. Open DBeaver. In the toolbar click **New Database Connection** (plug icon) or use `Database > New Database Connection`.
2. Select **PostgreSQL** and click **Next**.
3. On the **Main** tab fill in the fields individually:
   - **Host**: `ep-XXXX-XXXX-XXXXXX.us-east-2.aws.neon.tech` (your endpoint hostname from the connection string)
   - **Port**: `5432`
   - **Database**: `neondb`
   - **Username**: your Neon role name
   - **Password**: your Neon role password — check **Save password locally** to avoid re-entering it
4. Leave the **URL** field alone. Do not paste the full connection string there. The pgJDBC driver used by DBeaver does not accept the `postgresql://` URI format in that field; entering it breaks SSL and keepalive settings that are configured separately.

## SSL Configuration

Neon requires SSL. Without it the connection is rejected.

1. On the connection dialog, open the **Driver Properties** tab (at the bottom of the tab list).
2. Find the `sslmode` property and set its value to `require`.
3. If `sslmode` is not listed, click **Add** and enter it manually.

## Keep-Alive Configuration

Neon scales compute to zero after approximately 5 minutes of idle time. When that happens, an open DBeaver connection receives a TCP RST and becomes unusable. Setting a keepalive interval shorter than 5 minutes prevents Neon from sleeping while DBeaver is open.

1. On the connection dialog, open the **Connection Settings** tab.
2. Go to the **Initialization** sub-tab.
3. Enable **Keep-Alive** and set the interval to **60 seconds**.

This sends a lightweight `SELECT 1` over the connection every 60 seconds, which is sufficient to keep the compute endpoint awake during active work sessions. You will still need to reconnect if the machine sleeps or DBeaver is minimized for an extended period.

## Multiple Developer Branches

Neon creates a separate compute endpoint for each branch. To work against `dev/alice`, `dev/bob`, and `dev/carol` simultaneously, save a separate DBeaver connection for each:

1. Go to **Database > New Database Connection** and create a connection for each branch.
2. Use the endpoint hostname shown in the Neon Console for that branch — each branch has a distinct `ep-XXXX` prefix.
3. Name each connection clearly, e.g. `neon-dev-alice`, `neon-dev-bob`, `neon-dev-carol`.
4. Branch connections share the same port (5432), database name (`neondb`), and SSL settings. Only the **Host** differs.

## Testing the Connection

1. On the connection dialog, click **Test Connection**.
2. DBeaver will attempt to download the PostgreSQL JDBC driver if it is not already installed — allow this.
3. A dialog showing **Connected** with the server version confirms success.
4. Click **Finish** to save the connection.

## Troubleshooting

**SNI hostname mismatch / SSL handshake failure**
Neon uses SNI to route connections to the correct compute endpoint. DBeaver versions before 23.x use an older JDBC driver that does not send SNI. Upgrade to DBeaver CE 24.x or later to resolve this.

**Connection timeout immediately**
Verify that `sslmode` is set to `require` in Driver Properties. Connections without SSL are refused at the Neon proxy layer before the TCP handshake completes.

**"Connection refused" after idle period**
The compute endpoint scaled to zero. Click the connection in the Database Navigator and press `F5` (Reconnect) or right-click and choose **Invalidate/Reconnect**. Neon cold-start takes 1-3 seconds. Enabling the 60-second keepalive (see above) prevents this during active sessions.

**Authentication failed for user**
Password values in Neon connection strings are URL-encoded. Copy only the password segment and URL-decode any `%XX` sequences (e.g. `%40` becomes `@`) before pasting into the DBeaver password field.
