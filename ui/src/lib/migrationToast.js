import { h } from "vue";
import { ElNotification } from "element-plus";
import { compareSemverAsc } from "./projectMigration";
import "./migrationNotification.css";

const TAG_COLOR_VARIANTS = 8;

function versionTagVariantMap(versions) {
  const unique = [...new Set(versions.filter(Boolean))].sort(compareSemverAsc);
  const map = new Map();
  unique.forEach((v, i) => map.set(v, i % TAG_COLOR_VARIANTS));
  return map;
}

export function notifyMigrationIfNeeded(projectStore, t) {
  const changes = projectStore.lastMigrationChanges || [];
  const migrated = projectStore.migrationAppliedOnLastOpen;
  if (!migrated && changes.length === 0) {
    return;
  }

  const fromV = projectStore.migrationNotifyFrom || "";
  const toV = projectStore.migrationNotifyTo || "";

  const bodyChildren = [];
  if (fromV && toV) {
    bodyChildren.push(
      h("div", { class: "migration-notify-version-range" }, t("ui.migration.notification_version_range", { from: fromV, to: toV })),
    );
  }
  const rowItems = changes.filter((c) => c?.key);
  if (rowItems.length > 0) {
    const variantByVersion = versionTagVariantMap(rowItems.map((c) => c.migrationVersion));
    bodyChildren.push(
      h("div", { class: "migration-notify-changes" }, [
        h("div", { class: "migration-notify-changes-head" }, [
          h("div", { class: "migration-notify-changes-label migration-notify-changes-label--tag" }, t("ui.migration.notification_col_version")),
          h("div", { class: "migration-notify-changes-label migration-notify-changes-label--desc" }, t("ui.migration.notification_col_change")),
        ]),
        h(
          "ul",
          { class: "migration-notify-list", role: "list" },
          rowItems.map((c, i) => {
            const p = c.params || {};
            const description = p.descriptionKey ? t(p.descriptionKey) : p.description ?? "";
            const text = t(c.key, { description, count: p.count });
            const version = c.migrationVersion;
            const variant = version ? variantByVersion.get(version) ?? 0 : 0;
            const tagClass = `migration-notify-version-tag migration-notify-version-tag--${variant}`;
            return h("li", { key: i, class: "migration-notify-item" }, [
              h("div", { class: "migration-notify-row" }, [
                h("div", { class: "migration-notify-tag-cell" }, [
                  version
                    ? h("span", { class: tagClass }, t("ui.migration.notification_version_tag", { version }))
                    : h("span", { class: `${tagClass} migration-notify-version-tag--empty` }, "—"),
                ]),
                h("div", { class: "migration-notify-desc-cell" }, [h("span", { class: "migration-notify-change-text" }, text)]),
              ]),
            ]);
          }),
        ),
      ]),
    );
  } else if (migrated) {
    bodyChildren.push(
      h("p", { class: "migration-notify-no-rows" }, t("ui.migration.notification_no_model_changes")),
    );
  }

  if (bodyChildren.length === 0) {
    projectStore.lastMigrationChanges = [];
    projectStore.migrationAppliedOnLastOpen = false;
    projectStore.migrationNotifyFrom = "";
    projectStore.migrationNotifyTo = "";
    return;
  }

  ElNotification({
    title: t("ui.migration.notification_title"),
    message: h("div", { class: "migration-notify-body" }, bodyChildren),
    type: "info",
    duration: 0,
    showClose: true,
    position: "top-right",
    customClass: "migration-update-notification",
  });

  projectStore.lastMigrationChanges = [];
  projectStore.migrationAppliedOnLastOpen = false;
  projectStore.migrationNotifyFrom = "";
  projectStore.migrationNotifyTo = "";
}
