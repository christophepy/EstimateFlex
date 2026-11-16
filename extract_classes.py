#!/usr/bin/env python3

"""
Python Architecture Analyzer

Analyse récursivement un projet Python et génère :

    architecture_report.md

avec :

- modules
- imports
- relations module -> module
- classes
- héritage
- composition
- dépendances
- dataclasses
- Enums
- ABC / interfaces
- méthodes
- fonctions hors classe
- attributs
- diagrammes Mermaid
"""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

SRC_DIR = Path("src")
OUTPUT_FILE = Path("architecture_report.md")


# ============================================================
# UTILITAIRES
# ============================================================


def unparse(node):
    """Convertit un nœud AST en code Python."""
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return None


def dotted_name(node):
    """
    Retourne le nom complet d'un Name / Attribute.

    Exemple :

        foo.bar.Baz -> foo.bar.Baz
    """

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):

        parent = dotted_name(node.value)

        if parent:
            return f"{parent}.{node.attr}"

        return node.attr

    return None


def annotation_name(node):
    """
    Extrait le nom principal d'une annotation.

    Foo              -> Foo
    module.Foo       -> Foo
    list[Foo]        -> Foo
    Optional[Foo]    -> Foo
    """

    if node is None:
        return None

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    if isinstance(node, ast.Subscript):
        return annotation_name(node.slice)

    if isinstance(node, ast.Tuple):

        for element in node.elts:

            result = annotation_name(element)

            if result:
                return result

    return None


def is_decorator(node, name):
    """Vérifie si un nœud possède un décorateur donné."""

    for decorator in node.decorator_list:

        value = dotted_name(decorator)

        if value == name:
            return True

    return False


def is_abstract_class(node):
    """
    Détecte les classes ressemblant à des interfaces / ABC.

    Détecte notamment :

        class Foo(ABC)
        class Foo(ABC, ...)
        @abstractmethod
        @abstractclassmethod
        @abstractstaticmethod
    """

    for base in node.bases:

        name = dotted_name(base)

        if name in {
            "ABC",
            "abc.ABC",
        }:
            return True

    for item in node.body:

        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):

            for decorator in item.decorator_list:

                name = dotted_name(decorator)

                if name in {
                    "abstractmethod",
                    "abc.abstractmethod",
                    "abstractclassmethod",
                    "abstractstaticmethod",
                }:
                    return True

    return False


def is_enum_class(node):
    """Détecte les classes héritant de Enum."""

    for base in node.bases:

        name = dotted_name(base)

        if name in {
            "Enum",
            "IntEnum",
            "StrEnum",
            "enum.Enum",
            "enum.IntEnum",
            "enum.StrEnum",
        }:
            return True

    return False


def is_dataclass(node):
    """Détecte @dataclass."""

    return is_decorator(node, "dataclass") or is_decorator(
        node, "dataclasses.dataclass"
    )


# ============================================================
# PARAMÈTRES
# ============================================================


def get_parameters(func):

    args = func.args

    parameters = []

    all_args = args.posonlyargs + args.args

    for arg in all_args:

        annotation = unparse(arg.annotation)

        if annotation:

            parameters.append(f"{arg.arg}: {annotation}")

        else:

            parameters.append(arg.arg)

    if args.vararg:

        parameters.append(f"*{args.vararg.arg}")

    for arg in args.kwonlyargs:

        annotation = unparse(arg.annotation)

        if annotation:

            parameters.append(f"{arg.arg}: {annotation}")

        else:

            parameters.append(arg.arg)

    if args.kwarg:

        parameters.append(f"**{args.kwarg.arg}")

    return parameters


# ============================================================
# ATTRIBUTS D'INSTANCE
# ============================================================


