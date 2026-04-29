import { MIGRATION_LOG, FIRST_PUBLIC_VERSION } from "./migrationConfig";

function isOlderVersion(a, b) {
  if (!a || a === "") return true;
  const x = (a + "").split(".").map(Number);
  const y = (b + "").split(".").map(Number);
  for (let i = 0; i < Math.max(x.length, y.length); i++) {
    const p = x[i] || 0;
    const q = y[i] || 0;
    if (p < q) return true;
    if (p > q) return false;
  }
  return false;
}

function getMigrationVersions(loadedVersion, currentVersion) {
  const versions = Object.keys(MIGRATION_LOG).filter(
    (v) => !isOlderVersion(v, loadedVersion) && !isOlderVersion(currentVersion, v),
  );
  return versions.sort((a, b) => (isOlderVersion(a, b) ? -1 : 1));
}

function getAtPath(config, path) {
  if (!config || typeof config !== "object") return undefined;
  const parts = path.split(".");
  let obj = config;
  for (let i = 0; i < parts.length - 1; i++) {
    obj = obj?.[parts[i]];
    if (obj == null || typeof obj !== "object") return undefined;
  }
  return obj[parts[parts.length - 1]];
}

function setAtPath(model, path, value) {
  if (!model.configuration) model.configuration = {};
  const parts = path.split(".");
  let obj = model.configuration;
  for (let i = 0; i < parts.length - 1; i++) {
    const key = parts[i];
    if (!obj[key] || typeof obj[key] !== "object") obj[key] = {};
    obj = obj[key];
  }
  obj[parts[parts.length - 1]] = value;
}

/** Map stored value through valueMap with trim + case-insensitive key match for strings. */
function resolveValueMapTarget(raw, valueMap) {
  if (raw === undefined || raw === null) return undefined;
  if (typeof raw === "string") {
    const trimmed = raw.trim();
    if (trimmed === "") return undefined;
    if (valueMap[trimmed] !== undefined) return valueMap[trimmed];
    const lower = trimmed.toLowerCase();
    for (const key of Object.keys(valueMap)) {
      if (typeof key === "string" && key.toLowerCase() === lower) {
        return valueMap[key];
      }
    }
    return undefined;
  }
  if (valueMap[raw] !== undefined) return valueMap[raw];
  return undefined;
}

function applyMigrationToModel(model, entry) {
  if (model.type !== entry.modelType) return false;
  const valueMap = entry.valueMap;
  if (!valueMap || typeof valueMap !== "object") return false;

  const readPaths =
    entry.parameterPaths && entry.parameterPaths.length > 0
      ? entry.parameterPaths
      : [entry.parameter];
  const writePath = entry.parameter;
  if (!writePath) return false;

  let newValue;
  let readPathUsed = null;
  for (const path of readPaths) {
    const raw = getAtPath(model.configuration, path);
    const mapped = resolveValueMapTarget(raw, valueMap);
    if (mapped !== undefined) {
      readPathUsed = path;
      newValue = mapped;
      break;
    }
  }
  if (readPathUsed === null || newValue === undefined) return false;

  setAtPath(model, writePath, newValue);
  if (readPathUsed !== writePath) {
    setAtPath(model, readPathUsed, newValue);
  }
  return true;
}

function ensureKeyIfMissing(model, entry) {
  if (model.type !== entry.modelType) return false;
  const spec = entry.ensureKeyIfMissing;
  if (!spec || typeof spec.path !== "string") return false;
  const defaultValue = spec.value !== undefined ? spec.value : {};
  if (!model.configuration) model.configuration = {};
  const parts = spec.path.split(".");
  const last = parts.pop();
  let obj = model.configuration;
  for (const p of parts) {
    if (!obj[p] || typeof obj[p] !== "object") obj[p] = {};
    obj = obj[p];
  }
  if (obj[last] !== undefined) return false;
  obj[last] = defaultValue;
  return true;
}

function applyLogEntry(model, entry) {
  if (entry.ensureKeyIfMissing) {
    return ensureKeyIfMissing(model, entry);
  }
  return applyMigrationToModel(model, entry);
}

export function compareSemverAsc(a, b) {
  const ax = (a || "0").split(".").map(Number);
  const bx = (b || "0").split(".").map(Number);
  for (let i = 0; i < Math.max(ax.length, bx.length); i++) {
    const p = ax[i] || 0;
    const q = bx[i] || 0;
    if (p !== q) return p - q;
  }
  return 0;
}

function runMigrationLog(project, versions) {
  const changes = [];

  for (const version of versions) {
    const entries = MIGRATION_LOG[version];
    if (!Array.isArray(entries)) continue;
    for (const entry of entries) {
      let count = 0;
      const scenarios = project.scenarios || [];
      for (let scenarioIndex = 0; scenarioIndex < scenarios.length; scenarioIndex++) {
        const scenario = scenarios[scenarioIndex];
        for (const model of scenario.models || []) {
          if (applyLogEntry(model, entry)) count++;
        }
      }
      if (count > 0) {
        changes.push({
          key: "ui.migration.change_log_entry",
          params: { descriptionKey: entry.descriptionKey, count },
          migrationVersion: version,
        });
      }
    }
  }
  changes.sort((a, b) => {
    const byV = compareSemverAsc(a.migrationVersion, b.migrationVersion);
    if (byV !== 0) return byV;
    const da = a.params?.descriptionKey || "";
    const db = b.params?.descriptionKey || "";
    return da.localeCompare(db);
  });
  return changes;
}

export function migrateProject(project, currentVersion) {
  if (!project || typeof project !== "object") {
    return { project, changes: [], migrated: false, fromVersion: "", toVersion: "" };
  }
  if (!project.metadata) project.metadata = {};

  const rawLoaded = project.metadata.amanzi_version;
  const effectiveLoaded = rawLoaded || FIRST_PUBLIC_VERSION;

  if (!isOlderVersion(effectiveLoaded, currentVersion)) {
    return { project, changes: [], migrated: false, fromVersion: "", toVersion: "" };
  }

  const versions = getMigrationVersions(effectiveLoaded, currentVersion);
  const changes = runMigrationLog(project, versions);
  project.metadata.amanzi_version = currentVersion;
  return {
    project,
    changes,
    migrated: true,
    fromVersion: effectiveLoaded,
    toVersion: currentVersion,
  };
}
