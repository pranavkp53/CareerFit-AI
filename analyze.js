document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#analysisForm");
    const fileInput = document.querySelector("#resumeFile");
    const fileName = document.querySelector("#fileName");
    const dropZone = document.querySelector("#dropZone");

    const uploadPanel = document.querySelector("#uploadPanel");
    const createPanel = document.querySelector("#createPanel");
    const resumeText = document.querySelector("#resumeText");

    const uploadError = document.querySelector("#uploadError");
    const uploadStatus = document.querySelector("#uploadStatus");

    const generateButton = document.querySelector("#generateButton");
    const tabs = document.querySelectorAll(".tab");

    const jobTitle = document.querySelector("#jobTitle");
    const companyName = document.querySelector("#companyName");
    const jobDescription = document.querySelector("#jobDescription");

    const resultsSection = document.querySelector("#analysisResults");

    let activeMode = "upload";
    let latestResumeText = "";

    // ========================================================
    // 1. RESUME INPUT TABS
    // ========================================================

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            activeMode = tab.dataset.tab;

            tabs.forEach((item) => {
                const active = item === tab;

                item.classList.toggle("active", active);
                item.setAttribute("aria-selected", String(active));
            });

            uploadPanel.hidden = activeMode !== "upload";
            createPanel.hidden = activeMode !== "create";

            fileInput.required = activeMode === "upload";
            resumeText.required = activeMode === "create";

            clearMessages();
        });
    });

    // ========================================================
    // 2. STATUS AND ERROR MESSAGES
    // ========================================================

    function clearMessages() {
        uploadError.hidden = true;
        uploadError.textContent = "";
        uploadStatus.textContent = "";
    }

    function showError(message) {
        uploadError.textContent = message;
        uploadError.hidden = false;
        uploadStatus.textContent = "";
    }

    // ========================================================
    // 3. FILE VALIDATION
    // ========================================================

    function showFile(file) {
        clearMessages();

        if (!file) {
            fileName.textContent = "";
            return;
        }

        const extension = file.name.split(".").pop().toLowerCase();

        if (!["pdf", "docx"].includes(extension)) {
            fileInput.value = "";
            fileName.textContent = "";

            showError("Please select a PDF or DOCX resume.");
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            fileInput.value = "";
            fileName.textContent = "";

            showError("The resume must be 5 MB or smaller.");
            return;
        }

        fileName.textContent =
            `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    }

    fileInput.addEventListener("change", () => {
        showFile(fileInput.files[0]);
    });

    // ========================================================
    // 4. DRAG AND DROP
    // ========================================================

    if (dropZone) {
        ["dragenter", "dragover"].forEach((name) => {
            dropZone.addEventListener(name, (event) => {
                event.preventDefault();
                dropZone.classList.add("drag-over");
            });
        });

        ["dragleave", "drop"].forEach((name) => {
            dropZone.addEventListener(name, (event) => {
                event.preventDefault();
                dropZone.classList.remove("drag-over");
            });
        });

        dropZone.addEventListener("drop", (event) => {
            const file = event.dataTransfer.files[0];

            if (!file) return;

            const transfer = new DataTransfer();
            transfer.items.add(file);

            fileInput.files = transfer.files;

            showFile(file);
        });
    }

    // ========================================================
    // 5. DISPLAY LISTS SAFELY
    // ========================================================

    function displayList(elementId, items, emptyMessage) {
        const list = document.querySelector(`#${elementId}`);

        if (!list) return;

        list.replaceChildren();

        if (!Array.isArray(items) || items.length === 0) {
            const item = document.createElement("li");

            item.textContent = emptyMessage;
            list.appendChild(item);

            return;
        }

        items.forEach((value) => {
            const item = document.createElement("li");

            item.textContent =
                typeof value === "string"
                    ? value
                    : JSON.stringify(value);

            list.appendChild(item);
        });
    }

    // ========================================================
    // 6. DISPLAY ATS TAGS
    // ========================================================

    function displayTags(elementId, items, emptyMessage) {
        const container = document.querySelector(`#${elementId}`);

        if (!container) return;

        container.replaceChildren();

        if (!Array.isArray(items) || items.length === 0) {
            const tag = document.createElement("span");

            tag.className = "ats-tag";
            tag.textContent = emptyMessage;

            container.appendChild(tag);
            return;
        }

        items.forEach((value) => {
            const tag = document.createElement("span");

            tag.className = "ats-tag";
            tag.textContent = String(value);

            container.appendChild(tag);
        });
    }

    // ========================================================
    // 7. DISPLAY ATS RECOMMENDATIONS
    // ========================================================

    function displayRecommendations(recommendations) {
        const list = document.querySelector("#atsRecommendations");

        if (!list) return;

        list.replaceChildren();

        if (
            !Array.isArray(recommendations) ||
            recommendations.length === 0
        ) {
            const item = document.createElement("li");

            item.className = "recommendation-card";
            item.textContent =
                "No additional recommendations were generated. " +
                "Review your ATS checklist and missing skills.";

            list.appendChild(item);
            return;
        }

        const priorityOrder = {
            High: 0,
            Medium: 1,
            Low: 2
        };

        const sortedRecommendations = [...recommendations].sort(
            (a, b) =>
                (priorityOrder[a.priority] ?? 1) -
                (priorityOrder[b.priority] ?? 1)
        );

        sortedRecommendations.forEach((recommendation) => {
            const item = document.createElement("li");

            item.className = "recommendation-card";

            const heading = document.createElement("div");
            heading.className = "recommendation-heading";

            const priorityValue = ["High", "Medium", "Low"].includes(
                recommendation.priority
            )
                ? recommendation.priority
                : "Medium";

            const priority = document.createElement("span");

            priority.className =
                "recommendation-priority " +
                priorityValue.toLowerCase();

            priority.textContent = priorityValue + " Priority";

            const title = document.createElement("h4");

            title.textContent =
                recommendation.title || "Resume improvement";

            heading.append(priority, title);

            const description = document.createElement("p");

            description.textContent =
                recommendation.description ||
                "Review this area of your resume.";

            const action = document.createElement("p");
            action.className = "recommendation-action";

            const actionLabel = document.createElement("strong");

            actionLabel.textContent = "Recommended action: ";

            action.append(
                actionLabel,
                document.createTextNode(
                    recommendation.action ||
                    "Review and improve this area where relevant."
                )
            );

            item.append(heading, description, action);

            list.appendChild(item);
        });
    }

    // ========================================================
    // 8. DISPLAY ATS REPORT
    // ========================================================

    function displayATSReport(result) {
        const ats = result.ats_analysis;

        const scoreElement = document.querySelector("#atsScore");
        const scoreLabel = document.querySelector("#atsScoreLabel");
        const progress = document.querySelector("#atsProgress");
        const progressFill = document.querySelector("#atsProgressFill");

        if (!ats || typeof ats !== "object") {
            scoreElement.textContent = "—";
            scoreLabel.textContent = "ATS result unavailable";

            progress.setAttribute("aria-valuenow", "0");
            progressFill.style.width = "0%";

            document.querySelector("#atsSummary").textContent =
                "ATS feedback was not included in this response.";

            document.querySelector("#atsWordCount").textContent = "—";
            document.querySelector("#atsPassedCount").textContent = "—";
            document.querySelector("#atsFailedCount").textContent = "—";

            displayList(
                "atsChecks",
                [],
                "ATS checks are unavailable."
            );

            displayList(
                "atsSuggestions",
                [],
                "No suggestions are available."
            );

            displayRecommendations([]);

            displayTags("atsSections", [], "Not available");
            displayTags("atsActionVerbs", [], "Not available");

            return;
        }

        const rawScore = Number(ats.ats_score);

        const validScore = Number.isFinite(rawScore)
            ? Math.max(0, Math.min(100, rawScore))
            : null;

        scoreElement.textContent =
            validScore === null
                ? "—"
                : String(validScore);

        progressFill.style.width =
            validScore === null
                ? "0%"
                : `${validScore}%`;

        progress.setAttribute(
            "aria-valuenow",
            validScore === null
                ? "0"
                : String(validScore)
        );

        if (validScore === null) {
            scoreLabel.textContent = "Score unavailable";
        } else if (validScore >= 80) {
            scoreLabel.textContent = "Strong checklist result";
        } else if (validScore >= 60) {
            scoreLabel.textContent =
                "Some improvements recommended";
        } else {
            scoreLabel.textContent =
                "Several improvements recommended";
        }

        const checks = Array.isArray(ats.checks)
            ? ats.checks
            : [];

        const passedCount = checks.filter(
            (check) => check.passed === true
        ).length;

        const failedCount = checks.length - passedCount;

        document.querySelector("#atsSummary").textContent =
            `${passedCount} of ${checks.length} ATS checks passed.`;

        document.querySelector("#atsWordCount").textContent =
            Number.isFinite(Number(ats.word_count))
                ? String(ats.word_count)
                : "—";

        document.querySelector("#atsPassedCount").textContent =
            String(passedCount);

        document.querySelector("#atsFailedCount").textContent =
            String(failedCount);

        const checksList = document.querySelector("#atsChecks");

        checksList.replaceChildren();

        if (checks.length === 0) {
            const item = document.createElement("li");

            item.textContent = "No individual checks were returned.";

            checksList.appendChild(item);
        } else {
            checks.forEach((check) => {
                const item = document.createElement("li");

                item.className = check.passed
                    ? "ats-check-item passed"
                    : "ats-check-item failed";

                const details = document.createElement("div");

                const name = document.createElement("span");

                name.className = "ats-check-name";
                name.textContent = check.name || "Resume check";

                const status = document.createElement("span");

                status.className = "ats-check-status";
                status.textContent = check.passed
                    ? "✓ Passed"
                    : "✕ Needs improvement";

                details.append(name, status);

                const points = document.createElement("span");

                points.className = "ats-check-points";

                const possiblePoints = Number(check.points) || 0;

                const earnedPoints =
                    check.earned_points !== undefined
                        ? Number(check.earned_points) || 0
                        : check.passed
                            ? possiblePoints
                            : 0;

                points.textContent =
                    `${earnedPoints}/${possiblePoints} points`;

                item.append(details, points);

                checksList.appendChild(item);
            });
        }

        displayList(
            "atsSuggestions",
            ats.suggestions,
            "No improvement suggestions were returned."
        );

        displayRecommendations(ats.recommendations);

        displayTags(
            "atsSections",
            ats.sections_found,
            "No standard sections detected"
        );

        displayTags(
            "atsActionVerbs",
            ats.action_verbs_found,
            "No action verbs detected"
        );
    }

    // ========================================================
    // 9. PHASE 8: SKILL GAP ANALYSIS
    // ========================================================

    function displayGapAnalysis(result) {
        /*
         * Create the gap-analysis section dynamically.
         * This means you do not need to modify analyze.html.
         */

        let section = document.querySelector("#skillGapAnalysis");

        if (!section) {
            section = document.createElement("section");

            section.id = "skillGapAnalysis";
            section.className = "analysis-card";

            resultsSection.appendChild(section);
        }

        section.replaceChildren();

        // Section heading.
        const heading = document.createElement("h2");

        heading.textContent = "Skill Gap Analysis";

        const description = document.createElement("p");

        description.textContent =
            "Identify the skills you need to develop for this job.";

        section.append(heading, description);

        // Summary.
        const missingSkills = Array.isArray(result.missing_skills)
            ? result.missing_skills
            : [];

        const totalMissing = Number.isFinite(
            Number(result.total_missing_skills)
        )
            ? Number(result.total_missing_skills)
            : missingSkills.length;

        const summary = document.createElement("div");

        summary.className = "skill-gap-summary";

        const summaryText = document.createElement("p");

        summaryText.textContent =
            `Total skills to develop: ${totalMissing}`;

        summary.appendChild(summaryText);
        section.appendChild(summary);

        // Matched skills.
        const matchedHeading = document.createElement("h3");

        matchedHeading.textContent = "Matched Skills";

        section.appendChild(matchedHeading);

        const matchedSkills = Array.isArray(result.matched_skills)
            ? result.matched_skills
            : [];

        if (matchedSkills.length > 0) {
            const matchedList = document.createElement("ul");

            matchedList.className = "matched-skill-list";

            matchedSkills.forEach((skill) => {
                const item = document.createElement("li");

                item.textContent = `✓ ${skill}`;

                matchedList.appendChild(item);
            });

            section.appendChild(matchedList);
        } else {
            const message = document.createElement("p");

            message.textContent =
                "No matching recognized skills were detected.";

            section.appendChild(message);
        }

        // Missing skills heading.
        const missingHeading = document.createElement("h3");

        missingHeading.textContent = "Missing Skills";

        section.appendChild(missingHeading);

        if (missingSkills.length > 0) {
            const missingList = document.createElement("ul");

            missingList.className = "missing-skill-list";

            missingSkills.forEach((skill) => {
                const item = document.createElement("li");

                item.textContent = String(skill);

                missingList.appendChild(item);
            });

            section.appendChild(missingList);
        } else {
            const message = document.createElement("p");

            message.textContent =
                "No missing recognized skills were detected.";

            section.appendChild(message);
        }

        // Skills grouped by priority.
        const priorityHeading = document.createElement("h3");

        priorityHeading.textContent = "Priority Breakdown";

        section.appendChild(priorityHeading);

        const priorityData =
            result.missing_skills_by_priority || {};

        const priorities = [
            {
                name: "High",
                skills: Array.isArray(priorityData.High)
                    ? priorityData.High
                    : []
            },
            {
                name: "Medium",
                skills: Array.isArray(priorityData.Medium)
                    ? priorityData.Medium
                    : []
            },
            {
                name: "Low",
                skills: Array.isArray(priorityData.Low)
                    ? priorityData.Low
                    : []
            }
        ];

        priorities.forEach((priorityItem) => {
            const group = document.createElement("div");

            group.className =
                `skill-priority-group priority-${priorityItem.name.toLowerCase()}`;

            const groupHeading = document.createElement("h4");

            groupHeading.textContent =
                `${priorityItem.name} Priority`;

            group.appendChild(groupHeading);

            if (priorityItem.skills.length > 0) {
                const list = document.createElement("ul");

                priorityItem.skills.forEach((skill) => {
                    const item = document.createElement("li");

                    item.textContent = String(skill);

                    list.appendChild(item);
                });

                group.appendChild(list);
            } else {
                const message = document.createElement("p");

                message.textContent =
                    `No ${priorityItem.name.toLowerCase()}-priority gaps identified.`;

                group.appendChild(message);
            }

            section.appendChild(group);
        });

        // Individual skill learning suggestions.
        const learningHeading = document.createElement("h3");

        learningHeading.textContent = "Learning Suggestions";

        section.appendChild(learningHeading);

        const skillGaps = Array.isArray(result.skill_gaps)
            ? result.skill_gaps
            : [];

        if (skillGaps.length > 0) {
            skillGaps.forEach((gap) => {
                const card = document.createElement("article");

                card.className = "skill-learning-card";

                const skillHeading = document.createElement("h4");

                skillHeading.textContent =
                    gap.skill || "Missing skill";

                const priority = document.createElement("p");

                const priorityValue = [
                    "High",
                    "Medium",
                    "Low"
                ].includes(gap.priority)
                    ? gap.priority
                    : "Not specified";

                priority.textContent =
                    `Priority: ${priorityValue}`;

                const suggestion = document.createElement("p");

                suggestion.textContent =
                    gap.learning_suggestion ||
                    gap.suggestion ||
                    "Practise this skill using relevant exercises and projects.";

                card.append(
                    skillHeading,
                    priority,
                    suggestion
                );

                section.appendChild(card);
            });
        } else if (missingSkills.length > 0) {
            /*
             * Fallback for cases where missing_skills is available
             * but skill_gaps does not contain learning suggestions.
             */

            const message = document.createElement("p");

            message.textContent =
                "Skill gaps were detected, but no individual learning " +
                "suggestions were returned. Review the priority breakdown.";

            section.appendChild(message);
        } else {
            const message = document.createElement("p");

            message.textContent =
                "You have no identified skill gaps for the recognized " +
                "skills in this job description.";

            section.appendChild(message);
        }

        // Explain how to interpret the analysis.
        const note = document.createElement("p");

        note.className = "skill-gap-note";

        note.textContent =
            "These results are based on recognized keywords in your " +
            "resume and the job description. A missing keyword does not " +
            "necessarily mean you lack that skill.";

        section.appendChild(note);
    }

    // ========================================================
    // 10. DISPLAY COMPLETE ANALYSIS RESULTS
    // ========================================================

    function displayResults(result) {
        document.querySelector("#resultJobTitle").textContent =
            result.company_name
                ? `${result.job_title} at ${result.company_name}`
                : result.job_title;

        const matchScore = Number(result.match_score);

        document.querySelector("#matchScore").textContent =
            Number.isFinite(matchScore)
                ? `${matchScore.toFixed(2)}%`
                : "Unavailable";

        document.querySelector("#matchedSummary").textContent =
            `${result.total_matched_skills ?? 0} of ` +
            `${result.total_required_skills ?? 0} recognized job skills matched.`;

        displayList(
            "matchedSkills",
            result.matched_skills,
            "No matching skills detected."
        );

        displayList(
            "missingSkills",
            result.missing_skills,
            "No missing recognized skills detected."
        );

        displayList(
            "resumeSkills",
            result.resume_skills,
            "No recognized skills detected in the resume."
        );

        document.querySelector("#noSkillsMessage").hidden =
            Number(result.total_required_skills || 0) !== 0;

        // Existing ATS report.
        displayATSReport(result);

        // New Phase 8 gap analysis.
        displayGapAnalysis(result);

        resultsSection.hidden = false;

        resultsSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
    // ========================================================
// 11. RESUME IMPROVEMENT ASSISTANT — PHASE 9
// ========================================================

const improveButton = document.querySelector("#improveResumeBtn");

const improvementStatus = document.querySelector("#improvementStatus");

const improvementResults = document.querySelector("#improvementResults");

const improvementRecommendations = document.querySelector(
    "#improvementRecommendations"
);

const improvedBulletPoints = document.querySelector(
    "#improvedBulletPoints"
);


// --------------------------------------------------------
// HELPER: CREATE ELEMENTS SAFELY
// --------------------------------------------------------

function createImprovementElement(tag, className, text = "") {
    const element = document.createElement(tag);

    if (className) {
        element.className = className;
    }

    element.textContent = text;

    return element;
}


// --------------------------------------------------------
// HELPER: DISPLAY IMPROVEMENT SUMMARY
// --------------------------------------------------------

function displayImprovementSummary(data) {
    const summary = data.summary || {};

    const recommendationCount = Number.isFinite(
        Number(summary.recommendation_count)
    )
        ? Number(summary.recommendation_count)
        : (Array.isArray(data.recommendations)
            ? data.recommendations.length
            : 0);

    const bulletCount = Number.isFinite(
        Number(summary.bullet_improvement_count)
    )
        ? Number(summary.bullet_improvement_count)
        : (Array.isArray(data.bullet_improvements)
            ? data.bullet_improvements.length
            : 0);

    const keywordCount = Number.isFinite(
        Number(summary.missing_keyword_count)
    )
        ? Number(summary.missing_keyword_count)
        : (Array.isArray(data.missing_keywords)
            ? data.missing_keywords.length
            : 0);

    let summaryContainer = document.querySelector(
        "#improvementSummary"
    );

    if (!summaryContainer) {
        summaryContainer = document.createElement("div");
        summaryContainer.id = "improvementSummary";

        improvementResults.prepend(summaryContainer);
    }

    summaryContainer.replaceChildren();
    summaryContainer.className = "improvement-summary";

    const summaryItems = [
        {
            label: "Recommendations",
            value: recommendationCount,
            className: "recommendation-stat"
        },
        {
            label: "Bullet Suggestions",
            value: bulletCount,
            className: "bullet-stat"
        },
        {
            label: "Missing Keywords",
            value: keywordCount,
            className: "keyword-stat"
        }
    ];

    summaryItems.forEach((item) => {
        const card = document.createElement("article");

        card.className =
            `improvement-stat-card ${item.className}`;

        const value = createImprovementElement(
            "strong",
            "improvement-stat-value",
            String(item.value)
        );

        const label = createImprovementElement(
            "span",
            "improvement-stat-label",
            item.label
        );

        card.append(value, label);

        summaryContainer.appendChild(card);
    });
}


// --------------------------------------------------------
// HELPER: DISPLAY RECOMMENDATIONS
// --------------------------------------------------------

function displayImprovementRecommendations(recommendations) {
    improvementRecommendations.replaceChildren();

    if (
        !Array.isArray(recommendations) ||
        recommendations.length === 0
    ) {
        const message = createImprovementElement(
            "p",
            "improvement-empty-state",
            "No additional recommendations were generated."
        );

        improvementRecommendations.appendChild(message);
        return;
    }

    const priorityOrder = {
        High: 0,
        Medium: 1,
        Low: 2
    };

    const sortedRecommendations = [...recommendations].sort(
        (a, b) => {
            const priorityA = priorityOrder[a.priority] ?? 1;
            const priorityB = priorityOrder[b.priority] ?? 1;

            return priorityA - priorityB;
        }
    );

    sortedRecommendations.forEach((item) => {
        const card = document.createElement("article");

        card.className = "improvement-card";

        const heading = document.createElement("div");

        heading.className = "improvement-card-heading";

        const title = createImprovementElement(
            "h4",
            "improvement-card-title",
            item.title || "Resume recommendation"
        );

        const priorityValue = ["High", "Medium", "Low"].includes(
            item.priority
        )
            ? item.priority
            : "Medium";

        const priority = createImprovementElement(
            "span",
            `improvement-priority ${priorityValue.toLowerCase()}`,
            `${priorityValue} Priority`
        );

        heading.append(title, priority);

        const description = createImprovementElement(
            "p",
            "improvement-description",
            item.description || "Review this area of your resume."
        );

        const actionBox = document.createElement("div");

        actionBox.className = "improvement-action-box";

        const actionLabel = createImprovementElement(
            "strong",
            "",
            "Recommended action"
        );

        const actionText = createImprovementElement(
            "p",
            "",
            item.action ||
                "Review and improve this area where relevant."
        );

        actionBox.append(actionLabel, actionText);

        card.append(heading, description, actionBox);

        improvementRecommendations.appendChild(card);
    });
}


// --------------------------------------------------------
// HELPER: COPY TEXT TO CLIPBOARD
// --------------------------------------------------------

async function copyImprovedText(text, button) {
    const originalLabel = button.textContent;

    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            // Fallback for browsers where Clipboard API is unavailable.
            const temporaryInput = document.createElement("textarea");

            temporaryInput.value = text;
            temporaryInput.setAttribute("readonly", "");
            temporaryInput.style.position = "fixed";
            temporaryInput.style.left = "-9999px";

            document.body.appendChild(temporaryInput);

            temporaryInput.select();

            const copied = document.execCommand("copy");

            temporaryInput.remove();

            if (!copied) {
                throw new Error("Copy operation failed.");
            }
        }

        button.textContent = "Copied!";
        button.classList.add("copy-success");

    } catch (error) {
        console.error("Could not copy improved text:", error);

        button.textContent = "Copy failed";
    }

    button.disabled = true;

    window.setTimeout(() => {
        button.textContent = originalLabel;
        button.disabled = false;
        button.classList.remove("copy-success");
    }, 1600);
}


