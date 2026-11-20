#!/usr/bin/env python3
"""Pack the native mod into dist/horizonmatica-<version>.hmod.

Use --sign to sign and verify the archive with minisign.
"""
import argparse
import hashlib
import pathlib
import subprocess
import tomllib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "mixins" / "horizonmatica"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sign", action="store_true", help="sign the package with minisign")
    args = ap.parse_args()
    manifest = BUNDLE / "horizon-mod.toml"
    with manifest.open("rb") as source:
        mod = tomllib.load(source)

    out = ROOT / "dist" / f"{mod['id']}-{mod['version']}.hmod"
    out.parent.mkdir(exist_ok=True)

    entries = {name: BUNDLE / name for name in ("horizon-mod.toml", "Cargo.toml", "Cargo.lock")}
    entries.update({name: ROOT / name for name in ("LICENSE", "icon.png")})
    for path in (BUNDLE / "src").rglob("*"):
        rel = path.relative_to(BUNDLE)
        if "target" not in rel.parts and path.is_file() and path.suffix in (".rs", ".toml"):
            entries[rel.as_posix()] = path

    for path in (BUNDLE / "assets").rglob("*"):
        if path.is_file():
            entries[path.relative_to(BUNDLE).as_posix()] = path

    # Keep names, order, permissions and timestamps stable across builds.
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, path in sorted(entries.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"wrote {out} ({len(entries)} files, Horizon {mod['native']['horizon'][:10]})\nsha256 {digest}")
    if args.sign:
        sig = out.with_name(out.name + ".minisig")
        sig.unlink(missing_ok=True)
        subprocess.run(["minisign", "-Sm", str(out)], check=True)
        subprocess.run(["minisign", "-Vm", str(out), "-p", str(ROOT / "minisign.pub")], check=True)
        print(f"wrote {sig}")


if __name__ == "__main__":
    main()
