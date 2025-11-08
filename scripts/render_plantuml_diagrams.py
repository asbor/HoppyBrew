#!/usr/bin/env python3
"""Render all PlantUML diagrams into categorized PNG/SVG outputs for the wiki."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
import shutil
import tempfile


@dataclass(frozen=True)
class Paths:
    repo_root: Path

    @property
    def plantuml_bin(self) -> Path:
        return self.repo_root / "tools" / "plantuml"

    @property
    def source_root(self) -> Path:
        return self.repo_root / "documents" / "docs" / "plantuml"

    @property
    def diagram_root(self) -> Path:
        return self.repo_root / "documents" / "wiki-exports" / "diagrams"


def categorize(puml_path: Path) -> str:
    """Mirror the bash categorization logic for deterministic placement."""
    dirname = str(puml_path.parent).lower()
    stem = puml_path.stem.lower()

    if "erd" in dirname or "database" in dirname:
        return "database"
    if "component" in dirname:
        return "components"
    if "api" in dirname:
        return "api"
    if "workflow" in dirname or "process" in dirname:
        return "workflows"

    if any(key in stem for key in ("erd", "database", "schema")):
        return "database"
    if any(key in stem for key in ("component", "architecture")):
        return "architecture"
    if any(key in stem for key in ("api", "endpoint")):
        return "api"
    if any(key in stem for key in ("workflow", "process", "flow")):
        return "workflows"
    return "misc"


def ensure_executable(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"PlantUML executable not found at {path}")
    if not path.is_file():
        raise RuntimeError(f"PlantUML path {path} is not a file")
    if not path.stat().st_mode & 0o111:
        raise PermissionError(
            f"PlantUML executable at {path} is not marked executable"
        )


def render_diagram(
    binary: Path, source: Path, output_dir: Path, fmt: str
) -> list[Path]:
    """Render a single PlantUML source into the provided directory and return paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cmd = [
            str(binary),
            f"-t{fmt}",
            str(source),
            "-o",
            str(tmp_path),
        ]
        subprocess.run(cmd, check=True)
        produced = sorted(tmp_path.glob(f"*.{fmt}"))
        if not produced:
            raise RuntimeError(f"No {fmt} output generated for {source}")
        moved = []
        for idx, artifact in enumerate(produced, start=1):
            suffix = f"-{idx}" if len(produced) > 1 else ""
            target_file = output_dir / f"{source.stem}{suffix}.{fmt}"
            shutil.move(str(artifact), target_file)
            moved.append(target_file)
        return moved


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    paths = Paths(repo_root=repo_root)

    ensure_executable(paths.plantuml_bin)

    if not paths.source_root.exists():
        raise FileNotFoundError(f"PlantUML source directory missing: {paths.source_root}")

    # Recreate the diagram output directory for a clean build
    if paths.diagram_root.exists():
        shutil.rmtree(paths.diagram_root)
    paths.diagram_root.mkdir(parents=True, exist_ok=True)

    categories = ["architecture", "database", "workflows", "components", "api", "misc"]
    for cat in categories:
        (paths.diagram_root / cat).mkdir(parents=True, exist_ok=True)

    sources = sorted(paths.source_root.rglob("*.puml"))
    if not sources:
        print("No PlantUML sources found.", file=sys.stderr)
        sys.exit(1)

    rendered = 0
    failures: list[Path] = []
    for puml in sources:
        category = categorize(puml)
        target_dir = paths.diagram_root / category
        target_dir.mkdir(parents=True, exist_ok=True)

        try:
            render_diagram(paths.plantuml_bin, puml, target_dir, "png")
            render_diagram(paths.plantuml_bin, puml, target_dir, "svg")
            rendered += 1
        except subprocess.CalledProcessError as exc:
            print(f"[warn] Failed to render {puml}: {exc}", file=sys.stderr)
            failures.append(puml)
        except RuntimeError as exc:
            print(f"[warn] {exc}", file=sys.stderr)
            failures.append(puml)

    print(f"Rendered {rendered} PlantUML diagrams into {paths.diagram_root}")
    if failures:
        print(f"{len(failures)} diagrams reported errors and need manual review.")


if __name__ == "__main__":
    main()
