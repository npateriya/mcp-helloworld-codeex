# MCP HelloWorld for Code Exchange – integrated MCP Inspector Demo
MCP HelloWorld for Code Exchange with web MCP Inspector

## Try it in Cisco DevNet DevEnv (no local setup)
Click to launch a browser-based environment with this repo pre-cloned and FastMCP preinstalled:

[![Run MCP Inspector IDE in Cloud](assets/run-in-cloud-ide.svg)](https://testing-developer.cisco.com/devenv/?id=devenv-base-mcp-inspector&GITHUB_SOURCE_REPO=https://github.com/npateriya/mcp-helloworld-codeex)

Note: This DevEnv link is Cisco-internal.

Once the DevEnv opens:
- Clone repo `git clone https://github.com/npateriya/mcp-helloworld-codeex`
- Install requirements `pip install -r requirements.txt`
- Start the server (HTTP on 9000) if needed: `python demo_mcp.py`
  - MCP server endpoint: `http://127.0.0.1:9000/mcp` (transport: streamable-http)
- To open the MCP Inspector via the proxy, run this in a new terminal tab ('+' to open a new tab):

```bash
./scripts/mcp_inspector_url.sh
```

<details>
<summary>Show raw echo command for mcp inspector URL</summary>

```bash
echo "${DEVENV_APP_8080_URL}?MCP_PROXY_AUTH_TOKEN=${DEVENV_PASSWORD}&MCP_PROXY_FULL_ADDRESS=${DEVENV_APP_8081_URL}"
```

</details>

Open the printed URL in a new tab. In Inspector, choose the appropriate transport (HTTP/STDIO based on your use) and connect. You should see logs like 200 OK requests in the DevEnv terminal when invoking tools.
  - MCP server endpoint: `http://127.0.0.1:9000/mcp` (transport: streamable-http). Configure these in MCP Inspector and test tools.

### Local run (quick)
If you prefer local instead of DevEnv:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python demo_mcp.py
```



## What this demo provides
- **roll_dice(sides=6, rolls=1)**: Returns individual dice results and total.
- **nslookup(name, record?, server?, timeout=5.0)**: Wraps the system `nslookup` for quick DNS checks. Returns `ok`, `exit_code`, `command`, `stdout`, `stderr`.
- **cidr_info_ipv4(cidr)**: IPv4-only CIDR facts like netmask, wildcard, first/last IP, and total addresses.

## Requirements
- `nslookup` available on your system (macOS has it by default). Verify with: `which nslookup`.

## Quick start (venv)
```bash
cd /Users/npateriy/devnet/src/wwwin-github.cisco.com/DevNet/mcp-helloworld-codeex
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip wheel setuptools
python -m pip install -r requirements.txt
```

## Run as HTTP (Streamable) on port 9000
The script is configured to start an HTTP MCP server on `http://127.0.0.1:9000/mcp`.

```bash
source .venv/bin/activate
python demo_mcp.py
```

Health checks / quick probes:
- Base server: `curl -i http://127.0.0.1:9000/`
- MCP endpoint (expects MCP client payloads): `curl -i http://127.0.0.1:9000/mcp` (GET may return 406; that still confirms the endpoint is up.)


## Tool reference
### cidr_info_ipv4
Input:
```json
{ "cidr": "10.0.0.0/24" }
```
Output:
```json
{
  "cidr": "10.0.0.0/24",
  "netmask": "255.255.255.0",
  "wildcard": "0.0.0.255",
  "first_ip": "10.0.0.0",
  "last_ip": "10.0.0.255",
  "total_hosts": 256
}
```

### nslookup
Inputs (examples):
```json
{ "name": "example.com" }
{ "name": "example.com", "record": "AAAA" }
{ "name": "example.com", "record": "A", "server": "8.8.8.8" }
```

### roll_dice
Input:
```json
{ "rolls": 3 }
```
Output:
```json
{ "sides": 6, "rolls": 3, "results": [2, 6, 5], "total": 13 }
```

