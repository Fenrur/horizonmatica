#!/usr/bin/env python3
"""Packs the mod (hmod/) into dist/horizonmatica-<version>.hmod.

    python tools/package.py [--launcher <path>] [--sign]

The package itself is made by `cargo horizon-mod build` (deterministic: anyone can rebuild it from the tag
and get the same SHA-256). Before that, the registry-only Cargo.lock is regenerated with
`horizon-launcher native-lock`, because a plain `cargo check` rewrites it. --launcher points at
horizon-launcher(.exe) when it isn't on PATH. Afterwards `cargo horizon-mod check <package>` checks it.

--sign signs the package with minisign (default secret key ~/.minisign/minisign.key, asks for its password)
and verifies the signature against minisign.pub, writing <package>.minisig next to it.
"""
import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
MOD = ROOT / "hmod"


def run(*cmd: str) -> None:
    subprocess.run(list(cmd), cwd=MOD, check=True, stdin=subprocess.DEVNULL)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--launcher", default=shutil.which("horizon-launcher"), help="path to horizon-launcher")
    ap.add_argument("--sign", action="store_true", help="sign the package with minisign")
    args = ap.parse_args()
    if not args.launcher:
        raise SystemExit("horizon-launcher is not on PATH: pass --launcher <path>")

    toml = (MOD / "horizon-mod.toml").read_text(encoding="utf-8")
    version = re.search(r'^version\s*=\s*"([^"]+)"', toml, re.M).group(1)
    horizon = re.search(r'^horizon\s*=\s*"([0-9a-f]{40})"', toml, re.M).group(1)
    out = ROOT / "dist" / f"horizonmatica-{version}.hmod"
    sig = out.with_name(out.name + ".minisig")
    if sig.exists() and not args.sign:
        # A released package must not be replaced unnoticed: its signature would no longer match.
        raise SystemExit(f"{sig.name} exists: {out.name} is signed already (pass --sign to sign it again)")

    run(args.launcher, "native-lock", ".", "--update-lock")
    run("cargo", "horizon-mod", "build")
    out.parent.mkdir(exist_ok=True)
    shutil.copyfile(MOD / "target" / "horizon-mod" / "horizonmatica.hmod", out)
    run("cargo", "horizon-mod", "check", str(out))
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"wrote {out} (Horizon {horizon[:10]})\nsha256 {digest}")

    if args.sign:
        sig.unlink(missing_ok=True)  # never leave a stale signature next to a new package
        subprocess.run(["minisign", "-Sm", str(out)], check=True)
        subprocess.run(["minisign", "-Vm", str(out), "-p", str(ROOT / "minisign.pub")], check=True)
        print(f"wrote {sig}")


if __name__ == "__main__":
    main()