// --------------------------------------------------------
// HELPER: DISPLAY BEFORE-AND-AFTER BULLET POINTS
// --------------------------------------------------------

function displayImprovedBullets(bulletImprovements) {
    improvedBulletPoints.replaceChildren();

    if (
        !Array.isArray(bulletImprovements) ||
        bulletImprovements.length === 0
    ) {
        const emptyState = document.createElement("div");

        emptyState.className = "improvement-empty-state";

        const title = createImprovementElement(
            "h4",
            "",
            "Your bullet points look good!"
        );

        const description = createImprovementElement(
            "p",
            "",
            "No suitable automatic wording changes were identified. " +
            "You can still improve your resume by adding specific " +
            "contributions, relevant tools, and genuine results."
        );

        emptyState.append(title, description);

        improvedBulletPoints.appendChild(emptyState);
        return;
    }

    bulletImprovements.forEach((item, index) => {
        const card = document.createElement("article");

        card.className = "improvement-card bullet-comparison-card";

        // Card heading.
        const heading = createImprovementElement(
            "h4",
            "bullet-comparison-title",
            `Bullet Point ${index + 1}`
        );

        // Before-and-after layout.
        const comparison = document.createElement("div");

        comparison.className = "bullet-comparison-grid";

        // Original text.
        const originalBox = document.createElement("div");

        originalBox.className = "bullet-version original-version";

        const originalLabel = createImprovementElement(
            "span",
            "bullet-version-label",
            "BEFORE"
        );

        const originalText = createImprovementElement(
            "p",
            "bullet-version-text",
            item.original || "Original text unavailable."
        );

        originalBox.append(originalLabel, originalText);

        // Improved text.
        const improvedBox = document.createElement("div");

        improvedBox.className = "bullet-version improved-version";

        const improvedLabel = createImprovementElement(
            "span",
            "bullet-version-label",
            item.changed === false
                ? "SUGGESTION"
                : "AFTER"
        );

        const improvedText = createImprovementElement(
            "p",
            "bullet-version-text",
            item.improved || item.original || ""
        );

        improvedBox.append(improvedLabel, improvedText);

        comparison.append(originalBox, improvedBox);

        // Explanation.
        const reasonBox = document.createElement("div");

        reasonBox.className = "bullet-improvement-reason";

        const reasonLabel = createImprovementElement(
            "strong",
            "",
            "Why this suggestion?"
        );

        const reasonText = createImprovementElement(
            "p",
            "",
            item.reason || "Review the wording for clarity."
        );

        reasonBox.append(reasonLabel, reasonText);

        card.append(heading, comparison, reasonBox);

        // Add copy button only when a distinct version exists.
        if (
            item.improved &&
            item.improved !== item.original
        ) {
            const actions = document.createElement("div");

            actions.className = "bullet-card-actions";

            const copyButton = createImprovementElement(
                "button",
                "copy-improved-button",
                "Copy improved text"
            );

            copyButton.type = "button";

            copyButton.addEventListener("click", async () => {
                await copyImprovedText(
                    item.improved,
                    copyButton
                );
            });

            actions.appendChild(copyButton);

            card.appendChild(actions);
        }

        improvedBulletPoints.appendChild(card);
    });
}


