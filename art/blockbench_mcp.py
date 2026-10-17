import json
import sys
import urllib.request
from pathlib import Path

URL = 'http://localhost:3000/bb-mcp'


def request(body, session=None):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    if session:
        headers['Mcp-Session-Id'] = session
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=120) as response:
        raw = response.read().decode()
        if raw.startswith('event:') or raw.startswith('data:'):
            raw = next(line[6:] for line in raw.splitlines() if line.startswith('data: '))
        return response.headers.get('mcp-session-id'), json.loads(raw) if raw else {}


def call(name, arguments):
    session, initialized = request({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'FarmerPlusArt', 'version': '1.0'}}})
    if 'error' in initialized:
        raise RuntimeError(initialized['error'])
    request({'jsonrpc': '2.0', 'method': 'notifications/initialized'}, session)
    _, result = request({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}}, session)
    if 'error' in result or result.get('result', {}).get('isError'):
        raise RuntimeError(result)
    return result['result']


if __name__ == '__main__':
    code = Path(sys.argv[1]).read_text(encoding='utf-8')
    print(json.dumps(call('risky_eval', {'code': code}), ensure_ascii=True))