def extract_instance_attributes(func):

    attributes = {}

    for node in ast.walk(func):

        # self.foo = ...
        if isinstance(node, ast.Assign):

            targets = node.targets

        # self.foo: Type = ...
        elif isinstance(node, ast.AnnAssign):

            targets = [node.target]

        else:

            continue

        for target in targets:

            if not (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                continue

            name = target.attr

            annotation = None

            if isinstance(node, ast.AnnAssign):

                annotation = unparse(node.annotation)

            # self.foo = Foo(...)
            if isinstance(node, ast.Assign):

                value = node.value

                if isinstance(value, ast.Call):

                    called = dotted_name(value.func)

                    if called:
                        annotation = called

            attributes[name] = annotation

    return attributes


# ============================================================
# DÉPENDANCES D'UNE MÉTHODE
# ============================================================


def extract_method_dependencies(func):

    dependencies = set()

    # Paramètres
    for arg in func.args.posonlyargs + func.args.args + func.args.kwonlyargs:

        name = annotation_name(arg.annotation)

        if name:
            dependencies.add(name)

    # Retour
    return_type = annotation_name(func.returns)

    if return_type:
        dependencies.add(return_type)

    # Appels
    for node in ast.walk(func):

        if isinstance(node, ast.Call):

            called = dotted_name(node.func)

            if called:

                dependencies.add(called.split(".")[-1])

    return dependencies


# ============================================================
# MÉTHODE
# ============================================================


def extract_method(node):

    return {
        "name": node.name,
        "line": node.lineno,
        "async": isinstance(node, ast.AsyncFunctionDef),
        "parameters": get_parameters(node),
        "return": unparse(node.returns),
        "decorators": [dotted_name(d) for d in node.decorator_list if dotted_name(d)],
        "abstract": any(
            dotted_name(d)
            in {
                "abstractmethod",
                "abc.abstractmethod",
                "abstractclassmethod",
                "abstractstaticmethod",
            }
            for d in node.decorator_list
        ),
    }


# ============================================================
# CLASSE
# ============================================================


def extract_class(node):

    cls = {
        "name": node.name,
        "line": node.lineno,
        "bases": [],
        "dataclass": is_dataclass(node),
        "enum": is_enum_class(node),
        "abstract": is_abstract_class(node),
        "class_attributes": {},
        "instance_attributes": {},
        "methods": [],
        "dependencies": set(),
        "enum_values": [],
    }

    # --------------------------------------------------------
    # Héritage
    # --------------------------------------------------------

    for base in node.bases:

        name = dotted_name(base)

        if name:

            cls["bases"].append(name.split(".")[-1])

    # --------------------------------------------------------
    # Contenu
    # --------------------------------------------------------

    for item in node.body:

        # ----------------------------------------------------
        # Attribut annoté
        # ----------------------------------------------------

        if isinstance(item, ast.AnnAssign):

            if isinstance(item.target, ast.Name):

                name = item.target.id

                annotation = unparse(item.annotation)

                cls["class_attributes"][name] = annotation

                # Enum
                if cls["enum"]:

                    cls["enum_values"].append(name)

        # ----------------------------------------------------
        # Assign
        # ----------------------------------------------------

        elif isinstance(item, ast.Assign):

            for target in item.targets:

                if isinstance(target, ast.Name):

                    name = target.id

                    cls["class_attributes"][name] = None

                    if cls["enum"]:

                        cls["enum_values"].append(name)

        # ----------------------------------------------------
        # Méthode
        # ----------------------------------------------------

        elif isinstance(
            item,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            method = extract_method(item)

            cls["methods"].append(method)

            # Attributs self.xxx
            instance_attrs = extract_instance_attributes(item)

            for name, annotation in instance_attrs.items():

                cls["instance_attributes"][name] = annotation

            # Dépendances
            cls["dependencies"].update(extract_method_dependencies(item))

    # --------------------------------------------------------
    # Dépendances des attributs
    # --------------------------------------------------------

    for annotation in cls["class_attributes"].values():

        dependency = (
            annotation_name(ast.parse(annotation).body[0].value) if annotation else None
        )

        if dependency:

            cls["dependencies"].add(dependency)

    for annotation in cls["instance_attributes"].values():

        if not annotation:
            continue

        try:

            tree = ast.parse(annotation, mode="eval")

            dependency = annotation_name(tree.body)

        except SyntaxError:

            dependency = annotation.split(".")[-1]

        if dependency:

            cls["dependencies"].add(dependency)

    return cls


# ============================================================
# IMPORTS
# ============================================================


def extract_imports(tree):

    imports = []

    for node in ast.walk(tree):

        # import foo
        if isinstance(node, ast.Import):

            for alias in node.names:

                imports.append(
                    {
                        "module": alias.name,
                        "name": alias.asname,
                        "type": "import",
                    }
                )

        # from foo import Bar
        elif isinstance(node, ast.ImportFrom):

            module = node.module or ""

            if node.level:

                prefix = "." * node.level

                module = prefix + module

            for alias in node.names:

                imports.append(
                    {
                        "module": module,
                        "name": alias.name,
                        "as": alias.asname,
                        "type": "from",
                    }
                )

    return imports


# ============================================================
# FONCTIONS HORS CLASSE
# ============================================================


def extract_functions(tree):

    functions = []

    for node in tree.body:

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):

            functions.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "async": isinstance(node, ast.AsyncFunctionDef),
                    "parameters": get_parameters(node),
                    "return": unparse(node.returns),
                    "decorators": [
                        dotted_name(d) for d in node.decorator_list if dotted_name(d)
                    ],
                }
            )

    return functions


