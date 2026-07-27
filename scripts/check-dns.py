#!/usr/bin/env python3
"""Check that radhouses.eu DNS is set up correctly for GitHub Pages.

Reads the zone straight from the authoritative nameservers, so it shows what the
internet actually sees rather than what a control panel claims. Flags missing
records, leftover parking records and the classic doubled-name mistake.

    python3 scripts/check-dns.py [domain]

No dependencies — stdlib only.
"""

import socket
import struct
import sys

DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "radhouses.eu"
PAGES_HOST = "poklembarado-del.github.io"

EXPECTED_A = {
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
}
EXPECTED_AAAA = {
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153",
}

A, NS, CNAME, SOA, MX, TXT, AAAA = 1, 2, 5, 6, 15, 16, 28
TYPE_NAMES = {A: "A", NS: "NS", CNAME: "CNAME", SOA: "SOA", MX: "MX", TXT: "TXT", AAAA: "AAAA"}

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
if not sys.stdout.isatty():
    GREEN = RED = YELLOW = DIM = RESET = ""

problems = []


def ok(msg):
    print(f"  {GREEN}ok{RESET}    {msg}")


def bad(msg):
    print(f"  {RED}FAIL{RESET}  {msg}")
    problems.append(msg)


def warn(msg):
    print(f"  {YELLOW}warn{RESET}  {msg}")


