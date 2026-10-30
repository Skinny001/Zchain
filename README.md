# zchain CLI

`zchain` is a Python CLI utility for querying block and chain state from a Zcash Zebra regtest node via JSON-RPC.

---

## Features

- **Chain Height:** Fetch the current block height (`zchain height`).
- **Block Info:** Get the hash and timestamp for a target block (`zchain block <height>`).
- **Error Handling:** Prints clear errors to `stderr` and exits with code `1` on invalid input or RPC connection failures.
- **Dynamic Configuration:** Supports runtime environment variables for seamless execution across local Docker instances and CI test suites.

---

## Environment Variables

`zchain` reads configuration from standard environment variables with automatic fallback defaults. This allows local development (`RPC_PORT=29232` via Docker Compose host mapping) without breaking GitHub Actions CI pipelines running natively on port `18232`.

| Variable | Fallback Variable | Default | Purpose & Usage |
| :--- | :--- | :--- | :--- |
| `RPC_HOST` | `ZEBRA_RPC_HOST` | `127.0.0.1` | Host IP address of the Zebra RPC node. |
| `RPC_PORT` | `ZEBRA_RPC_PORT` | `18232` | RPC port. Set to `29232` when testing against local Docker containers mapped to host ports. |
| `RPC_USER` | `ZEBRA_RPC_USER` | `zcashuser` | Basic Auth HTTP RPC username. |
| `RPC_PASSWORD` | `ZEBRA_RPC_PASSWORD` | `zcashpassword` | Basic Auth HTTP RPC password. |
| `RPC_URL` | `ZEBRA_RPC_URL` | `http://{HOST}:{PORT}/` | Full RPC endpoint URL. Overrides host/port settings if set directly. |

---

## Installation

```bash
git clone [https://github.com/your-username/zchain.git](https://github.com/your-username/zchain.git)
cd zchain

python3 -m venv venv
source venv/bin/activate
pip install pytest