# ============================================================
# MODULE
# ============================================================


def analyze_file(file_path):

    try:

        source = file_path.read_text(encoding="utf-8")

        tree = ast.parse(source)

    except (
        SyntaxError,
        UnicodeDecodeError,
    ) as exc:

        print(f"[WARN] {file_path}: {exc}")

        return None

    classes = []

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            classes.append(extract_class(node))

    functions = extract_functions(tree)

    imports = extract_imports(tree)

    return {
        "imports": imports,
        "classes": classes,
        "functions": functions,
    }


# ============================================================
# PROJET
# ============================================================


def analyze_project():

    project = {
        "modules": {},
        "classes": {},
        "functions": {},
        "module_relations": [],
        "class_relations": [],
    }

    files = sorted(SRC_DIR.rglob("*.py"))

    # --------------------------------------------------------
    # Première passe : modules
    # --------------------------------------------------------

    for file_path in files:

        relative = file_path.relative_to(SRC_DIR)

        module_name = str(relative).replace("\\", ".").replace("/", ".")

        if module_name.endswith(".py"):

            module_name = module_name[:-3]

        if module_name.endswith(".__init__"):

            module_name = module_name[:-9]

        data = analyze_file(file_path)

        if data is None:
            continue

        project["modules"][module_name] = {
            "file": str(relative),
            **data,
        }

    # --------------------------------------------------------
    # Index classes
    # --------------------------------------------------------

    for module_name, module in project["modules"].items():

        for cls in module["classes"]:

            project["classes"][cls["name"]] = {
                **cls,
                "module": module_name,
            }

        for function in module["functions"]:

            project["functions"][f"{module_name}.{function['name']}"] = function

    class_names = set(project["classes"].keys())

    module_names = set(project["modules"].keys())

    # ========================================================
    # Relations modules
    # ========================================================

    for module_name, module in project["modules"].items():

        for imp in module["imports"]:

            imported = imp["module"]

            # Retirer le "." des imports relatifs
            clean_import = imported.lstrip(".")

            target = None

            # Correspondance exacte
            if clean_import in module_names:

                target = clean_import

            else:

                # Recherche d'un sous-module
                candidates = [
                    m for m in module_names if m.startswith(clean_import + ".")
                ]

                if candidates:

                    target = sorted(candidates)[0]

            if target and target != module_name:

                project["module_relations"].append(
                    {
                        "from": module_name,
                        "to": target,
                        "type": "import",
                    }
                )

    # ========================================================
    # Relations classes
    # ========================================================

    for class_name, cls in project["classes"].items():

        # ----------------------------------------------------
        # Héritage
        # ----------------------------------------------------

        for base in cls["bases"]:

            if base in class_names:

                project["class_relations"].append(
                    {
                        "from": base,
                        "to": class_name,
                        "type": "inheritance",
                    }
                )

        # ----------------------------------------------------
        # Composition
        # ----------------------------------------------------

        for annotation in cls["instance_attributes"].values():

            if not annotation:
                continue

            try:

                tree = ast.parse(annotation, mode="eval")

                target = annotation_name(tree.body)

            except SyntaxError:

                target = annotation.split(".")[-1]

            if target in class_names:

                project["class_relations"].append(
                    {
                        "from": class_name,
                        "to": target,
                        "type": "composition",
                    }
                )

        # ----------------------------------------------------
        # Dépendances
        # ----------------------------------------------------

        for dependency in cls["dependencies"]:

            dependency = dependency.split(".")[-1]

            if dependency not in class_names:
                continue

            if dependency == class_name:
                continue

            already_exists = any(
                r["from"] == class_name and r["to"] == dependency
                for r in project["class_relations"]
            )

            if not already_exists:

                project["class_relations"].append(
                    {
                        "from": class_name,
                        "to": dependency,
                        "type": "dependency",
                    }
                )

    # ========================================================
    # Suppression doublons
    # ========================================================

    def unique_relations(relations):

        seen = set()
        result = []

        for relation in relations:

            key = (
                relation["from"],
                relation["to"],
                relation["type"],
            )

            if key not in seen:

                seen.add(key)

                result.append(relation)

        return result

    project["module_relations"] = unique_relations(project["module_relations"])

    project["class_relations"] = unique_relations(project["class_relations"])

    return project


