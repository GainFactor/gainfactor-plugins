(() => {
  if (window.__GAINFACTOR_PM_PROTOTYPE_REVIEW_LOADED__) return
  window.__GAINFACTOR_PM_PROTOTYPE_REVIEW_LOADED__ = true

  const initialize = () => {
    const config = window.GAINFACTOR_PM_PROTOTYPE_REVIEW_CONFIG || {}
    const locale = String(config.locale || document.documentElement.lang || "zh-CN")
    const isChinese = locale.toLowerCase().startsWith("zh")
    const text = isChinese
      ? {
          launcher: "评审模式",
          launcherOpen: "开启原型评审模式",
          launcherClose: "退出原型评审模式",
          toolbarStatus: "评审模式已开启",
          toolbarTip: "点击页面区域添加意见",
          pageFeedback: "页面整体意见",
          showList: "查看意见",
          exit: "退出评审",
          toolLabel: "原型评审工具",
          addTitle: "添加意见",
          listTitle: "意见汇总",
          close: "关闭评审面板",
          target: "意见位置",
          pageWhole: "页面整体",
          type: "意见类型",
          priority: "优先级",
          comment: "问题或建议",
          expectation: "希望如何调整",
          optional: "选填",
          commentPlaceholder: "请描述具体问题、影响或建议。",
          expectationPlaceholder: "请描述希望看到的调整结果。",
          privacy:
            "意见只保存在当前浏览器和当前页面地址中，不会主动上传到网络。",
          cancel: "取消",
          save: "保存意见",
          summary: "评审意见",
          addPage: "添加页面意见",
          empty: "还没有评审意见",
          emptyTip: "关闭面板并点击页面区域，即可记录第一条意见。",
          delete: "删除",
          expected: "希望调整",
          aiReady: "AI 读取已就绪",
          aiTip: "保持当前页面打开，直接告诉 AI：“读取当前页的评审意见”。",
          showMarkdown: "查看 AI 可读取的 Markdown",
          copyMarkdown: "复制 Markdown",
          expandMarkdown: "展开 Markdown",
          clear: "清空意见",
          noComments: "还没有可以处理的评审意见",
          copied: "全部意见已复制",
          copyFallback: "自动复制失败，已展开并选中 Markdown",
          expanded: "完整 Markdown 已展开",
          saved: "意见已保存",
          deleted: "意见已删除",
          cleared: "评审意见已清空",
          clearConfirm: "确认清空全部评审意见？清空后无法恢复。",
          required: "请填写问题或建议",
          modeStarted: "评审模式已开启，点击页面区域即可添加意见",
          urlReady: "URL 与页面出口均可读取",
          domOnly: "当前页面使用其他 hash，AI 可从页面出口读取",
          urlTooLong: "意见较多，AI 可从页面出口读取",
          count: (count) => `${count} 条意见`,
          summaryCount: (count, blockers, important) =>
            `共 ${count} 条 · 阻塞 ${blockers} · 重要 ${important}`,
          markdownTitle: (name) => `# ${name}原型评审意见`,
          exportedAt: "导出时间",
          total: "意见总数",
          page: "页面",
          location: "位置",
          pageAddress: "页面地址",
          targetPath: "元素标识",
          recordedAt: "记录时间",
          issue: "问题或建议",
          desired: "希望如何调整",
          types: {
            flow: "流程",
            information: "信息",
            state: "状态",
            permission: "权限",
            interaction: "交互",
            copy: "文案",
            visual: "视觉",
          },
          priorities: {
            blocker: "阻塞",
            important: "重要",
            improvement: "优化",
          },
        }
      : {
          launcher: "Review",
          launcherOpen: "Open prototype review mode",
          launcherClose: "Exit prototype review mode",
          toolbarStatus: "Review mode is on",
          toolbarTip: "Select a page area to add feedback",
          pageFeedback: "Page feedback",
          showList: "View feedback",
          exit: "Exit review",
          toolLabel: "Prototype review",
          addTitle: "Add feedback",
          listTitle: "Feedback summary",
          close: "Close review panel",
          target: "Feedback location",
          pageWhole: "Whole page",
          type: "Feedback type",
          priority: "Priority",
          comment: "Issue or suggestion",
          expectation: "Desired adjustment",
          optional: "Optional",
          commentPlaceholder: "Describe the issue, impact, or suggestion.",
          expectationPlaceholder: "Describe the expected result.",
          privacy:
            "Feedback stays in this browser and page URL. It is not uploaded automatically.",
          cancel: "Cancel",
          save: "Save feedback",
          summary: "Review feedback",
          addPage: "Add page feedback",
          empty: "No feedback yet",
          emptyTip: "Close the panel and select a page area to add the first item.",
          delete: "Delete",
          expected: "Desired adjustment",
          aiReady: "Ready for AI",
          aiTip: 'Keep this page open and tell the AI: "Read feedback from the current page."',
          showMarkdown: "View AI-readable Markdown",
          copyMarkdown: "Copy Markdown",
          expandMarkdown: "Expand Markdown",
          clear: "Clear feedback",
          noComments: "There is no feedback to process",
          copied: "All feedback copied",
          copyFallback: "Copy failed. Markdown is expanded and selected.",
          expanded: "Full Markdown expanded",
          saved: "Feedback saved",
          deleted: "Feedback deleted",
          cleared: "Feedback cleared",
          clearConfirm: "Clear all review feedback? This cannot be undone.",
          required: "Enter an issue or suggestion",
          modeStarted: "Review mode is on. Select a page area to add feedback.",
          urlReady: "URL and page exports are readable",
          domOnly: "This page uses another hash; AI can read the page export",
          urlTooLong: "Feedback is large; AI can read the page export",
          count: (count) => `${count} item${count === 1 ? "" : "s"}`,
          summaryCount: (count, blockers, important) =>
            `${count} total · ${blockers} blocker · ${important} important`,
          markdownTitle: (name) => `# ${name} prototype review feedback`,
          exportedAt: "Exported",
          total: "Total feedback",
          page: "Page",
          location: "Location",
          pageAddress: "Page URL",
          targetPath: "Element",
          recordedAt: "Recorded",
          issue: "Issue or suggestion",
          desired: "Desired adjustment",
          types: {
            flow: "Flow",
            information: "Information",
            state: "State",
            permission: "Permission",
            interaction: "Interaction",
            copy: "Copy",
            visual: "Visual",
          },
          priorities: {
            blocker: "Blocker",
            important: "Important",
            improvement: "Improvement",
          },
        }

    const SCHEMA = "gainfactor-pm-prototype-review/v1"
    const HASH_PREFIX = "#prototype-review-v1="
    const prototypeId = String(
      config.prototypeId ||
        document.documentElement.dataset.prototypeId ||
        window.location.pathname.replace(/\/[^/]*$/, "") ||
        "prototype",
    )
    const projectName = String(
      config.projectName ||
        document.documentElement.dataset.prototypeName ||
        document.title ||
        (isChinese ? "交互" : "Interactive"),
    )
    const storageKey =
      config.storageKey || `gainfactor-pm-prototype-review-v1:${prototypeId}`
    const maxUrlLength = Number(config.maxUrlLength || 60000)
    const targetSelector = [
      "[data-review-target]",
      "button",
      "a",
      "tr",
      "article",
      "section",
      "form",
      "fieldset",
      "label",
      "[role='button']",
      "[class*='card']",
      "[class*='panel']",
    ].join(",")

    let comments = loadComments()
    let reviewActive = false
    let selectedTarget = null
    let hoveredTarget = null
    let toastTimer = null

    const root = document.createElement("div")
    root.className = "tpr-root"
    root.dataset.reviewUi = "true"
    root.dataset.reviewAiReadable = SCHEMA
    root.innerHTML = `
      <button
        class="tpr-launcher"
        type="button"
        aria-label="${text.launcherOpen}"
        aria-pressed="false"
        data-review-action="toggle"
      >
        <span aria-hidden="true">✦</span>
        <span>${text.launcher}</span>
        <span class="tpr-count tpr-hide" data-review-count>0</span>
      </button>

      <div class="tpr-toolbar" role="toolbar" aria-label="${text.toolLabel}" aria-hidden="true">
        <strong><span class="tpr-live-dot"></span>${text.toolbarStatus}</strong>
        <span class="tpr-toolbar-tip">${text.toolbarTip}</span>
        <button type="button" data-review-action="page-feedback">${text.pageFeedback}</button>
        <button type="button" data-review-action="show-list">
          ${text.showList} <span data-review-toolbar-count>0</span>
        </button>
        <button type="button" data-review-action="exit">${text.exit}</button>
      </div>

      <div class="tpr-backdrop" data-review-action="close-panel"></div>

      <aside
        class="tpr-panel"
        role="dialog"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="tpr-panel-title"
      >
        <header class="tpr-panel-header">
          <div>
            <span>${text.toolLabel}</span>
            <h2 id="tpr-panel-title">${text.addTitle}</h2>
          </div>
          <button type="button" class="tpr-icon-button" data-review-action="close-panel" aria-label="${text.close}">×</button>
        </header>

        <div class="tpr-panel-body" data-review-form-view>
          <div class="tpr-target-card">
            <span>${text.target}</span>
            <strong data-review-target-page>${text.pageWhole}</strong>
            <p data-review-target-summary>${text.pageWhole}</p>
          </div>

          <form data-review-form>
            <div class="tpr-form-row">
              <label>
                <span>${text.type}</span>
                <select data-review-type>
                  ${Object.entries(text.types)
                    .map(([value, label]) => `<option value="${value}">${label}</option>`)
                    .join("")}
                </select>
              </label>
              <label>
                <span>${text.priority}</span>
                <select data-review-priority>
                  <option value="important">${text.priorities.important}</option>
                  <option value="blocker">${text.priorities.blocker}</option>
                  <option value="improvement">${text.priorities.improvement}</option>
                </select>
              </label>
            </div>

            <label class="tpr-form-field">
              <span>${text.comment}<b>*</b></span>
              <textarea data-review-comment rows="5" placeholder="${text.commentPlaceholder}" required></textarea>
            </label>

            <label class="tpr-form-field">
              <span>${text.expectation}<small>${text.optional}</small></span>
              <textarea data-review-expectation rows="3" placeholder="${text.expectationPlaceholder}"></textarea>
            </label>

            <p class="tpr-privacy">${text.privacy}</p>

            <div class="tpr-panel-actions">
              <button class="tpr-button secondary" type="button" data-review-action="close-panel">${text.cancel}</button>
              <button class="tpr-button primary" type="submit">${text.save}</button>
            </div>
          </form>
        </div>

        <div class="tpr-panel-body tpr-hide" data-review-list-view>
          <div class="tpr-list-summary">
            <div>
              <strong>${text.summary}</strong>
              <span data-review-list-summary>${text.empty}</span>
            </div>
            <button type="button" class="tpr-text-button" data-review-action="page-feedback">${text.addPage}</button>
          </div>

          <div class="tpr-comment-list" data-review-comment-list></div>

          <div class="tpr-ai-card" data-gainfactor-pm-review-export="${SCHEMA}">
            <div>
              <strong>${text.aiReady}</strong>
              <span data-review-ai-count>${text.count(0)}</span>
            </div>
            <p>${text.aiTip}</p>
            <p class="tpr-bridge-status" data-review-bridge-status></p>
            <details data-review-markdown-details>
              <summary>${text.showMarkdown}</summary>
              <textarea id="gainfactor-pm-review-output" rows="10" readonly aria-label="${text.showMarkdown}"></textarea>
            </details>
          </div>

          <div class="tpr-export-actions">
            <button class="tpr-button secondary" type="button" data-review-action="copy">${text.copyMarkdown}</button>
            <button class="tpr-button secondary" type="button" data-review-action="expand">${text.expandMarkdown}</button>
            <button class="tpr-text-button danger" type="button" data-review-action="clear">${text.clear}</button>
          </div>
        </div>
      </aside>

      <div class="tpr-toast" role="status" aria-live="polite" aria-hidden="true"></div>
    `
    document.body.append(root)

    const find = (selector) => root.querySelector(selector)
    const panel = find(".tpr-panel")
    const toolbar = find(".tpr-toolbar")
    const formView = find("[data-review-form-view]")
    const listView = find("[data-review-list-view]")
    const form = find("[data-review-form]")

    function safeParse(value) {
      if (!value) return []
      try {
        const parsed = JSON.parse(value)
        return Array.isArray(parsed) ? parsed : []
      } catch {
        return []
      }
    }

    function mergeComments(...lists) {
      const merged = new Map()
      lists.flat().forEach((comment) => {
        if (
          comment &&
          typeof comment.id === "string" &&
          typeof comment.createdAt === "string" &&
          !Number.isNaN(Date.parse(comment.createdAt))
        ) {
          merged.set(comment.id, comment)
        }
      })
      return Array.from(merged.values()).sort((a, b) =>
        a.createdAt.localeCompare(b.createdAt),
      )
    }

    function encodePayload(value) {
      const bytes = new TextEncoder().encode(value)
      let binary = ""
      bytes.forEach((byte) => {
        binary += String.fromCharCode(byte)
      })
      return window
        .btoa(binary)
        .replaceAll("+", "-")
        .replaceAll("/", "_")
        .replace(/=+$/g, "")
    }

    function decodePayload(value) {
      const base64 = value.replaceAll("-", "+").replaceAll("_", "/")
      const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, "=")
      const binary = window.atob(padded)
      const bytes = Uint8Array.from(binary, (character) =>
        character.charCodeAt(0),
      )
      return new TextDecoder().decode(bytes)
    }

    function loadHashComments() {
      if (!window.location.hash.startsWith(HASH_PREFIX)) return []
      try {
        const payload = JSON.parse(
          decodePayload(window.location.hash.slice(HASH_PREFIX.length)),
        )
        return payload?.schema === SCHEMA && Array.isArray(payload.comments)
          ? payload.comments
          : []
      } catch {
        return []
      }
    }

    function loadComments() {
      let localComments = []
      let sessionComments = []
      try {
        localComments = safeParse(window.localStorage.getItem(storageKey))
      } catch {
        localComments = []
      }
      try {
        sessionComments = safeParse(window.sessionStorage.getItem(storageKey))
      } catch {
        sessionComments = []
      }
      return mergeComments(localComments, sessionComments, loadHashComments())
    }

    function saveComments() {
      const value = JSON.stringify(comments)
      try {
        window.localStorage.setItem(storageKey, value)
      } catch {
        try {
          window.sessionStorage.setItem(storageKey, value)
        } catch {
          // URL and DOM exports remain available when browser storage is disabled.
        }
      }
      updateCounts()
      syncExport()
    }

    function pageContext() {
      const role = document.body.dataset.reviewRole || ""
      const view = document.body.dataset.reviewView || ""
      const heading = normalizeText(document.querySelector("h1")?.textContent, 70)
      const fallback = heading || normalizeText(document.title, 70) || text.pageWhole
      const page =
        document.body.dataset.reviewPage ||
        [role, view].filter(Boolean).join(isChinese ? "｜" : " | ") ||
        fallback
      return {
        page,
        role,
        view,
        location: `${window.location.pathname.split("/").pop() || ""}${window.location.search}`,
      }
    }

    function normalizeText(value, limit = 110) {
      const normalized = String(value || "")
        .replace(/\s+/g, " ")
        .trim()
      return normalized.length > limit
        ? `${normalized.slice(0, limit)}…`
        : normalized
    }

    function targetSummary(target) {
      if (!target) return text.pageWhole
      return (
        normalizeText(target.getAttribute?.("aria-label")) ||
        normalizeText(target.textContent) ||
        target.tagName.toLowerCase()
      )
    }

    function targetSection(target) {
      if (!target) return text.pageWhole
      const explicit = target.closest("[data-review-target]")?.dataset.reviewTarget
      if (explicit) return normalizeText(explicit, 70)
      const container = target.closest("section, article, form, fieldset, tr, main")
      const heading = container?.querySelector("h1, h2, h3, legend")
      return normalizeText(heading?.textContent, 70) || pageContext().page
    }

    function targetPath(target) {
      if (!target) return text.pageWhole
      if (target.id) return `#${target.id}`
      const testId = target.getAttribute?.("data-testid")
      if (testId) return `[data-testid="${testId}"]`
      const reviewTarget = target.getAttribute?.("data-review-target")
      if (reviewTarget) return `[data-review-target="${reviewTarget}"]`
      const stableClasses = Array.from(target.classList || [])
        .filter(
          (name) =>
            !["active", "show", "hide", "tpr-hover", "tpr-selected"].includes(
              name,
            ),
        )
        .slice(0, 2)
      return `${target.tagName.toLowerCase()}${stableClasses
        .map((name) => `.${name}`)
        .join("")}`
    }

    function findTarget(element) {
      if (!(element instanceof Element) || root.contains(element)) return null
      const target = element.closest(targetSelector) || element
      if (target === document.body || target === document.documentElement) return null
      return target
    }

    function clearHighlight() {
      hoveredTarget?.classList.remove("tpr-hover")
      selectedTarget?.classList.remove("tpr-selected")
      hoveredTarget = null
      selectedTarget = null
    }

    function setActive(active) {
      reviewActive = active
      document.body.classList.toggle("tpr-active", active)
      root.classList.toggle("tpr-active", active)
      toolbar.setAttribute("aria-hidden", String(!active))
      const launcher = find(".tpr-launcher")
      launcher.setAttribute("aria-pressed", String(active))
      launcher.setAttribute(
        "aria-label",
        active ? text.launcherClose : text.launcherOpen,
      )
      if (!active) {
        closePanel()
        clearHighlight()
      } else {
        showToast(text.modeStarted)
      }
    }

    function openPanel() {
      root.classList.add("tpr-panel-open")
      panel.setAttribute("aria-hidden", "false")
    }

    function closePanel() {
      root.classList.remove("tpr-panel-open")
      panel.setAttribute("aria-hidden", "true")
      selectedTarget?.classList.remove("tpr-selected")
      selectedTarget = null
    }

    function showForm(target) {
      clearHighlight()
      selectedTarget = target
      selectedTarget?.classList.add("tpr-selected")
      const context = pageContext()
      find("[data-review-target-page]").textContent = context.page
      find("[data-review-target-summary]").textContent = target
        ? `${targetSection(target)} · ${targetSummary(target)}`
        : text.pageWhole
      find("[data-review-comment]").value = ""
      find("[data-review-expectation]").value = ""
      find("[data-review-type]").value = "flow"
      find("[data-review-priority]").value = "important"
      formView.classList.remove("tpr-hide")
      listView.classList.add("tpr-hide")
      find("#tpr-panel-title").textContent = text.addTitle
      openPanel()
      window.setTimeout(() => find("[data-review-comment]").focus(), 50)
    }

    function showList() {
      selectedTarget?.classList.remove("tpr-selected")
      selectedTarget = null
      formView.classList.add("tpr-hide")
      listView.classList.remove("tpr-hide")
      find("#tpr-panel-title").textContent = text.listTitle
      renderList()
      openPanel()
    }

    function nextId() {
      const largest = comments.reduce((max, comment) => {
        const match = String(comment.id).match(/PR-(\d+)/)
        return Math.max(max, Number(match?.[1] || 0))
      }, 0)
      return `PR-${String(largest + 1).padStart(3, "0")}`
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;")
    }

    function formatDate(value) {
      return new Intl.DateTimeFormat(locale, {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      }).format(new Date(value))
    }

    function renderList() {
      const list = find("[data-review-comment-list]")
      const summary = find("[data-review-list-summary]")
      if (!comments.length) {
        summary.textContent = text.empty
        list.innerHTML = `
          <div class="tpr-empty">
            <span aria-hidden="true">✦</span>
            <strong>${text.empty}</strong>
            <p>${text.emptyTip}</p>
          </div>
        `
        return
      }

      const blockers = comments.filter(
        (comment) => comment.priority === "blocker",
      ).length
      const important = comments.filter(
        (comment) => comment.priority === "important",
      ).length
      summary.textContent = text.summaryCount(
        comments.length,
        blockers,
        important,
      )
      list.innerHTML = comments
        .slice()
        .reverse()
        .map(
          (comment) => `
            <article class="tpr-comment-card">
              <div class="tpr-comment-head">
                <span class="tpr-comment-id">${escapeHtml(comment.id)}</span>
                <span class="tpr-priority ${escapeHtml(comment.priority)}">${escapeHtml(
                  text.priorities[comment.priority] || comment.priority,
                )}</span>
                <span class="tpr-type">${escapeHtml(
                  text.types[comment.type] || comment.type,
                )}</span>
                <button
                  type="button"
                  class="tpr-delete"
                  data-review-delete="${escapeHtml(comment.id)}"
                  aria-label="${text.delete} ${escapeHtml(comment.id)}"
                >${text.delete}</button>
              </div>
              <strong class="tpr-comment-page">${escapeHtml(comment.page)}</strong>
              <span class="tpr-comment-target">${escapeHtml(
                comment.section,
              )} · ${escapeHtml(comment.targetSummary)}</span>
              <p>${escapeHtml(comment.comment)}</p>
              ${
                comment.expectation
                  ? `<div class="tpr-expectation"><span>${text.expected}</span>${escapeHtml(
                      comment.expectation,
                    )}</div>`
                  : ""
              }
              <time>${formatDate(comment.createdAt)}</time>
            </article>
          `,
        )
        .join("")
    }

    function updateCounts() {
      const count = comments.length
      const launcherCount = find("[data-review-count]")
      launcherCount.textContent = String(count)
      launcherCount.classList.toggle("tpr-hide", count === 0)
      find("[data-review-toolbar-count]").textContent = String(count)
      find("[data-review-ai-count]").textContent = text.count(count)
      root.dataset.reviewCount = String(count)
      if (!listView.classList.contains("tpr-hide")) renderList()
    }

    function buildMarkdown() {
      const lines = [
        text.markdownTitle(projectName),
        "",
        `${text.exportedAt}：${new Date().toLocaleString(locale, {
          hour12: false,
        })}`,
        `${text.total}：${comments.length}`,
        "",
      ]

      comments.forEach((comment) => {
        lines.push(
          `## ${comment.id} · ${
            text.priorities[comment.priority] || comment.priority
          } · ${text.types[comment.type] || comment.type}`,
          "",
          `- ${text.page}：${comment.page}`,
          `- ${text.location}：${comment.section} · ${comment.targetSummary}`,
          `- ${text.pageAddress}：${comment.location}`,
          `- ${text.targetPath}：\`${String(comment.targetPath).replaceAll(
            "`",
            "'",
          )}\``,
          `- ${text.recordedAt}：${new Date(comment.createdAt).toLocaleString(
            locale,
            { hour12: false },
          )}`,
          "",
          `**${text.issue}**`,
          "",
          comment.comment,
          "",
        )
        if (comment.expectation) {
          lines.push(`**${text.desired}**`, "", comment.expectation, "")
        }
      })

      return lines.join("\n")
    }

    function buildExport(markdown) {
      return {
        schema: SCHEMA,
        exportedAt: new Date().toISOString(),
        count: comments.length,
        markdown,
        comments: comments.map((comment) => ({ ...comment })),
      }
    }

    function replaceReviewHash(payload) {
      const status = find("[data-review-bridge-status]")
      const currentHash = window.location.hash
      const hasForeignHash = currentHash && !currentHash.startsWith(HASH_PREFIX)
      if (config.urlBridge === false || hasForeignHash) {
        root.dataset.reviewUrlBridge = "dom-only"
        status.textContent = text.domOnly
        return
      }

      let nextHash = ""
      if (comments.length) {
        const urlPayload = {
          schema: payload.schema,
          exportedAt: payload.exportedAt,
          count: payload.count,
          comments: payload.comments,
        }
        nextHash = `${HASH_PREFIX}${encodePayload(JSON.stringify(urlPayload))}`
        if (nextHash.length > maxUrlLength) {
          nextHash = ""
          root.dataset.reviewUrlBridge = "overflow"
          status.textContent = text.urlTooLong
        } else {
          root.dataset.reviewUrlBridge = "ready"
          status.textContent = text.urlReady
        }
      } else {
        root.dataset.reviewUrlBridge = "ready"
        status.textContent = text.urlReady
      }

      if (currentHash === nextHash) return
      try {
        window.history.replaceState(
          window.history.state,
          "",
          `${window.location.pathname}${window.location.search}${nextHash}`,
        )
      } catch {
        root.dataset.reviewUrlBridge = "dom-only"
        status.textContent = text.domOnly
      }
    }

    function syncExport() {
      const markdown = buildMarkdown()
      const payload = buildExport(markdown)
      window.__GAINFACTOR_PM_PROTOTYPE_REVIEW__ = payload
      find("#gainfactor-pm-review-output").value = markdown
      replaceReviewHash(payload)
    }

    async function copyMarkdown() {
      if (!comments.length) {
        showToast(text.noComments, "warn")
        return
      }
      const markdown = buildMarkdown()
      let copied = false
      try {
        await navigator.clipboard.writeText(markdown)
        copied = true
      } catch {
        const textarea = document.createElement("textarea")
        textarea.value = markdown
        textarea.style.position = "fixed"
        textarea.style.opacity = "0"
        document.body.append(textarea)
        textarea.select()
        copied = document.execCommand("copy")
        textarea.remove()
      }
      if (!copied) {
        expandMarkdown()
        find("#gainfactor-pm-review-output").select()
        showToast(text.copyFallback, "warn")
        return
      }
      showToast(text.copied)
    }

    function expandMarkdown() {
      if (!comments.length) {
        showToast(text.noComments, "warn")
        return
      }
      find("[data-review-markdown-details]").open = true
      find("#gainfactor-pm-review-output").focus()
      showToast(text.expanded)
    }

    function showToast(message, type = "success") {
      const toast = find(".tpr-toast")
      window.clearTimeout(toastTimer)
      toast.textContent = message
      toast.className = `tpr-toast show ${type}`
      toast.setAttribute("aria-hidden", "false")
      toastTimer = window.setTimeout(() => {
        toast.classList.remove("show")
        toast.setAttribute("aria-hidden", "true")
        toast.textContent = ""
      }, 2600)
    }

    root.addEventListener("click", (event) => {
      const actionElement = event.target.closest("[data-review-action]")
      if (actionElement) {
        const action = actionElement.dataset.reviewAction
        if (action === "toggle") setActive(!reviewActive)
        if (action === "page-feedback") showForm(null)
        if (action === "show-list") showList()
        if (action === "close-panel") closePanel()
        if (action === "exit") setActive(false)
        if (action === "copy") copyMarkdown()
        if (action === "expand") expandMarkdown()
        if (action === "clear") {
          if (!comments.length) return
          if (!window.confirm(text.clearConfirm)) return
          comments = []
          saveComments()
          renderList()
          showToast(text.cleared)
        }
        return
      }

      const deleteElement = event.target.closest("[data-review-delete]")
      if (deleteElement) {
        comments = comments.filter(
          (comment) => comment.id !== deleteElement.dataset.reviewDelete,
        )
        saveComments()
        renderList()
        showToast(text.deleted)
      }
    })

    form.addEventListener("submit", (event) => {
      event.preventDefault()
      const comment = find("[data-review-comment]").value.trim()
      if (!comment) {
        showToast(text.required, "warn")
        return
      }
      const context = pageContext()
      comments.push({
        id: nextId(),
        type: find("[data-review-type]").value,
        priority: find("[data-review-priority]").value,
        comment,
        expectation: find("[data-review-expectation]").value.trim(),
        page: context.page,
        role: context.role,
        view: context.view,
        location: context.location,
        section: targetSection(selectedTarget),
        targetSummary: targetSummary(selectedTarget),
        targetPath: targetPath(selectedTarget),
        createdAt: new Date().toISOString(),
      })
      const savedId = comments.at(-1).id
      saveComments()
      closePanel()
      showToast(`${savedId} · ${text.saved}`)
    })

    document.addEventListener(
      "mouseover",
      (event) => {
        if (!reviewActive || root.classList.contains("tpr-panel-open")) return
        const target = findTarget(event.target)
        if (target === hoveredTarget) return
        hoveredTarget?.classList.remove("tpr-hover")
        hoveredTarget = target
        hoveredTarget?.classList.add("tpr-hover")
      },
      true,
    )

    document.addEventListener(
      "mouseout",
      (event) => {
        if (!hoveredTarget || hoveredTarget.contains(event.relatedTarget)) return
        hoveredTarget.classList.remove("tpr-hover")
        hoveredTarget = null
      },
      true,
    )

    document.addEventListener(
      "click",
      (event) => {
        if (
          !reviewActive ||
          root.contains(event.target) ||
          root.classList.contains("tpr-panel-open")
        ) {
          return
        }
        const target = findTarget(event.target)
        if (!target) return
        event.preventDefault()
        event.stopImmediatePropagation()
        showForm(target)
      },
      true,
    )

    document.addEventListener(
      "keydown",
      (event) => {
        if (event.key !== "Escape") return
        if (root.classList.contains("tpr-panel-open")) {
          event.preventDefault()
          closePanel()
        } else if (reviewActive) {
          event.preventDefault()
          setActive(false)
        }
      },
      true,
    )

    window.addEventListener("storage", (event) => {
      if (event.key !== storageKey) return
      comments = mergeComments(safeParse(event.newValue))
      updateCounts()
      syncExport()
    })

    saveComments()
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true })
  } else {
    initialize()
  }
})()
