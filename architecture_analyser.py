from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path

# ============================================================
# Configuration
# ============================================================

SRC_DIR = Path("src")
OUTPUT_DIR = Path("architecture")

REPORT_FILE = OUTPUT_DIR / "architecture_report.md"
JSON_FILE = OUTPUT_DIR / "architecture.json"

DIAGRAM_DIR = OUTPUT_DIR / "diagrams"
MODULE_MMD = DIAGRAM_DIR / "modules.mmd"
MODULE_SVG = DIAGRAM_DIR / "modules.svg"
CLASS_MMD = DIAGRAM_DIR / "classes.mmd"
CLASS_SVG = DIAGRAM_DIR / "classes.svg"


# ============================================================
# Data structures
# ============================================================


@dataclass
class FunctionInfo:
    name: str
    args: list[str] = field(default_factory=list)
    returns: str | None = None
    decorators: list[str] = field(default_factory=list)


@dataclass
class AttributeInfo:
    name: str
    annotation: str | None = None
    value_type: str | None = None


@dataclass
class MethodInfo:
    name: str
    args: list[str] = field(default_factory=list)
    returns: str | None = None
    decorators: list[str] = field(default_factory=list)
    is_async: bool = False


@dataclass
class ClassInfo:
    name: str
    bases: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)

    is_dataclass: bool = False
    is_enum: bool = False
    is_abc: bool = False

    class_attributes: list[AttributeInfo] = field(default_factory=list)
    instance_attributes: list[AttributeInfo] = field(default_factory=list)
    methods: list[MethodInfo] = field(default_factory=list)

    dependencies: list[str] = field(default_factory=list)


@dataclass
class ModuleInfo:
    name: str
    file: str

    imports: list[str] = field(default_factory=list)
    from_imports: list[str] = field(default_factory=list)

    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)

    dependencies: list[str] = field(default_factory=list)


# ============================================================
# AST helpers
# ============================================================


def annotation_to_string(node: ast.AST | None) -> str | None:
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return None


def expression_to_string(node: ast.AST | None) -> str | None:
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return None


def decorator_name(node: ast.AST) -> str:
    return expression_to_string(node) or ""


def get_decorators(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
) -> list[str]:
    return [decorator_name(d) for d in node.decorator_list if decorator_name(d)]