// --------------------------------------------------------
// HELPER: DISPLAY MISSING SKILLS AND KEYWORDS
// --------------------------------------------------------

function displayMissingKeywords(missingKeywords, missingSkills) {
    let section = document.querySelector(
        "#improvementMissingKeywords"
    );

    if (!section) {
        section = document.createElement("section");

        section.id = "improvementMissingKeywords";
        section.className = "improvement-keywords-section";

        improvementResults.appendChild(section);
    }

    section.replaceChildren();

    const heading = createImprovementElement(
        "h3",
        "improvement-section-title",
        "Job Description Keyword Analysis"
    );

    const description = createImprovementElement(
        "p",
        "improvement-section-description",
        "Review these terms to see whether they accurately reflect " +
        "your existing skills and experience."
    );

    section.append(heading, description);

    // Normalize both the newer object format and string arrays.
    const keywordItems = Array.isArray(missingKeywords)
        ? missingKeywords
        : [];

    const normalizedItems = keywordItems.map((item) => {
        if (typeof item === "string") {
            return {
                keyword: item,
                type: "keyword",
                reason: "Review whether this term applies to your experience."
            };
        }

        return {
            keyword: String(item.keyword || ""),
            type: item.type === "skill" ? "skill" : "keyword",
            reason: item.reason ||
                "Review whether this term applies to your experience."
        };
    }).filter((item) => item.keyword);

    // Include missing skills from the analysis response if needed.
    const existingKeywords = new Set(
        normalizedItems.map((item) => item.keyword.toLowerCase())
    );

    if (Array.isArray(missingSkills)) {
        missingSkills.forEach((skill) => {
            const name = String(skill);

            if (!existingKeywords.has(name.toLowerCase())) {
                normalizedItems.push({
                    keyword: name,
                    type: "skill",
                    reason:
                        "This skill was not detected in your resume " +
                        "during the job-description comparison."
                });

                existingKeywords.add(name.toLowerCase());
            }
        });
    }

    if (normalizedItems.length === 0) {
        const successMessage = createImprovementElement(
            "div",
            "keyword-success-message",
            "No missing keywords were identified by this analysis."
        );

        section.appendChild(successMessage);
        return;
    }

    const keywordSummary = createImprovementElement(
        "p",
        "keyword-count",
        `${normalizedItems.length} term(s) to review`
    );

    section.appendChild(keywordSummary);

    const keywordGrid = document.createElement("div");

    keywordGrid.className = "improvement-keyword-grid";

    normalizedItems.forEach((item) => {
        const card = document.createElement("article");

        card.className = "improvement-keyword-card";

        const badge = createImprovementElement(
            "span",
            `keyword-type-badge ${item.type}`,
            item.type === "skill" ? "SKILL" : "KEYWORD"
        );

        const name = createImprovementElement(
            "h4",
            "improvement-keyword-name",
            item.keyword
        );

        const reason = createImprovementElement(
            "p",
            "improvement-keyword-reason",
            item.reason
        );

        card.append(badge, name, reason);

        keywordGrid.appendChild(card);
    });

    section.appendChild(keywordGrid);

    const note = createImprovementElement(
        "p",
        "improvement-keyword-note",
        "Important: A missing term does not necessarily mean you lack " +
        "that skill. Include it only if it accurately represents your " +
        "skills, projects, education, or experience."
    );

    section.appendChild(note);
}