# ============================================================
# MERMAID : MODULES
# ============================================================


def generate_module_mermaid(project):

    lines = [
        "```mermaid",
        "flowchart LR",
        "",
    ]

    for module_name in sorted(project["modules"]):

        safe = module_name.replace(".", "_").replace("-", "_")

        label = module_name.replace('"', "'")

        lines.append(f'    {safe}["{label}"]')

    lines.append("")

    for relation in project["module_relations"]:

        source = relation["from"].replace(".", "_").replace("-", "_")

        target = relation["to"].replace(".", "_").replace("-", "_")

        lines.append(f"    {source} --> {target}")

    lines.append("")
    lines.append("```")

    return "\n".join(lines)


# ============================================================
# MERMAID : CLASSES
# ============================================================


def generate_class_mermaid(project):

    lines = [
        "```mermaid",
        "classDiagram",
        "",
    ]

    # --------------------------------------------------------
    # Classes
    # --------------------------------------------------------

    for class_name in sorted(project["classes"]):

        cls = project["classes"][class_name]

        # Mermaid n'aime pas certains caractères
        safe_name = class_name.replace("-", "_")

        lines.append(f"    class {safe_name} {{")

        # Stéréotypes
        if cls["dataclass"]:

            lines.append("        <<dataclass>>")

        if cls["enum"]:

            lines.append("        <<enumeration>>")

        elif cls["abstract"]:

            lines.append("        <<abstract>>")

        # Attributs
        for name, annotation in cls["class_attributes"].items():

            if annotation:

                lines.append(f"        +{name}: " f"{annotation}")

            else:

                lines.append(f"        +{name}")

        for name, annotation in cls["instance_attributes"].items():

            if annotation:

                lines.append(f"        +{name}: " f"{annotation}")

            else:

                lines.append(f"        +{name}")

        # Méthodes
        for method in cls["methods"]:

            params = ", ".join(method["parameters"])

            prefix = ""

            if method["abstract"]:
                prefix = "*"

            async_prefix = "async " if method["async"] else ""

            signature = f"+{prefix}" f"{async_prefix}" f"{method['name']}" f"({params})"

            if method["return"]:

                signature += f" {method['return']}"

            lines.append(f"        {signature}")

        lines.append("    }")

        lines.append("")

    # --------------------------------------------------------
    # Relations
    # --------------------------------------------------------

    for relation in project["class_relations"]:

        source = relation["from"].replace("-", "_")

        target = relation["to"].replace("-", "_")

        if relation["type"] == "inheritance":

            lines.append(f"    {source} <|-- {target}")

        elif relation["type"] == "composition":

            lines.append(f"    {source} *-- {target}")

        elif relation["type"] == "dependency":

            lines.append(f"    {source} ..> {target}")

    lines.append("")
    lines.append("```")

    return "\n".join(lines)


