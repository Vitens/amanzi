/*
  On-disk format migrations (forward-only). See projectMigration.js for behaviour.

  Structure
  - MIGRATION_LOG keys are release versions (e.g. "1.0.5"). For a file older than the app,
    every key in (loadedVersion, currentAppVersion] runs, in version order.
  - Each value is an array of entries. All entries for a version run; each entry is tried on
    every model in every scenario.

  Common fields (every entry)
  - modelType: model `type` string (must match or the entry is skipped).
  - descriptionKey: vue-i18n key for the human-readable line (e.g. ui.migration.descriptions.<id>).
  - id: optional stable id; keep it aligned with descriptions.<id> in locale JSON for clarity.

  Only two entry kinds exist (no mixing in one object):
  1) valueMap  — remap an existing stored value to a new one.
  2) ensureKeyIfMissing — if a path under configuration is undefined, set a default.

  If an entry has `ensureKeyIfMissing`, that branch runs and `valueMap` is ignored for that entry.
  To add a third kind, extend applyLogEntry() in projectMigration.js.

  --- valueMap ---
  - parameter: dot path under model.configuration to WRITE the new value (canonical location).
  - parameterPaths: optional array of dot paths to READ, tried in order. Use when old files stored
    the same setting at different paths (e.g. "chemical" vs "parameters.chemical"). First path
    where the value is non-null and appears as a key in valueMap wins.
  - valueMap: object map { oldStoredValue: newValue }. Only applies when current value matches a key
    exactly (e.g. NaOH -> lye). If nothing matches, the model is unchanged for this entry.

  --- ensureKeyIfMissing ---
  - ensureKeyIfMissing.path: dot path under model.configuration. If the final key is missing,
    it is created.
  - ensureKeyIfMissing.value: optional; defaults to {}. Use for new nested objects/defaults.

  When amanzi_version is absent on load, the file is treated as FIRST_PUBLIC_VERSION for comparison.
*/

export const FIRST_PUBLIC_VERSION = "1.0.0";

export const MIGRATION_LOG = {
  "1.0.4": [
    {
      id: "dosing_chemical_slugs",
      modelType: "dosing",
      descriptionKey: "ui.migration.descriptions.dosing_chemical_slugs",
      parameter: "parameters.chemical",
      parameterPaths: ["chemical", "parameters.chemical"],
      valueMap: { NaOH: "lye" },
    }
  ]
};