// --------------------------------------------------------
// MAIN: RUN RESUME IMPROVEMENT ANALYSIS
// --------------------------------------------------------

if (improveButton) {
    improveButton.addEventListener("click", async () => {
        if (!latestResumeText) {
            improvementStatus.textContent =
                "Please analyze your resume first.";

            return;
        }

        improveButton.disabled = true;

        improveButton.textContent = "Improving Resume...";

        improvementStatus.textContent =
            "Analyzing your resume and identifying improvements...";

        improvementResults.hidden = true;

        try {
            const response = await fetch("/api/improve-resume", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    resume_text: latestResumeText,
                    job_description: jobDescription.value.trim(),
                    job_title: jobTitle.value.trim()
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to improve your resume."
                );
            }

            // Display summary cards.
            displayImprovementSummary(data);

            // Display recommendations.
            displayImprovementRecommendations(
                data.recommendations
            );

            // Display original and improved bullet points.
            displayImprovedBullets(
                data.bullet_improvements
            );

            // Display missing skills and keywords.
            displayMissingKeywords(
                data.missing_keywords,
                data.missing_skills
            );

            // Reveal results.
            improvementResults.hidden = false;

            improvementStatus.textContent =
                "Resume improvement analysis completed. " +
                "Review each suggestion before using it.";

            improvementResults.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        } catch (error) {
            console.error(
                "Resume improvement error:",
                error
            );

            improvementStatus.textContent =
                error.message ||
                "Something went wrong. Please try again.";

        } finally {
            improveButton.disabled = false;

            improveButton.textContent = "Improve My Resume";
        }
    });
}
// ========================================================
// PHASE 10: RESUME READINESS SCORE
// ========================================================

