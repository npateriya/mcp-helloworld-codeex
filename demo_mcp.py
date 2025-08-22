from fastmcp import FastMCP
import os
import random
import datetime
import subprocess
import shlex
import ipaddress


mcp = FastMCP("Tiny MCP Playground 🎲📝")


def _roll_dice(sides: int = 6, rolls: int = 1) -> dict:
    """Roll dice and return individual results and total.

    - sides: number of faces on each die (>= 2)
    - rolls: number of dice to roll (1..100)
    """
    if sides < 2 or rolls < 1 or rolls > 100:
        raise ValueError("Invalid input: require sides>=2 and 1<=rolls<=100")

    results = [random.randint(1, sides) for _ in range(rolls)]
    return {
        "sides": sides,
        "rolls": rolls,
        "results": results,
        "total": sum(results),
    }

roll_dice = mcp.tool(_roll_dice)





def _nslookup(name: str, record: str = "", server: str = "", timeout: float = 5.0) -> dict:
    """Run nslookup for a hostname or IP.

    - name: hostname or IP (e.g., example.com, 8.8.8.8)
    - record: optional DNS record type (A, AAAA, CNAME, MX, TXT, NS, PTR, SOA)
    - server: optional DNS server to query (e.g., 8.8.8.8)
    - timeout: seconds to wait before giving up
    """
    allowed_records = {"A", "AAAA", "CNAME", "MX", "TXT", "NS", "PTR", "SOA"}
    record_upper = record.upper().strip()
    if record and record_upper not in allowed_records:
        raise ValueError(f"Unsupported record type: {record}. Supported: {sorted(allowed_records)}")

    cmd = ["nslookup"]
    if record_upper:
        cmd.append(f"-type={record_upper}")
    cmd.append(name)
    if server.strip():
        cmd.append(server.strip())

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": result.returncode == 0,
            "exit_code": result.returncode,
            "command": " ".join(shlex.quote(part) for part in cmd),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "ok": False,
            "exit_code": None,
            "command": " ".join(shlex.quote(part) for part in cmd),
            "stdout": e.stdout or "",
            "stderr": (e.stderr or "") + f"\nTimed out after {timeout} seconds",
        }

nslookup = mcp.tool(_nslookup)


def _cidr_info_ipv4(cidr: str) -> dict:
    """Return IPv4 CIDR info: netmask, wildcard, first/last, total hosts.

    Example: cidr="10.0.0.0/24"
    """
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
    except Exception as e:
        raise ValueError(f"Invalid IPv4 CIDR: {cidr}: {e}")

    network_str = str(network.network_address)
    broadcast_str = str(network.broadcast_address)
    netmask_str = str(network.netmask)

    # Wildcard mask is inverse of netmask
    wildcard_int = int(ipaddress.IPv4Address("255.255.255.255")) ^ int(network.netmask)
    wildcard_str = str(ipaddress.IPv4Address(wildcard_int))

    # Include network and broadcast as first/last for simplicity, matching example
    total_hosts = network.num_addresses

    return {
        "cidr": str(network),
        "netmask": netmask_str,
        "wildcard": wildcard_str,
        "first_ip": network_str,
        "last_ip": broadcast_str,
        "total_hosts": total_hosts,
    }

cidr_info_ipv4 = mcp.tool(_cidr_info_ipv4)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=9000,
        path="/mcp",
    )