def get_function_args(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    args = []

    positional = node.args.posonlyargs + node.args.args

    for arg in positional:
        annotation = annotation_to_string(arg.annotation)

        if annotation:
            args.append(f"{arg.arg}: {annotation}")
        else:
            args.append(arg.arg)

    if node.args.vararg:
        args.append(f"*{node.args.vararg.arg}")

    for arg in node.args.kwonlyargs:
        annotation = annotation_to_string(arg.annotation)

        if annotation:
            args.append(f"{arg.arg}: {annotation}")
        else:
            args.append(arg.arg)

    if node.args.kwarg:
        args.append(f"**{node.args.kwarg.arg}")

    return args


def called_names(node: ast.AST) -> set[str]:
    result = set()

    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func

            if isinstance(func, ast.Name):
                result.add(func.id)

            elif isinstance(func, ast.Attribute):
                result.add(func.attr)

    return result


def assigned_self_attributes(node: ast.AST) -> list[AttributeInfo]:
    result = {}

    for child in ast.walk(node):
        if isinstance(child, ast.Assign):
            targets = child.targets

        elif isinstance(child, ast.AnnAssign):
            targets = [child.target]

        else:
            continue

        for target in targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                annotation = None
                value_type = None

                if isinstance(child, ast.AnnAssign):
                    annotation = annotation_to_string(child.annotation)

                if isinstance(child, ast.Assign):
                    value_type = expression_to_string(child.value)

                result[target.attr] = AttributeInfo(
                    name=target.attr,
                    annotation=annotation,
                    value_type=value_type,
                )

    return list(result.values())


def class_attributes(node: ast.ClassDef) -> list[AttributeInfo]:
    result = []

    for item in node.body:
        if isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                result.append(
                    AttributeInfo(
                        name=item.target.id,
                        annotation=annotation_to_string(item.annotation),
                        value_type=expression_to_string(item.value),
                    )
                )

        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    result.append(
                        AttributeInfo(
                            name=target.id,
                            value_type=expression_to_string(item.value),
                        )
                    )

    return result


# ============================================================
# Class analysis
# ============================================================


def analyze_class(node: ast.ClassDef) -> ClassInfo:
    bases = [
        expression_to_string(base) for base in node.bases if expression_to_string(base)
    ]

    decorators = get_decorators(node)

    decorator_lower = {d.lower() for d in decorators}
    base_lower = {b.lower() for b in bases}

    is_dataclass = any("dataclass" in d for d in decorator_lower)

    is_enum = any("enum" in base or base.endswith("Enum") for base in base_lower)

    is_abc = any(
        "abc" in base or "abstract" in base or "abc" in d or "abstractmethod" in d
        for base in base_lower
        for d in decorator_lower
    )

    methods = []
    instance_attrs = []

    dependencies = set()

    for item in node.body:

        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.append(
                MethodInfo(
                    name=item.name,
                    args=get_function_args(item),
                    returns=annotation_to_string(item.returns),
                    decorators=get_decorators(item),
                    is_async=isinstance(item, ast.AsyncFunctionDef),
                )
            )

            instance_attrs.extend(assigned_self_attributes(item))

            dependencies.update(called_names(item))

            for arg in item.args.args:
                annotation = annotation_to_string(arg.annotation)
                if annotation:
                    dependencies.add(annotation)

            return_annotation = annotation_to_string(item.returns)

            if return_annotation:
                dependencies.add(return_annotation)

    unique_attrs = {}

    for attr in instance_attrs:
        unique_attrs[attr.name] = attr

    return ClassInfo(
        name=node.name,
        bases=bases,
        decorators=decorators,
        is_dataclass=is_dataclass,
        is_enum=is_enum,
        is_abc=is_abc,
        class_attributes=class_attributes(node),
        instance_attributes=list(unique_attrs.values()),
        methods=methods,
        dependencies=sorted(dependencies),
    )


# ============================================================
# Module analysis
# ============================================================


def analyze_module(
    path: Path,
    src_dir: Path,
) -> ModuleInfo:

    relative = path.relative_to(src_dir).with_suffix("")

    parts = list(relative.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    module_name = ".".join(parts)

    source = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        print(f"[WARN] Impossible d'analyser {path}: {exc}")
        return ModuleInfo(
            name=module_name,
            file=str(path),
        )

    imports = set()
    from_imports = set()

    classes = []
    functions = []

    for node in tree.body:

        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = "." * node.level + (node.module or "")

            for alias in node.names:
                from_imports.add(f"{module}:{alias.name}")

        elif isinstance(node, ast.ClassDef):
            classes.append(analyze_class(node))

        elif isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            functions.append(
                FunctionInfo(
                    name=node.name,
                    args=get_function_args(node),
                    returns=annotation_to_string(node.returns),
                    decorators=get_decorators(node),
                )
            )

    return ModuleInfo(
        name=module_name,
        file=str(path),
        imports=sorted(imports),
        from_imports=sorted(from_imports),
        classes=classes,
        functions=functions,
    )


# ============================================================
# Module resolution
# ============================================================


def build_module_index(
    modules: list[ModuleInfo],
) -> dict[str, str]:

    index = {}

    for module in modules:
        index[module.name] = module.name

    return index


def normalize_relative_import(
    current_module: str,
    import_name: str,
) -> str:

    if not import_name.startswith("."):
        return import_name

    dots = len(import_name) - len(import_name.lstrip("."))

    remainder = import_name[dots:]

    current_parts = current_module.split(".")

    # One leading dot = current package
    base = current_parts[: max(0, len(current_parts) - dots + 1)]

    if remainder:
        base.extend(remainder.split("."))

    return ".".join(p for p in base if p)


def resolve_module_dependency(
    current_module: str,
    imported: str,
    known_modules: set[str],
) -> str | None:

    resolved = normalize_relative_import(
        current_module,
        imported,
    )

    if resolved in known_modules:
        return resolved

    # Try parent module
    parts = resolved.split(".")

    for i in range(len(parts), 0, -1):
        candidate = ".".join(parts[:i])

        if candidate in known_modules:
            return candidate

    # Absolute import may point to a child module
    for module in known_modules:
        if module.startswith(resolved + "."):
            return resolved

    return None


def resolve_dependencies(
    modules: list[ModuleInfo],
) -> None:

    known = {m.name for m in modules}

    for module in modules:
        dependencies = set()

        for imported in module.imports:
            resolved = resolve_module_dependency(
                module.name,
                imported,
                known,
            )

            if resolved and resolved != module.name:
                dependencies.add(resolved)

        for imported in module.from_imports:
            resolved = resolve_module_dependency(
                module.name,
                imported,
                known,
            )

            if resolved and resolved != module.name:
                dependencies.add(resolved)

        module.dependencies = sorted(dependencies)


# ============================================================
# Class relationships
# ============================================================


def build_class_index(
    modules: list[ModuleInfo],
) -> dict[str, tuple[str, ClassInfo]]:

    index = {}

    for module in modules:
        for cls in module.classes:
            index[cls.name] = (module.name, cls)

    return index


def resolve_class_name(
    name: str,
    class_index: dict[str, tuple[str, ClassInfo]],
) -> str | None:

    clean = name

    # Remove generic parameters
    clean = re.sub(r"\[.*\]", "", clean)

    # Handle Optional / list etc.
    clean = clean.replace("typing.", "")

    if clean in class_index:
        return clean

    short = clean.split(".")[-1]

    if short in class_index:
        return short

    return None


def build_class_relationships(
    modules: list[ModuleInfo],
):
    class_index = build_class_index(modules)

    inheritance = []
    composition = []
    dependencies = []

    for module in modules:
        for cls in module.classes:

            for base in cls.bases:
                target = resolve_class_name(
                    base,
                    class_index,
                )

                if target and target != cls.name:
                    inheritance.append(
                        (
                            cls.name,
                            target,
                        )
                    )

            for attr in cls.instance_attributes:
                candidates = []

                if attr.annotation:
                    candidates.append(attr.annotation)

                if attr.value_type:
                    candidates.append(attr.value_type)

                for candidate in candidates:
                    target = resolve_class_name(
                        candidate,
                        class_index,
                    )

                    if target and target != cls.name:
                        composition.append(
                            (
                                cls.name,
                                target,
                            )
                        )

            for dependency in cls.dependencies:
                target = resolve_class_name(
                    dependency,
                    class_index,
                )

                if target and target != cls.name:
                    dependencies.append(
                        (
                            cls.name,
                            target,
                        )
                    )

    return {
        "inheritance": sorted(set(inheritance)),
        "composition": sorted(set(composition)),
        "dependencies": sorted(set(dependencies)),
    }


# ============================================================
# Circular dependencies
# ============================================================


def detect_cycles(
    modules: list[ModuleInfo],
) -> list[list[str]]:

    graph = {module.name: module.dependencies for module in modules}

    cycles = []
    visited = set()
    stack = []

    def visit(node: str):
        if node in stack:
            index = stack.index(node)
            cycle = stack[index:] + [node]

            normalized = tuple(sorted(cycle))

            if normalized not in {tuple(sorted(c)) for c in cycles}:
                cycles.append(cycle)

            return

        if node in visited:
            return

        visited.add(node)
        stack.append(node)

        for dependency in graph.get(node, []):
            visit(dependency)

        stack.pop()

    for module in graph:
        visit(module)

    return cycles


# ============================================================
# Mermaid
# ============================================================


def mermaid_id(name: str) -> str:
    return re.sub(
        r"[^a-zA-Z0-9_]",
        "_",
        name,
    )


def generate_modules_mermaid(
    modules: list[ModuleInfo],
) -> str:

    lines = [
        "flowchart LR",
    ]

    for module in modules:
        module_id = mermaid_id(module.name)

        label = module.name.replace('"', "'")

        lines.append(f'    {module_id}["{label}"]')

    lines.append("")

    seen = set()

    for module in modules:
        source = mermaid_id(module.name)

        for dependency in module.dependencies:
            target = mermaid_id(dependency)

            relation = (
                source,
                target,
            )

            if relation in seen:
                continue

            seen.add(relation)

            lines.append(f"    {source} --> {target}")

    return "\n".join(lines) + "\n"


def generate_classes_mermaid(
    modules: list[ModuleInfo],
) -> str:

    relations = build_class_relationships(modules)

    lines = [
        "classDiagram",
    ]

    all_classes = []

    for module in modules:
        for cls in module.classes:
            all_classes.append((module.name, cls))

    for module_name, cls in all_classes:

        class_name = mermaid_id(cls.name)

        lines.append(f"    class {class_name} {{")

        for attr in cls.class_attributes:
            attr_type = attr.annotation or "Any"

            lines.append(f"        +{attr_type} {attr.name}")

        for attr in cls.instance_attributes:
            attr_type = attr.annotation or "Any"

            lines.append(f"        +{attr_type} {attr.name}")

        for method in cls.methods:
            args = ", ".join(arg.split(":")[0] for arg in method.args if arg != "self")

            returns = method.returns or "None"

            prefix = "+"

            if method.is_async:
                prefix = "+"

            lines.append(f"        {prefix}{method.name}({args}) {returns}")

        lines.append("    }")

    lines.append("")

    seen = set()

    for child, parent in relations["inheritance"]:

        relation = (
            mermaid_id(parent),
            mermaid_id(child),
        )

        if relation not in seen:
            lines.append(f"    {relation[0]} <|-- {relation[1]}")
            seen.add(relation)

    for source, target in relations["composition"]:

        relation = (
            mermaid_id(source),
            mermaid_id(target),
        )

        if relation not in seen:
            lines.append(f"    {relation[0]} *-- {relation[1]}")
            seen.add(relation)

    for source, target in relations["dependencies"]:

        relation = (
            mermaid_id(source),
            mermaid_id(target),
        )

        if relation not in seen:
            lines.append(f"    {relation[0]} ..> {relation[1]}")
            seen.add(relation)

    return "\n".join(lines) + "\n"


# ============================================================
# JSON
# ============================================================


def generate_json(
    modules: list[ModuleInfo],
    cycles: list[list[str]],
) -> dict:

    return {
        "source": str(SRC_DIR),
        "modules": [asdict(module) for module in modules],
        "circular_dependencies": cycles,
        "statistics": {
            "modules": len(modules),
            "classes": sum(len(m.classes) for m in modules),
            "functions": sum(len(m.functions) for m in modules),
            "dataclasses": sum(sum(c.is_dataclass for c in m.classes) for m in modules),
            "enums": sum(sum(c.is_enum for c in m.classes) for m in modules),
            "abc_interfaces": sum(sum(c.is_abc for c in m.classes) for m in modules),
        },
    }


# ============================================================
# Markdown report
# ============================================================


def generate_markdown(
    modules: list[ModuleInfo],
    cycles: list[list[str]],
) -> str:

    class_relations = build_class_relationships(modules)

    total_classes = sum(len(m.classes) for m in modules)

    total_functions = sum(len(m.functions) for m in modules)

    total_dataclasses = sum(sum(c.is_dataclass for c in m.classes) for m in modules)

    total_enums = sum(sum(c.is_enum for c in m.classes) for m in modules)

    total_abc = sum(sum(c.is_abc for c in m.classes) for m in modules)

    lines = [
        "# Architecture Report",
        "",
        f"> Source analysée : `{SRC_DIR}`",
        "",
        "## Vue d'ensemble",
        "",
        f"- Modules : **{len(modules)}**",
        f"- Classes : **{total_classes}**",
        f"- Fonctions top-level : **{total_functions}**",
        f"- Dataclasses : **{total_dataclasses}**",
        f"- Enums : **{total_enums}**",
        f"- ABC / interfaces : **{total_abc}**",
        f"- Dépendances circulaires : **{len(cycles)}**",
        "",
        "## Architecture des modules",
        "",
        "```mermaid",
        "flowchart LR",
    ]

    module_diagram = generate_modules_mermaid(modules)

    lines.extend(module_diagram.splitlines()[1:])

    lines.extend(
        [
            "```",
            "",
            "## Diagramme des classes",
            "",
            "```mermaid",
            "classDiagram",
        ]
    )

    class_diagram = generate_classes_mermaid(modules)

    lines.extend(class_diagram.splitlines()[1:])

    lines.extend(
        [
            "```",
            "",
            "## Dépendances circulaires",
            "",
        ]
    )

    if cycles:
        for cycle in cycles:
            lines.append("- " + " → ".join(f"`{x}`" for x in cycle))
    else:
        lines.append("Aucune dépendance circulaire détectée.")

    lines.extend(
        [
            "",
            "## Modules",
            "",
        ]
    )

    for module in modules:

        lines.extend(
            [
                f"### `{module.name}`",
                "",
                f"Fichier : `{module.file}`",
                "",
            ]
        )

        if module.dependencies:
            lines.append("**Dépendances internes :**")
            lines.append("")

            for dependency in module.dependencies:
                lines.append(f"- `{dependency}`")

            lines.append("")

        if module.imports:
            lines.append("**Imports :**")
            lines.append("")

            for item in module.imports:
                lines.append(f"- `{item}`")

            lines.append("")

        if module.from_imports:
            lines.append("**From imports :**")
            lines.append("")

            for item in module.from_imports:
                lines.append(f"- `{item}`")

            lines.append("")

        if module.classes:
            lines.append("#### Classes")
            lines.append("")

            for cls in module.classes:

                flags = []

                if cls.is_dataclass:
                    flags.append("dataclass")

                if cls.is_enum:
                    flags.append("Enum")

                if cls.is_abc:
                    flags.append("ABC/interface")

                suffix = f" — {', '.join(flags)}" if flags else ""

                lines.append(f"##### `{cls.name}`{suffix}")

                lines.append("")

                if cls.bases:
                    lines.append(
                        "**Héritage :** " + ", ".join(f"`{base}`" for base in cls.bases)
                    )
                    lines.append("")

                if cls.class_attributes:
                    lines.append("**Attributs de classe :**")
                    lines.append("")

                    for attr in cls.class_attributes:
                        lines.append(
                            f"- `{attr.name}`"
                            + (f": `{attr.annotation}`" if attr.annotation else "")
                        )

                    lines.append("")

                if cls.instance_attributes:
                    lines.append("**Attributs d'instance :**")
                    lines.append("")

                    for attr in cls.instance_attributes:
                        details = []

                        if attr.annotation:
                            details.append(f"type `{attr.annotation}`")

                        if attr.value_type:
                            details.append(f"valeur `{attr.value_type}`")

                        suffix = f" ({', '.join(details)})" if details else ""

                        lines.append(f"- `{attr.name}`{suffix}")

                    lines.append("")

                if cls.methods:
                    lines.append("**Méthodes :**")
                    lines.append("")

                    for method in cls.methods:

                        args = ", ".join(method.args)

                        returns = method.returns or "None"

                        lines.append(f"- `{method.name}({args}) -> {returns}`")

                    lines.append("")

        if module.functions:
            lines.append("#### Fonctions top-level")
            lines.append("")

            for function in module.functions:
                args = ", ".join(function.args)

                returns = function.returns or "None"

                lines.append(f"- `{function.name}({args}) -> {returns}`")

            lines.append("")

    lines.extend(
        [
            "## Relations entre classes",
            "",
            "### Héritage",
            "",
        ]
    )

    if class_relations["inheritance"]:
        for child, parent in class_relations["inheritance"]:
            lines.append(f"- `{child}` hérite de `{parent}`")
    else:
        lines.append("- Aucune.")

    lines.extend(
        [
            "",
            "### Composition",
            "",
        ]
    )

    if class_relations["composition"]:
        for source, target in class_relations["composition"]:
            lines.append(f"- `{source}` contient/utilise `{target}`")
    else:
        lines.append("- Aucune.")

    lines.extend(
        [
            "",
            "### Dépendances",
            "",
        ]
    )

    if class_relations["dependencies"]:
        for source, target in class_relations["dependencies"]:
            lines.append(f"- `{source}` dépend de `{target}`")
    else:
        lines.append("- Aucune.")

    lines.extend(
        [
            "",
            "## Fichiers générés",
            "",
            "- `architecture_report.md` — rapport complet",
            "- `architecture.json` — représentation structurée",
            "- `diagrams/modules.mmd` — diagramme Mermaid des modules",
            "- `diagrams/modules.svg` — diagramme SVG des modules",
            "- `diagrams/classes.mmd` — diagramme Mermaid des classes",
            "- `diagrams/classes.svg` — diagramme SVG des classes",
            "",
        ]
    )

    return "\n".join(lines)


# ============================================================
# Mermaid CLI / SVG
# ============================================================


def find_mmdc() -> str | None:
    return shutil.which("mmdc")


def generate_svg(
    mmd_file: Path,
    svg_file: Path,
) -> bool:

    mmdc = find_mmdc()

    if not mmdc:
        return False

    command = [
        mmdc,
        "-i",
        str(mmd_file),
        "-o",
        str(svg_file),
        "-b",
        "transparent",
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )

        return True

    except subprocess.CalledProcessError as exc:
        print(f"[WARN] Mermaid n'a pas pu générer {svg_file}")

        if exc.stderr:
            print(exc.stderr)

        return False


# ============================================================
# Main
# ============================================================


def main():

    if not SRC_DIR.exists():
        raise SystemExit(f"Erreur : dossier `{SRC_DIR}` introuvable.")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    DIAGRAM_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 60)
    print("Architecture Analyzer")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Scan
    # --------------------------------------------------------

    python_files = sorted(SRC_DIR.rglob("*.py"))

    print(f"[1/6] Analyse de {len(python_files)} fichiers Python...")

    modules = [
        analyze_module(
            path,
            SRC_DIR,
        )
        for path in python_files
    ]

    # --------------------------------------------------------
    # Dependencies
    # --------------------------------------------------------

    print("[2/6] Résolution des dépendances...")

    resolve_dependencies(modules)

    # --------------------------------------------------------
    # Cycles
    # --------------------------------------------------------

    print("[3/6] Détection des dépendances circulaires...")

    cycles = detect_cycles(modules)

    # --------------------------------------------------------
    # Mermaid
    # --------------------------------------------------------

    print("[4/6] Génération des diagrammes Mermaid...")

    modules_mermaid = generate_modules_mermaid(modules)

    classes_mermaid = generate_classes_mermaid(modules)

    MODULE_MMD.write_text(
        modules_mermaid,
        encoding="utf-8",
    )

    CLASS_MMD.write_text(
        classes_mermaid,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # SVG
    # --------------------------------------------------------

    print("[5/6] Génération des SVG...")

    module_svg_ok = generate_svg(
        MODULE_MMD,
        MODULE_SVG,
    )

    class_svg_ok = generate_svg(
        CLASS_MMD,
        CLASS_SVG,
    )

    # --------------------------------------------------------
    # JSON + Markdown
    # --------------------------------------------------------

    print("[6/6] Génération du rapport...")

    data = generate_json(
        modules,
        cycles,
    )

    JSON_FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    report = generate_markdown(
        modules,
        cycles,
    )

    REPORT_FILE.write_text(
        report,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    total_classes = sum(len(m.classes) for m in modules)

    total_functions = sum(len(m.functions) for m in modules)

    print()
    print("=" * 60)
    print("Analyse terminée")
    print("=" * 60)
    print()
    print(f"Modules       : {len(modules)}")
    print(f"Classes       : {total_classes}")
    print(f"Fonctions     : {total_functions}")
    print(f"Cycles        : {len(cycles)}")
    print()
    print(f"Rapport       : {REPORT_FILE}")
    print(f"JSON          : {JSON_FILE}")
    print(f"Modules MMD   : {MODULE_MMD}")
    print(f"Classes MMD   : {CLASS_MMD}")

    if module_svg_ok:
        print(f"Modules SVG   : {MODULE_SVG}")
    else:
        print("Modules SVG   : non généré " "(Mermaid CLI / mmdc absent)")

    if class_svg_ok:
        print(f"Classes SVG   : {CLASS_SVG}")
    else:
        print("Classes SVG   : non généré " "(Mermaid CLI / mmdc absent)")

    print()


if __name__ == "__main__":
    main()