function getReadinessComponentScore(result, componentName) {
    const component = result[componentName];

    // The component may be a number.
    if (typeof component === "number") {
        return component;
    }

    // Or it may be an object containing a score.
    if (component && typeof component === "object") {
        const score = Number(
            component.score ??
            component.value ??
            component.percentage
        );

        if (Number.isFinite(score)) {
            return score;
        }
    }

    // Fall back to the components object.
    const components = result.components || {};
    const fallback = components[componentName];

    if (typeof fallback === "number") {
        return fallback;
    }

    if (fallback && typeof fallback === "object") {
        const score = Number(
            fallback.score ??
            fallback.value ??
            fallback.percentage
        );

        if (Number.isFinite(score)) {
            return score;
        }
    }

    return null;
}


function setReadinessProgress(elementId, score) {
    const element = document.querySelector(`#${elementId}`);

    if (!element) return;

    const validScore =
        Number.isFinite(score)
            ? Math.max(0, Math.min(100, score))
            : 0;

    element.style.width = `${validScore}%`;
}


function displayReadinessFeedback(feedback) {
    const container = document.querySelector("#readinessFeedback");

    if (!container) return;

    container.replaceChildren();

    if (!Array.isArray(feedback) || feedback.length === 0) {
        const message = document.createElement("p");

        message.className = "readiness-empty";
        message.textContent =
            "No specific recommendations were returned.";

        container.appendChild(message);
        return;
    }

    feedback.forEach((item) => {
        const card = document.createElement("article");

        card.className = "readiness-feedback-card";

        // Support either a plain string or an object.
        if (typeof item === "string") {
            card.textContent = item;
        } else {
            const heading = document.createElement("h4");
            heading.textContent =
                item.title || item.category || "Recommendation";

            const description = document.createElement("p");
            description.textContent =
                item.description ||
                item.message ||
                item.action ||
                item.feedback ||
                "Review this area of your resume.";

            card.append(heading, description);
        }

        container.appendChild(card);
    });
}