# ============================================================
# RAPPORT
# ============================================================


def generate_report(project):

    report = []

    modules = project["modules"]

    classes = project["classes"]

    functions = project["functions"]

    # ========================================================
    # INTRODUCTION
    # ========================================================

    report.append("# Architecture Report")

    report.append("")

    report.append(f"Projet analysé : `{SRC_DIR}`")

    report.append("")

    report.append(f"- Modules : **{len(modules)}**")

    report.append(f"- Classes : **{len(classes)}**")

    report.append(f"- Fonctions hors classe : " f"**{len(functions)}**")

    report.append(f"- Relations modules : " f"**{len(project['module_relations'])}**")

    report.append(f"- Relations classes : " f"**{len(project['class_relations'])}**")

    report.append("")

    # ========================================================
    # ARCHITECTURE MODULES
    # ========================================================

    report.append("## Architecture des modules")

    report.append("")

    report.append(generate_module_mermaid(project))

    report.append("")

    # ========================================================
    # ARCHITECTURE CLASSES
    # ========================================================

    report.append("## Architecture des classes")

    report.append("")

    report.append(generate_class_mermaid(project))

    report.append("")

    # ========================================================
    # MODULES
    # ========================================================

    report.append("## Modules")

    report.append("")

    for module_name in sorted(modules):

        module = modules[module_name]

        report.append(f"### `{module_name}`")

        report.append("")

        report.append(f"Fichier : `{module['file']}`")

        report.append("")

        # Imports
        if module["imports"]:

            report.append("**Imports :**")

            report.append("")

            for imp in module["imports"]:

                if imp["type"] == "import":

                    text = f"`import " f"{imp['module']}`"

                else:

                    text = f"`from " f"{imp['module']} " f"import " f"{imp['name']}`"

                report.append(f"- {text}")

            report.append("")

        # Classes
        if module["classes"]:

            report.append("**Classes :**")

            report.append("")

            for cls in module["classes"]:

                markers = []

                if cls["dataclass"]:
                    markers.append("dataclass")

                if cls["enum"]:
                    markers.append("Enum")

                if cls["abstract"]:
                    markers.append("ABC")

                suffix = ""

                if markers:

                    suffix = " — " + ", ".join(markers)

                report.append(f"- `{cls['name']}`" f"{suffix}")

            report.append("")

        # Fonctions
        if module["functions"]:

            report.append("**Fonctions :**")

            report.append("")

            for function in module["functions"]:

                params = ", ".join(function["parameters"])

                report.append(f"- " f"`{function['name']}" f"({params})`")

            report.append("")

    # ========================================================
    # CLASSES DÉTAILLÉES
    # ========================================================

    report.append("## Classes détaillées")

    report.append("")

    for class_name in sorted(classes):

        cls = classes[class_name]

        report.append(f"### `{class_name}`")

        report.append("")

        report.append(f"Module : `{cls['module']}`")

        report.append("")

        # Type
        types = []

        if cls["dataclass"]:
            types.append("dataclass")

        if cls["enum"]:
            types.append("Enum")

        if cls["abstract"]:
            types.append("ABC / interface")

        if types:

            report.append("**Type :** " + ", ".join(types))

            report.append("")

        # Héritage
        if cls["bases"]:

            report.append(
                "**Hérite de :** " + ", ".join(f"`{x}`" for x in cls["bases"])
            )

            report.append("")

        # Enum
        if cls["enum_values"]:

            report.append("**Valeurs Enum :**")

            report.append("")

            for value in cls["enum_values"]:

                report.append(f"- `{value}`")

            report.append("")

        # Attributs
        if cls["class_attributes"] or cls["instance_attributes"]:

            report.append("**Attributs :**")

            report.append("")

            for name, annotation in cls["class_attributes"].items():

                if annotation:

                    report.append(f"- `{name}: " f"{annotation}` " "(classe)")

                else:

                    report.append(f"- `{name}` " "(classe)")

            for name, annotation in cls["instance_attributes"].items():

                if annotation:

                    report.append(f"- `self.{name}: " f"{annotation}`")

                else:

                    report.append(f"- `self.{name}`")

            report.append("")

        # Méthodes
        if cls["methods"]:

            report.append("**Méthodes :**")

            report.append("")

            for method in cls["methods"]:

                prefix = ""

                if method["abstract"]:
                    prefix = "abstract "

                if method["async"]:
                    prefix += "async "

                params = ", ".join(method["parameters"])

                signature = f"{prefix}" f"{method['name']}" f"({params})"

                if method["return"]:

                    signature += f" -> " f"{method['return']}"

                report.append(f"- `{signature}` " f"(ligne " f"{method['line']})")

            report.append("")

    # ========================================================
    # RELATIONS
    # ========================================================

    report.append("## Relations entre classes")

    report.append("")

    for relation in project["class_relations"]:

        source = relation["from"]
        target = relation["to"]

        if relation["type"] == "inheritance":

            symbol = "hérite de"

        elif relation["type"] == "composition":

            symbol = "compose / possède"

        else:

            symbol = "dépend de"

        report.append(f"- `{source}` " f"**{symbol}** " f"`{target}`")

    report.append("")

    # ========================================================
    # RELATIONS MODULES
    # ========================================================

    report.append("## Relations entre modules")

    report.append("")

    for relation in project["module_relations"]:

        report.append(f"- `{relation['from']}` " f"→ `{relation['to']}`")

    report.append("")

    # ========================================================
    # INDICATEURS
    # ========================================================

    report.append("## Indicateurs d'architecture")

    report.append("")

    dataclasses = [cls for cls in classes.values() if cls["dataclass"]]

    enums = [cls for cls in classes.values() if cls["enum"]]

    abstracts = [cls for cls in classes.values() if cls["abstract"]]

    report.append(f"- Dataclasses : **{len(dataclasses)}**")

    report.append(f"- Enums : **{len(enums)}**")

    report.append(f"- Interfaces / ABC : " f"**{len(abstracts)}**")

    # Modules très dépendants
    module_dependency_count = defaultdict(int)

    for relation in project["module_relations"]:

        module_dependency_count[relation["from"]] += 1

    if module_dependency_count:

        most_dependent = sorted(
            module_dependency_count.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        report.append("")

        report.append("### Modules avec le plus de dépendances")

        report.append("")

        for module, count in most_dependent:

            report.append(f"- `{module}` : " f"**{count}** dépendances")

    report.append("")

    # ========================================================
    # ÉCRITURE
    # ========================================================

    OUTPUT_FILE.write_text("\n".join(report), encoding="utf-8")


# ============================================================
# MAIN
# ============================================================


def main():

    print()
    print("=" * 60)
    print(" Python Architecture Analyzer")
    print("=" * 60)
    print()

    print(f"Analyse de : {SRC_DIR}")

    project = analyze_project()

    generate_report(project)

    print()
    print(f"Modules       : " f"{len(project['modules'])}")

    print(f"Classes       : " f"{len(project['classes'])}")

    print(f"Fonctions     : " f"{len(project['functions'])}")

    print(f"Relations mod.: " f"{len(project['module_relations'])}")

    print(f"Relations cls.: " f"{len(project['class_relations'])}")

    print()
    print(f"Rapport généré : " f"{OUTPUT_FILE}")

    print()


if __name__ == "__main__":
    main()
