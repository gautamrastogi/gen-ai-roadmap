import ctypes
import ctypes.wintypes as wt
import json
import ssl

import httpx
import truststore


class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ("Flags", wt.DWORD),
        ("Type", wt.DWORD),
        ("TargetName", wt.LPWSTR),
        ("Comment", wt.LPWSTR),
        ("LastWritten", wt.LARGE_INTEGER),
        ("CredentialBlobSize", wt.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),
        ("Persist", wt.DWORD),
        ("AttributeCount", wt.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wt.LPWSTR),
        ("UserName", wt.LPWSTR),
    ]


def read_cred(target: str) -> str:
    advapi = ctypes.windll.advapi32
    ptr = ctypes.c_void_p()
    ok = advapi.CredReadW(target, 1, 0, ctypes.byref(ptr))
    if not ok:
        raise RuntimeError(f"CredRead failed: {ctypes.GetLastError()}")
    cred = ctypes.cast(ptr, ctypes.POINTER(CREDENTIAL)).contents
    raw = bytes(cred.CredentialBlob[: cred.CredentialBlobSize])
    advapi.CredFree(ptr)
    if len(raw) >= 2 and raw[1] == 0:
        return raw.decode("utf-16-le").rstrip("\x00")
    return raw.decode("utf-8").rstrip("\x00")


token = read_cred("copilot-cli/https://github.com:GRAST_danske")
print(f"OAuth token prefix: {token[:8]}..., len={len(token)}")

ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ctx, timeout=20)

# Exchange for a short-lived Copilot session token
r = client.get(
    "https://api.github.com/copilot_internal/v2/token",
    headers={
        "Authorization": f"Bearer {token}",
        "editor-version": "vscode/1.93.0",
        "editor-plugin-version": "copilot/1.229.0",
        "user-agent": "GithubCopilot/1.229.0",
    },
)
print(f"Copilot token exchange: {r.status_code}")
print(r.text[:500])