function displayReadinessMissingSkills(result) {
    const container = document.querySelector("#readinessMissingSkills");

    if (!container) return;

    container.replaceChildren();

    const keywordCoverage = result.keyword_coverage || {};
    const components = result.components || {};
    const componentCoverage = components.keyword_coverage || {};

    const missingSkills =
        keywordCoverage.missing_skills ||
        keywordCoverage.missing_keywords ||
        componentCoverage.missing_skills ||
        componentCoverage.missing_keywords ||
        result.missing_skills ||
        [];

    if (!Array.isArray(missingSkills) || missingSkills.length === 0) {
        const message = document.createElement("p");

        message.className = "readiness-empty";
        message.textContent =
            "No missing skills were returned, or no job-specific " +
            "keywords could be assessed.";

        container.appendChild(message);
        return;
    }

    missingSkills.forEach((skill) => {
        const tag = document.createElement("span");

        tag.className = "readiness-keyword";

        // Support strings and objects.
        tag.textContent =
            typeof skill === "string"
                ? skill
                : String(skill.skill || skill.keyword || skill.name || "");

        container.appendChild(tag);
    });
}


function displayResumeReadiness(result) {
    const section = document.querySelector("#resumeReadinessSection");

    if (!section) {
        console.warn("Resume Readiness HTML section was not found.");
        return;
    }

    const rawScore = Number(result.readiness_score);

    const score = Number.isFinite(rawScore)
        ? Math.max(0, Math.min(100, rawScore))
        : null;

    // Overall score.
    document.querySelector("#readinessScore").textContent =
        score === null ? "—" : String(score);

    document.querySelector("#readinessDescription").textContent =
        result.score_basis ||
        "This score estimates your resume's content quality and job alignment.";

    setReadinessProgress("readinessProgress", score);

    // Overall score label.
    const label = document.querySelector("#readinessLabel");

    if (score === null) {
        label.textContent = "Score unavailable";
    } else if (score >= 80) {
        label.textContent = "Strong resume readiness";
    } else if (score >= 60) {
        label.textContent = "Good starting point";
    } else {
        label.textContent = "Improvements recommended";
    }

    // Component scores.
    const contentScore = getReadinessComponentScore(
        result,
        "content_quality"
    );

    const relevanceScore = getReadinessComponentScore(
        result,
        "job_relevance"
    );

    const keywordScore = getReadinessComponentScore(
        result,
        "keyword_coverage"
    );

    document.querySelector("#contentQualityScore").textContent =
        contentScore === null ? "N/A" : `${contentScore}/100`;

    document.querySelector("#jobRelevanceScore").textContent =
        relevanceScore === null ? "N/A" : `${relevanceScore}/100`;

    document.querySelector("#keywordCoverageScore").textContent =
        keywordScore === null ? "N/A" : `${keywordScore}/100`;

    setReadinessProgress("contentQualityProgress", contentScore);
    setReadinessProgress("jobRelevanceProgress", relevanceScore);
    setReadinessProgress("keywordCoverageProgress", keywordScore);

    // Feedback and missing skills.
    displayReadinessFeedback(result.feedback);
    displayReadinessMissingSkills(result);

    // Use the backend disclaimer if available.
    const disclaimer = document.querySelector("#readinessDisclaimer");

    if (disclaimer && result.disclaimer) {
        disclaimer.textContent = result.disclaimer;
    }

    // Show the section now that results are available.
    section.hidden = false;
}


