#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
import base64

def get_rpc_config():
    host = os.environ.get("RPC_HOST", os.environ.get("ZEBRA_RPC_HOST", "127.0.0.1"))
    port = os.environ.get("RPC_PORT", os.environ.get("ZEBRA_RPC_PORT", "18232"))
    user = os.environ.get("RPC_USER", os.environ.get("ZEBRA_RPC_USER", "zcashuser"))
    password = os.environ.get("RPC_PASSWORD", os.environ.get("ZEBRA_RPC_PASSWORD", "zcashpassword"))
    url = os.environ.get("RPC_URL", os.environ.get("ZEBRA_RPC_URL", f"http://{host}:{port}/"))
    return url, user, password

def make_rpc_call(method, params=None):
    url, user, password = get_rpc_config()
    payload = json.dumps({
        "jsonrpc": "1.0",
        "id": "zchain-cli",
        "method": method,
        "params": params or []
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    if user and password:
        credentials = f"{user}:{password}"
        encoded_creds = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        req.add_header("Authorization", f"Basic {encoded_creds}")

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if res_data.get("error"):
                sys.stderr.write(f"RPC Error: {res_data['error']}\n")
                sys.exit(1)
            return res_data.get("result")
    except Exception as e:
        sys.stderr.write(f"Error communicating with Zebra RPC: {e}\n")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Error: Missing command. Usage: zchain <height|block <height>>\n")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "height":
        height = make_rpc_call("getblockcount")
        print(height)

    elif cmd == "block":
        if len(sys.argv) < 3:
            sys.stderr.write("Error: Missing block height. Usage: zchain block <height>\n")
            sys.exit(1)
        
        try:
            target_height = int(sys.argv[2])
        except ValueError:
            sys.stderr.write("Error: Block height must be an integer.\n")
            sys.exit(1)

        block_hash = make_rpc_call("getblockhash", [target_height])
        
        # Zebra's getblock accepts verbosity=1 (JSON object)
        block_data = make_rpc_call("getblock", [block_hash, 1])
        
        timestamp = block_data.get("time")
        print(f"Hash: {block_hash}")
        print(f"Timestamp: {timestamp}")

    else:
        sys.stderr.write(f"Error: Unknown command '{cmd}'. Valid commands: height, block <height>\n")
        sys.exit(1)

if __name__ == "__main__":
    main()