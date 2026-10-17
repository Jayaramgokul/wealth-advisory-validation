"""Render catalogue.yaml into catalogue.md (both in 04-test-design).

    python 04-test-design/render_catalogue.py
"""

from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> Path:
    data = yaml.safe_load((HERE / "catalogue.yaml").read_text())
    tests = data["tests"]
    by_group = {g["code"]: [t for t in tests if t["id"].startswith(g["code"])] for g in data["passes"]}

    def lens(g):
        doc = g.get("doc")
        if doc and (ROOT / "03-research" / doc).exists():
            return f"[{g['lens']}](../03-research/{doc})"
        return g["lens"]

    lines = [
        "# Test catalogue",
        "",
        "*Generated from [catalogue.yaml](catalogue.yaml) by `render_catalogue.py`. Edit the YAML, not this page.*",
        "",
        f"{len(tests)} tests in {len(data['passes'])} groups. Each group reads one or more public sources as a lens "
        "and asks what an existing validation would miss. \"Agreed tolerance\" means a bar the validator and the "
        "model owner fix in advance; this repository does not prescribe one. Linked lenses have a full research "
        "write-up.",
        "",
        "| Group | Lens | Question it asks | Tests |",
        "|---|---|---|---|",
    ]
    for g in data["passes"]:
        lines.append(f"| **{g['code']}** | {lens(g)} | {g['question']} | {len(by_group[g['code']])} |")
    lines += ["", "▶ marks tests with an illustration script in [05-illustrations](../05-illustrations/).", ""]
    for g in data["passes"]:
        lines += [f"## {g['code']}: {lens(g)}", "", g["question"], "",
                  "| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |",
                  "|---|---|---|---|---|---|---|"]
        for t in by_group[g["code"]]:
            ident = t["id"]
            if t.get("script"):
                ident = f"[{t['id']} ▶](../05-illustrations/{t['script']})"
            lines.append(f"| {ident} | **{t['name']}** | {t['risk']} | {t['method']} | {t['passes_if']} | "
                         f"{t['nist']} | {t['hook']} |")
        lines.append("")
    out = HERE / "catalogue.md"
    out.write_text("\n".join(lines).rstrip("\n") + "\n")
    return out


if __name__ == "__main__":
    print(f"wrote {main()}")