async function runResumeReadiness(resumeTextValue, jobDescriptionValue) {
    const section = document.querySelector("#resumeReadinessSection");

    if (!section) {
        console.warn("Resume Readiness section is missing from analyze.html.");
        return;
    }

    section.hidden = true;

    try {
        const response = await fetch("/api/resume-readiness", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                resume_text: resumeTextValue,
                job_description: jobDescriptionValue
            })
        });

        const data = await response.json();

        if (!response.ok || data.success === false) {
            throw new Error(
                data.error || "Unable to calculate resume readiness."
            );
        }

        displayResumeReadiness(data);

    } catch (error) {
        console.error("Resume Readiness error:", error);

        section.hidden = false;

        document.querySelector("#readinessScore").textContent = "—";

        document.querySelector("#readinessLabel").textContent =
            "Assessment unavailable";

        document.querySelector("#readinessDescription").textContent =
            "The readiness score could not be calculated. " +
            "Your other analysis results are still available.";
    }
}

    // ========================================================
    // 12. SUBMIT FORM AND RUN ANALYSIS
    // ========================================================

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        clearMessages();

        resultsSection.hidden = true;

        if (!form.reportValidity()) return;

        const title = jobTitle.value.trim();
        const description = jobDescription.value.trim();

        if (!title || !description) {
            showError(
                "Please enter the job title and job description."
            );

            return;
        }

        let actualResumeText = "";
        let uploadedFileName = "pasted_resume.txt";

        generateButton.disabled = true;

        try {
            if (activeMode === "upload") {
                const file = fileInput.files[0];

                if (!file) {
                    showError("Please select a resume file.");
                    return;
                }

                const extension =
                    file.name.split(".").pop().toLowerCase();

                if (!["pdf", "docx"].includes(extension)) {
                    showError(
                        "Only PDF and DOCX files are supported."
                    );

                    return;
                }

                if (file.size > 5 * 1024 * 1024) {
                    showError(
                        "The resume must be 5 MB or smaller."
                    );

                    return;
                }

                uploadedFileName = file.name;

                const formData = new FormData();

                formData.append("resume", file);

                generateButton.textContent = "Reading Resume...";

                uploadStatus.textContent =
                    "Uploading and extracting your resume...";

                const parseResponse = await fetch(
                    "/api/resume/parse",
                    {
                        method: "POST",
                        body: formData
                    }
                );

                const parsed = await parseResponse.json();

                if (!parseResponse.ok) {
                    throw new Error(
                        parsed.error || "Resume parsing failed."
                    );
                }

                actualResumeText =
                    String(parsed.resume_text || "").trim();

                if (!actualResumeText) {
                    throw new Error(
                        "No readable text was found in this resume. " +
                        "Try another PDF or DOCX file."
                    );
                }

            } else {
                actualResumeText = resumeText.value.trim();

                if (actualResumeText.length < 30) {
                    showError(
                        "Please enter at least 30 characters " +
                        "of resume content."
                    );

                    return;
                }
            }

            generateButton.textContent = "Analyzing...";

            uploadStatus.textContent =
                "Comparing your resume with the job requirements " +
                "and checking ATS readiness...";

            const analysisResponse = await fetch(
                "/api/analyze",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        resume_text: actualResumeText,
                        resume_file_name: uploadedFileName,
                        job_title: title,
                        company_name: companyName.value.trim(),
                        job_description: description
                    })
                }
            );

            const result = await analysisResponse.json();

            if (!analysisResponse.ok) {
                throw new Error(
                    result.error ||
                    "Analysis could not be completed."
                );
            }

            latestResumeText = actualResumeText;