def query(name, qtype, server="8.8.8.8", timeout=6):
    """Return (rcode_name, [(type, value), ...]) for answers only."""
    header = struct.pack(">HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0)
    qname = b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\x00"
    packet = header + qname + struct.pack(">HH", qtype, 1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(packet, (server, 53))
        data, _ = sock.recvfrom(4096)
    except OSError as exc:
        return f"ERROR ({exc})", []
    finally:
        sock.close()

    rcode = struct.unpack(">H", data[2:4])[0] & 0xF
    answer_count = struct.unpack(">H", data[6:8])[0]

    def read_name(off):
        parts = []
        while True:
            length = data[off]
            if length == 0:
                off += 1
                break
            if length & 0xC0 == 0xC0:
                pointer = struct.unpack(">H", data[off : off + 2])[0] & 0x3FFF
                parts.append(read_name(pointer)[0])
                off += 2
                break
            parts.append(data[off + 1 : off + 1 + length].decode("latin1"))
            off += 1 + length
        return ".".join(parts), off

    off = 12
    _, off = read_name(off)
    off += 4

    records = []
    for _ in range(answer_count):
        _, off = read_name(off)
        rtype, _cls, _ttl, length = struct.unpack(">HHIH", data[off : off + 10])
        off += 10
        if rtype == A:
            value = socket.inet_ntoa(data[off : off + 4])
        elif rtype == AAAA:
            value = socket.inet_ntop(socket.AF_INET6, data[off : off + 16])
        elif rtype in (NS, CNAME):
            value = read_name(off)[0]
        elif rtype == MX:
            value = read_name(off + 2)[0]
        elif rtype == TXT:
            value = data[off + 1 : off + length].decode("latin1")
        else:
            value = f"<type {rtype}>"
        records.append((rtype, value))
        off += length

    rcodes = {0: "NOERROR", 2: "SERVFAIL", 3: "NXDOMAIN", 5: "REFUSED"}
    return rcodes.get(rcode, str(rcode)), records


def main():
    print(f"\nChecking {DOMAIN} for GitHub Pages\n")

    # --- Step 1: delegation ---------------------------------------------------
    print("Delegation (are nameservers set at the registrar?)")
    rcode, records = query(DOMAIN, NS)
    nameservers = [v for t, v in records if t == NS]

    if rcode == "NXDOMAIN" or not nameservers:
        bad(f"{DOMAIN} has no nameservers ({rcode}).")
        print(
            f"\n{DIM}  The domain is not delegated yet, so no records can be seen from\n"
            f"  outside no matter what the control panel shows. Set the ns1-ns4 fields\n"
            f"  at the registrar first, then re-run. Allow up to an hour.{RESET}\n"
        )
        return 1

    for ns in sorted(nameservers):
        ok(f"NS  {ns}")

    # Query the authoritative servers directly: no resolver caching, and it shows
    # the zone as published rather than as the panel renders it.
    auth_ip = None
    for ns in sorted(nameservers):
        try:
            auth_ip = socket.getaddrinfo(ns, 53, socket.AF_INET)[0][4][0]
            print(f"{DIM}  reading zone directly from {ns} ({auth_ip}){RESET}")
            break
        except OSError:
            continue
    if auth_ip is None:
        warn("could not resolve any nameserver; falling back to a public resolver")
        auth_ip = "8.8.8.8"

    # --- Step 2: apex A records ----------------------------------------------
    print(f"\nApex records ({DOMAIN} -> GitHub Pages)")
    _, records = query(DOMAIN, A, auth_ip)
    found_a = {v for t, v in records if t == A}
    apex_cname = [v for t, v in records if t == CNAME]

    if apex_cname:
        bad(f"apex has a CNAME ({apex_cname[0]}) — it must be A records, not a CNAME")

    for ip in sorted(EXPECTED_A - found_a):
        bad(f"missing A record: {ip}")
    for ip in sorted(found_a & EXPECTED_A):
        ok(f"A   {ip}")
    for ip in sorted(found_a - EXPECTED_A):
        bad(f"unexpected A record: {ip} — leftover parking record? delete it")

    # --- Step 3: IPv6 (optional) ---------------------------------------------
    _, records = query(DOMAIN, AAAA, auth_ip)
    found_aaaa = {v for t, v in records if t == AAAA}
    if not found_aaaa:
        warn("no AAAA records (IPv6) — optional, but recommended")
    else:
        for ip in sorted(found_aaaa & EXPECTED_AAAA):
            ok(f"AAAA {ip}")
        for ip in sorted(found_aaaa - EXPECTED_AAAA):
            bad(f"unexpected AAAA record: {ip}")

    # --- Step 4: www ----------------------------------------------------------
    print(f"\nwww.{DOMAIN}")
    _, records = query(f"www.{DOMAIN}", A, auth_ip)
    cnames = [v.rstrip(".") for t, v in records if t == CNAME]
    if not records:
        warn(f"www.{DOMAIN} does not resolve — add a CNAME to {PAGES_HOST}")
    elif cnames and cnames[0].lower() == PAGES_HOST.lower():
        ok(f"CNAME -> {cnames[0]}")
    elif cnames:
        bad(f"www points at {cnames[0]}, expected {PAGES_HOST}")
    else:
        warn("www resolves via A records rather than a CNAME — works, but a CNAME is tidier")

    # --- Step 5: doubled-name mistake ----------------------------------------
    print("\nCommon mistakes")
    doubled = f"{DOMAIN}.{DOMAIN}"
    rcode, records = query(doubled, A, auth_ip)
    if records:
        bad(f"{doubled} exists — a Host field was filled with the full domain name")
    else:
        ok("no doubled-name records")

    doubled_www = f"www.{DOMAIN}.{DOMAIN}"
    _, records = query(doubled_www, A, auth_ip)
    if records:
        bad(f"{doubled_www} exists — delete it and use Host 'www'")

    # --- Step 6: does the site answer? ---------------------------------------
    print("\nSite")
    for host in (DOMAIN, f"www.{DOMAIN}"):
        try:
            with socket.create_connection((host, 443), timeout=8):
                ok(f"https://{host} accepts connections")
        except OSError as exc:
            warn(f"https://{host} not reachable yet ({exc.__class__.__name__})")

    # --- Summary --------------------------------------------------------------
    print()
    if problems:
        print(f"{RED}{len(problems)} problem(s) to fix:{RESET}")
        for p in problems:
            print(f"  - {p}")
        print()
        return 1

    print(f"{GREEN}DNS looks correct.{RESET}")
    print(
        f"{DIM}If the site does not load yet, check Settings -> Pages: the custom domain\n"
        f"should read {DOMAIN} and 'Enforce HTTPS' should be ticked once available.{RESET}\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
