#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

plugin = {
  "name": "yamldoc",
  "directives": [
    {
      "name": "yaml-doc",
      "function": "yaml_doc",
    }
  ]
}




def declare_result(content):
    """Declare result as JSON to stdout

    :param content: content to declare as the result
    """

    # Format result and write to stdout
    json.dump(content, sys.stdout, indent=2)
    # Successfully exit
    raise SystemExit(0)

def _stringify(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return ", ".join(_stringify(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}={_stringify(val)}" for key, val in value.items())
    return str(value)


def _text(value):
    return {"type": "text", "value": value}


def _heading(depth, text):
    return {"type": "heading", "depth": depth, "children": [_text(text)]}


def _table_cell(value):
    return {"type": "tableCell", "children": [_text(value)]}


def _table_header_cell(value):
    return {
        "type": "tableCell",
        "children": [{"type": "strong", "children": [_text(value)]}],
    }


def _table_row(values):
    return {"type": "tableRow", "children": [_table_cell(value) for value in values]}


def _table(headers, rows):
    return {
        "type": "table",
        "align": [None] * len(headers),
        "children": [
            {"type": "tableRow", "children": [_table_header_cell(value) for value in headers]}
        ]
        + [_table_row(row) for row in rows],
    }


def _resolve_model_name(data):
    options = data.get("options", {}) if isinstance(data, dict) else {}
    if "model" in options and options["model"]:
        return str(options["model"])

    for key in ("args", "arguments"):
        values = data.get(key) if isinstance(data, dict) else None
        if isinstance(values, list) and values:
            return str(values[0])
    return "groundwater"


def _normalize_model_name(value):
    return str(value).strip().lower().replace("-", "").replace("_", "")


def _read_translations():
    locales_file = Path(__file__).resolve().parents[2] / "ui" / "src" / "locales" / "en.json"
    with locales_file.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _translation_at(translations, path, fallback):
    value = translations
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return fallback
        value = value[key]
    return str(value)


def _lookup_translation(translations, namespace, model_namespace, parameter_name):
    models = translations.get("models", {})
    keys = []
    if namespace:
        keys.append(str(namespace))
    if model_namespace and model_namespace not in keys:
        keys.append(str(model_namespace))

    for key in keys:
        translated = (
            models.get(key, {})
            .get("parameters", {})
            .get(parameter_name)
        )
        if translated:
            return str(translated)
    return parameter_name


def _is_hidden_group(category, section):
    return str(category).startswith("_") or str(section).startswith("_")


def _format_range(value):
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return f"{_stringify(value[0])} ... {_stringify(value[1])}"
    return _stringify(value)


def _allowed_values(parameter):
    options = _stringify(parameter.get("options"))
    value_range = _format_range(parameter.get("range"))
    if options and value_range:
        return f"{options}; range {value_range}"
    if options:
        return options
    return value_range


def _format_unit(value):
    unit = _stringify(value)
    if not unit:
        return unit

    # Common scientific unit formatting for docs readability.
    replacements = [
        ("gCO2-eq/m3", "gCO₂-eq/m³"),
        ("gCO2-eq/kWh", "gCO₂-eq/kWh"),
        ("gCO2-eq/gAS", "gCO₂-eq/gAS"),
        ("gAS/m3", "gAS/m³"),
        ("kg/m3", "kg/m³"),
        ("kg/m2", "kg/m²"),
        ("g/m3", "g/m³"),
        ("kWh/m3", "kWh/m³"),
        ("m3/h", "m³/h"),
        ("Mm3", "Mm³"),
        ("m3", "m³"),
        ("m2", "m²"),
        ("H2O", "H₂O"),
        ("CO2", "CO₂"),
    ]
    for source, target in replacements:
        unit = unit.replace(source, target)

    return unit


def _header_labels(translations):
    return {
        "label": _translation_at(
            translations, ["ui", "design", "parameterlist", "parameter"], "Label"
        ),
        "default": _translation_at(
            translations, ["ui", "design", "parameterlist", "default"], "Default"
        ),
        "unit": _translation_at(
            translations, ["ui", "design", "tables", "units"], "Unit"
        ),
        "allowed": _translation_at(
            translations, ["ui", "design", "parameterlist", "allowed_values"], "Allowed values"
        ),
    }


def _translate_category(translations, category):
    return _translation_at(
        translations,
        ["ui", "design", "categories", str(category)],
        str(category),
    )


def _translate_section(translations, section):
    return _translation_at(
        translations,
        ["ui", "design", "sections", str(section)],
        str(section),
    )


def _discover_model_classes():
    import amanzi.models

    model_classes = {}
    for attribute_name in dir(amanzi.models):
        candidate = getattr(amanzi.models, attribute_name)
        if not isinstance(candidate, type):
            continue
        module_name = getattr(candidate, "__module__", "")
        if not module_name.startswith("amanzi.models."):
            continue
        # Skip generic base/helper classes.
        if attribute_name in {"Model", "Output"}:
            continue

        class_key = _normalize_model_name(attribute_name)
        module_key = _normalize_model_name(module_name.rsplit(".", 1)[-1])
        model_classes[class_key] = candidate
        model_classes[module_key] = candidate

    # Common shorthand alias used in docs.
    if "sandfiltration" in model_classes and "filtration" not in model_classes:
        model_classes["filtration"] = model_classes["sandfiltration"]

    return model_classes


def _read_input_parameters_from_model(model_name):
    normalized = _normalize_model_name(model_name)
    model_classes = _discover_model_classes()
    if normalized not in model_classes:
        raise ValueError(
            f"Unknown model '{model_name}'. Available models: {', '.join(sorted(model_classes))}"
        )

    model_class = model_classes[normalized]
    model = model_class({}, None)

    return normalized, model.parametric_model, model.input_parameters


def run_directive(name, data):
    model_name = _resolve_model_name(data)
    normalized, parametric_files, input_parameters = _read_input_parameters_from_model(model_name)
    translations = _read_translations()
    headers_labels = _header_labels(translations)

    grouped_parameters = {}
    for parameter_name, parameter in input_parameters.items():
        category = parameter.get("category", "general")
        section = parameter.get("section", "general")
        if _is_hidden_group(category, section):
            continue
        grouped_parameters.setdefault((category, section), []).append((parameter_name, parameter))

    nodes = []

    headers = [
        headers_labels["label"],
        headers_labels["default"],
        headers_labels["unit"],
        headers_labels["allowed"],
    ]

    for category, section in sorted(grouped_parameters.keys()):
        rows = []
        for parameter_name, parameter in grouped_parameters[(category, section)]:
            namespace = _stringify(parameter.get("namespace"))
            translated_label = _lookup_translation(
                translations=translations,
                namespace=namespace,
                model_namespace=normalized,
                parameter_name=parameter_name,
            )
            rows.append(
                [
                    translated_label,
                    _stringify(parameter.get("default")),
                    _format_unit(parameter.get("uom")),
                    _allowed_values(parameter),
                ]
            )

        translated_category = _translate_category(translations, category)
        translated_section = _translate_section(translations, section)
        nodes.append(_heading(3, f"{translated_category} / {translated_section}"))
        nodes.append(_table(headers, rows))

    return nodes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--role")
    group.add_argument("--directive")
    group.add_argument("--transform")
    args = parser.parse_args()

    if args.directive:
        data = json.load(sys.stdin)
        declare_result(run_directive(args.directive, data))
    elif args.transform:
        raise NotImplementedError
    elif args.role:
        raise NotImplementedError
    else:
        declare_result(plugin)