// Display the existing analysis results.
displayResults(result);

// PHASE 10: Calculate the separate Resume Readiness Score.
await runResumeReadiness(
    actualResumeText,
    description
);

uploadStatus.textContent =
    "Analysis completed successfully. " +
    "Your results have been saved.";

        } catch (error) {
            console.error(
                "Resume analysis error:",
                error
            );

            showError(
                error.message || "Something went wrong."
            );

        } finally {
            generateButton.disabled = false;

            generateButton.textContent =
                "Generate Analysis →";
        }
    });

    // ========================================================
// PHASE 5: AI-POWERED JOB RECOMMENDATIONS
// ========================================================

const recommendJobsBtn = document.querySelector("#recommendJobsBtn");

const jobRecommendationsStatus = document.querySelector(
    "#jobRecommendationsStatus"
);

const jobRecommendationsResults = document.querySelector(
    "#jobRecommendationsResults"
);

if (
    recommendJobsBtn &&
    jobRecommendationsStatus &&
    jobRecommendationsResults
) {
    recommendJobsBtn.addEventListener("click", async () => {
        // Check whether a resume has already been analyzed.
        if (
            typeof latestResumeText === "undefined" ||
            !latestResumeText ||
            !latestResumeText.trim()
        ) {
            jobRecommendationsStatus.textContent =
                "Please upload and analyze your resume before requesting job recommendations.";

            jobRecommendationsResults.replaceChildren();
            return;
        }

        recommendJobsBtn.disabled = true;

        jobRecommendationsStatus.textContent =
            "Finding jobs that match your resume skills...";

        jobRecommendationsResults.replaceChildren();

        try {
            // Request recommendations from Flask.
            const response = await fetch("/api/recommend-jobs", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    resume_text: latestResumeText
                })
            });

            // Read the server response.
            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error ||
                    "Unable to retrieve job recommendations."
                );
            }

            // Support common API response formats.
            const jobs = Array.isArray(data)
                ? data
                : Array.isArray(data.recommendations)
                    ? data.recommendations
                    : Array.isArray(data.jobs)
                        ? data.jobs
                        : [];

            if (jobs.length === 0) {
                jobRecommendationsStatus.textContent =
                    "No job recommendations were returned. Please check your resume skills and try again.";

                return;
            }

            // Display each recommendation.
            jobs.forEach((job) => {
                const card = document.createElement("article");
                card.className = "recommended-job-card";

            // Job title.
const title = document.createElement("h3");
title.className = "recommended-job-title";

title.textContent =
    job.job_role ||
    job.title ||
    job.job_title ||
    job.role ||
    job.position ||
    job.name ||
    "Recommended Job";
                
                

                // Company.
                const company = document.createElement("p");
                company.className = "recommended-job-company";

                company.textContent =
                    job.company ||
                    job.company_name ||
                    job.employer ||
                    "Company not specified";

                // Match percentage.
                const rawMatch =
                    job.match_percentage ??
                    job.match_score ??
                    job.match ??
                    job.score;

                const match = document.createElement("p");
                match.className = "recommended-job-match";

                const matchValue = Number(rawMatch);

                if (
                    rawMatch !== undefined &&
                    rawMatch !== null &&
                    rawMatch !== "" &&
                    Number.isFinite(matchValue)
                ) {
                    const percentage = Math.max(
                        0,
                        Math.min(100, matchValue)
                    );

                    match.textContent =
                        `Skill match: ${percentage}%`;
                } else {
                    match.textContent =
                        "Skill match unavailable";
                }

                // Job description.
const description = document.createElement("div");
description.className = "recommended-job-description";

const matchedSkills = Array.isArray(job.matched_skills)
    ? job.matched_skills
    : [];

const missingSkills = Array.isArray(job.missing_skills)
    ? job.missing_skills
    : [];

const learningSuggestions = Array.isArray(job.learning_suggestions)
    ? job.learning_suggestions
    : [];

const matchedText = document.createElement("p");
matchedText.textContent = matchedSkills.length
    ? `Matching skills: ${matchedSkills.join(", ")}`
    : "No matching skills listed.";

description.appendChild(matchedText);

if (missingSkills.length > 0) {
    const missingText = document.createElement("p");
    missingText.textContent =
        `Skills to develop: ${missingSkills.join(", ")}`;

    description.appendChild(missingText);
}

if (learningSuggestions.length > 0) {
    const learningText = document.createElement("p");
    learningText.textContent =
        `Suggested learning: ${learningSuggestions.join(", ")}`;

    description.appendChild(learningText);
}

                // Add elements to the card.
                card.appendChild(title);
                card.appendChild(company);
                card.appendChild(match);
                card.appendChild(description);

                // Add the card to the recommendations section.
                jobRecommendationsResults.appendChild(card);
            });

            jobRecommendationsStatus.textContent =
                `Found ${jobs.length} job recommendation(s).`;

        } catch (error) {
            console.error(
                "Job recommendations error:",
                error
            );

            jobRecommendationsStatus.textContent =
                error.message ||
                "Something went wrong while finding job recommendations.";

        } finally {
            recommendJobsBtn.disabled = false;
        }
    });
}

// ========================================================
// END PHASE 5
// ========================================================




});
