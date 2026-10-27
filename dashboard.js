document.addEventListener("DOMContentLoaded", () => {
    updateDashboardGreeting();

    // ==========================================
    // 1. SIDEBAR
    // ==========================================

    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle");

    menuToggle?.addEventListener("click", () => {
        sidebar?.classList.toggle("open");
    });

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            document.querySelectorAll(".nav-link").forEach(item => {
                item.classList.remove("active");
            });

            link.classList.add("active");
            sidebar?.classList.remove("open");
        });
    });


    // ==========================================
    // 2. SAVED JOBS AND JOB FILTERING
    // ==========================================

    let storedJobs = [];

    try {
        storedJobs = JSON.parse(
            localStorage.getItem("careerfitSavedJobs") || "[]"
        );

        if (!Array.isArray(storedJobs)) {
            storedJobs = [];
        }
    } catch (error) {
        console.error("Could not read saved jobs:", error);
        storedJobs = [];
    }

    const savedJobs = new Set(
        storedJobs.filter(job => typeof job === "string")
    );

    const saveButtons = document.querySelectorAll("[data-save]");
    const savedCount = document.getElementById("savedCount");
    const jobFilter = document.getElementById("jobFilter");
    const jobSearch = document.getElementById("jobSearch");
    const globalSearch = document.getElementById("globalSearch");
    const emptyJobs = document.getElementById("emptyJobs");

    function renderSavedJobs() {
        saveButtons.forEach(button => {
            const isSaved = savedJobs.has(button.dataset.save);

            button.classList.toggle("saved", isSaved);
            button.textContent = isSaved ? "♥" : "♡";

            button.setAttribute(
                "aria-pressed",
                String(isSaved)
            );
        });

        if (savedCount) {
            savedCount.textContent = String(savedJobs.size);
        }

        filterJobs();
    }

    function filterJobs() {
        const query = (
            jobSearch?.value ||
            globalSearch?.value ||
            ""
        ).trim().toLowerCase();

        const onlySaved = jobFilter?.value === "saved";

        let visibleCount = 0;

        document.querySelectorAll(".job-card").forEach(card => {
            const title = (
                card.dataset.title || ""
            ).toLowerCase();

            const text = card.textContent.toLowerCase();

            const saveButton = card.querySelector("[data-save]");
            const id = saveButton?.dataset.save;

            const matchesQuery =
                !query ||
                title.includes(query) ||
                text.includes(query);

            const matchesSaved =
                !onlySaved ||
                (id && savedJobs.has(id));

            const visible = matchesQuery && matchesSaved;

            card.hidden = !visible;

            if (visible) {
                visibleCount++;
            }
        });

        if (emptyJobs) {
            emptyJobs.hidden = visibleCount !== 0;
        }
    }

    saveButtons.forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.save;

            if (!id) {
                return;
            }

            if (savedJobs.has(id)) {
                savedJobs.delete(id);
            } else {
                savedJobs.add(id);
            }

            try {
                localStorage.setItem(
                    "careerfitSavedJobs",
                    JSON.stringify([...savedJobs])
                );
            } catch (error) {
                console.error(
                    "Could not save job preferences:",
                    error
                );
            }

            renderSavedJobs();
        });
    });

    jobFilter?.addEventListener("change", filterJobs);
    jobSearch?.addEventListener("input", filterJobs);
    globalSearch?.addEventListener("input", filterJobs);

    renderSavedJobs();


    // ==========================================
    // 3. DASHBOARD ANALYTICS STATE
    // ==========================================

    let matchScoreChartInstance = null;

    const refreshAnalyticsButton = document.getElementById(
        "refreshAnalytics"
    );

    refreshAnalyticsButton?.addEventListener("click", async () => {
        if (refreshAnalyticsButton.disabled) {
            return;
        }

        refreshAnalyticsButton.disabled = true;
        refreshAnalyticsButton.textContent = "Refreshing...";

        try {
            await loadDashboardData();
        } finally {
            refreshAnalyticsButton.disabled = false;
            refreshAnalyticsButton.textContent = "↻ Refresh";
        }
    });
    
    // ==========================================
// 🌞 DYNAMIC DASHBOARD GREETING
// ==========================================

function updateDashboardGreeting() {
    const currentHour = new Date().getHours();
    let greeting;

    if (currentHour >= 5 && currentHour < 12) {
        greeting = "Good Morning ☀️";
    } else if (currentHour >= 12 && currentHour < 17) {
        greeting = "Good Afternoon 🌤️";
    } else if (currentHour >= 17 && currentHour < 21) {
        greeting = "Good Evening 🌆";
    } else {
        greeting = "Good Night 🌙";
    }

    const greetingElement = document.getElementById("greetingMessage");

    if (greetingElement) {
        greetingElement.textContent = greeting + "!";
    }
}


// ==========================================
// YOUR EXISTING DASHBOARD CODE
// ==========================================

// Keep your existing function below this line.
// Do not replace its contents!

async function loadDashboardData() {
    // Your original code stays here.
}

    // ==========================================
    // 4. LOAD DASHBOARD DATA FROM FLASK / MYSQL
    // ==========================================

    async function loadDashboardData() {
        const statusElement = document.querySelector(
            "[data-dashboard='status']"
        );

        try {
            const response = await fetch("/api/dashboard", {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            });

            let data;

            try {
                data = await response.json();
            } catch (error) {
                throw new Error(
                    "The server returned an invalid response."
                );
            }

            if (!response.ok) {
                throw new Error(
                    data.error || "Could not load dashboard data."
                );
            }

            const summary = data.summary || {};

            const analyses = Array.isArray(data.recent_analyses)
                ? data.recent_analyses
                : [];

            const latest = analyses.length > 0
                ? analyses[0]
                : null;


            // --------------------------------------
            // 4A. LATEST ANALYSIS RESULT
            // --------------------------------------

            let latestResult = latest?.analysis_result || {};

            if (typeof latestResult === "string") {
                try {
                    latestResult = JSON.parse(latestResult);
                } catch (error) {
                    console.error(
                        "Could not parse the latest analysis result:",
                        error
                    );

                    latestResult = {};
                }
            }

            if (
                !latestResult ||
                typeof latestResult !== "object" ||
                Array.isArray(latestResult)
            ) {
                latestResult = {};
            }


            // --------------------------------------
            // 4B. OVERALL MATCH SCORE
            // --------------------------------------

            const score = latest?.match_score == null
                ? null
                : Number(latest.match_score);

            const validScore =
                score !== null && Number.isFinite(score)
                    ? Math.max(0, Math.min(100, score))
                    : null;

            setText(
                "[data-dashboard='overall-score']",
                validScore === null
                    ? "—"
                    : validScore.toFixed(2)
            );

            setProgressBar(
                "[data-dashboard-bar='overall-score']",
                validScore
            );

            setText(
                "[data-dashboard='overall-note']",
                latest
                    ? `Latest analysis: ${latest.job_title || "Job"}`
                    : "Run your first resume analysis"
            );


            // --------------------------------------
            // 4C. KEYWORD RELEVANCE
            // --------------------------------------

            // The existing matcher uses match_score as the
            // keyword relevance score.
            setText(
                "[data-dashboard='keyword-score']",
                validScore === null
                    ? "—"
                    : validScore.toFixed(2)
            );

            setProgressBar(
                "[data-dashboard-bar='keyword-score']",
                validScore
            );


            // --------------------------------------
            // 4D. ATS FORMATTING SCORE
            // --------------------------------------

            const atsScore = latestResult.ats_score == null
                ? null
                : Number(latestResult.ats_score);

            const validAtsScore =
                atsScore !== null && Number.isFinite(atsScore)
                    ? Math.max(0, Math.min(100, atsScore))
                    : null;

            setText(
                "[data-dashboard='ats-score']",
                validAtsScore === null
                    ? "—"
                    : validAtsScore.toFixed(1)
            );

            setProgressBar(
                "[data-dashboard-bar='ats-score']",
                validAtsScore
            );


            // --------------------------------------
            // 4E. ANALYSIS SUMMARY
            // --------------------------------------

            const totalAnalyses = Number(
                summary.total_analyses || 0
            );

            const averageScore = summary.average_score == null
                ? null
                : Number(summary.average_score);

            setText(
                "[data-dashboard='total-analyses']",
                totalAnalyses
            );

            setText(
                "[data-dashboard='average-score']",
                averageScore === null ||
                !Number.isFinite(averageScore)
                    ? "—"
                    : `${averageScore.toFixed(1)}%`
            );

            setText(
                "[data-dashboard='latest-score']",
                validScore === null
                    ? "—"
                    : `${validScore.toFixed(2)}%`
            );


            // --------------------------------------
            // 4F. MATCHED AND MISSING SKILLS
            // --------------------------------------

            const matchedSkills = Array.isArray(
                latestResult.matched_skills
            )
                ? latestResult.matched_skills
                : [];

            const missingSkills = Array.isArray(
                latestResult.missing_skills
            )
                ? latestResult.missing_skills
                : [];

            setText(
                "[data-dashboard='missing-skills-count']",
                missingSkills.length
            );

            setText("#matchedSkillCount", matchedSkills.length);
            setText("#missingSkillCount", missingSkills.length);

            renderSkillBadges(
                "#dashboardMatchedSkills",
                matchedSkills,
                "matched"
            );

            renderSkillBadges(
                "#dashboardMissingSkills",
                missingSkills,
                "missing"
            );

            setText(
                "#skillGapMessage",
                latest
                    ? "These results come from your latest resume and job description."
                    : "Run an analysis to discover your skill gaps."
            );


            // --------------------------------------
            // 4G. DASHBOARD STATUS
            // --------------------------------------

            if (statusElement) {
                statusElement.textContent = latest
                    ? "Latest analysis available"
                    : "Run your first resume analysis";
            }

            setText(
                "[data-dashboard='growth-note']",
                totalAnalyses > 0
                    ? `${totalAnalyses} saved analysis(es) in your history.`
                    : "Your tracker will update as you use the application."
            );


            // --------------------------------------
            // 4H. RECENT ANALYSES
            // --------------------------------------

            renderRecentAnalyses(analyses);


            // --------------------------------------
            // 4I. ANALYTICS SUMMARY CARDS
            // --------------------------------------

            setText(
                "[data-dashboard='analytics-total']",
                totalAnalyses
            );

            setText(
                "[data-dashboard='analytics-average']",
                averageScore === null ||
                !Number.isFinite(averageScore)
                    ? "0"
                    : averageScore.toFixed(1)
            );

            setText(
                "[data-dashboard='analytics-latest-date']",
                summary.latest_analysis || "—"
            );


            // --------------------------------------
            // 4J. ANALYTICS CHART AND INSIGHTS
            // --------------------------------------

            renderMatchScoreChart(
                Array.isArray(data.score_trend)
                    ? data.score_trend
                    : []
            );

            renderTopJobRoles(
                Array.isArray(data.top_job_roles)
                    ? data.top_job_roles
                    : []
            );

            renderFrequentlyMissingSkills(
                Array.isArray(data.frequently_missing_skills)
                    ? data.frequently_missing_skills
                    : []
            );

        } catch (error) {
            console.error(
                "Dashboard loading failed:",
                error
            );

            if (statusElement) {
                statusElement.textContent =
                    "Unable to load dashboard data";
            }

            showLoadError(
                "[data-dashboard='recent-analyses']",
                "Could not load recent analyses. Refresh the page to try again."
            );

            showLoadError(
                "#dashboardMatchedSkills",
                "Could not load matched skills."
            );

            showLoadError(
                "#dashboardMissingSkills",
                "Could not load missing skills."
            );

            showLoadError(
                "#topJobRoles",
                "Could not load job role analytics. Please refresh."
            );

            showLoadError(
                "#frequentlyMissingSkills",
                "Could not load skill analytics. Please refresh."
            );

            const chartEmptyMessage = document.getElementById(
                "matchScoreChartEmpty"
            );

            if (chartEmptyMessage) {
                chartEmptyMessage.hidden = false;
                chartEmptyMessage.textContent =
                    "Could not load analytics. Please refresh.";
            }
        }
    }


    // ==========================================
    // 5. SAFE TEXT AND PROGRESS HELPERS
    // ==========================================

    function setText(selector, value) {
        document.querySelectorAll(selector).forEach(element => {
            element.textContent = String(value);
        });
    }

    function setProgressBar(selector, value) {
        document.querySelectorAll(selector).forEach(bar => {
            const validValue =
                value !== null && Number.isFinite(value)
                    ? Math.max(0, Math.min(100, value))
                    : 0;

            bar.style.width = `${validValue}%`;
        });
    }

    function showLoadError(selector, message) {
        const container = document.querySelector(selector);

        if (!container) {
            return;
        }

        container.replaceChildren();

        const paragraph = document.createElement("p");

        paragraph.className = "muted";
        paragraph.textContent = message;

        container.appendChild(paragraph);
    }


    // ==========================================
    // 6. SKILL GAP ANALYZER
    // ==========================================

    function renderSkillBadges(selector, skills, type) {
        const container = document.querySelector(selector);

        if (!container) {
            return;
        }

        container.replaceChildren();

        if (!Array.isArray(skills) || skills.length === 0) {
            const message = document.createElement("p");

            message.className = "muted";

            message.textContent = type === "matched"
                ? "No matched skills found in the latest analysis."
                : "No missing skills reported in the latest analysis.";

            container.appendChild(message);
            return;
        }

        skills.forEach(skill => {
            const badge = document.createElement("span");

            badge.className = `skill-badge ${type}`;
            badge.textContent = String(skill);

            container.appendChild(badge);
        });
    }


    // ==========================================
    // 7. RECENT ANALYSES
    // ==========================================

    function renderRecentAnalyses(analyses) {
        const container = document.querySelector(
            "[data-dashboard='recent-analyses']"
        );

        if (!container) {
            return;
        }

        container.replaceChildren();

        if (!Array.isArray(analyses) || analyses.length === 0) {
            const message = document.createElement("p");

            message.className = "muted";
            message.textContent =
                "No saved analyses yet. Analyze a resume to get started.";

            container.appendChild(message);
            return;
        }

        analyses.forEach(analysis => {
            const card = document.createElement("article");

            card.className = "dashboard-analysis-item";

            const title = document.createElement("h3");
            title.textContent = analysis.job_title || "Untitled job";

            const company = document.createElement("p");

            company.className = "muted";
            company.textContent =
                analysis.company_name || "Company not specified";

            const score = document.createElement("strong");

            const numericScore = analysis.match_score == null
                ? NaN
                : Number(analysis.match_score);

            score.textContent = Number.isFinite(numericScore)
                ? `${numericScore.toFixed(2)}% match`
                : "Score unavailable";

            const date = document.createElement("small");

            date.className = "muted";
            date.textContent = analysis.created_at || "";

            card.append(title, company, score, date);
            container.appendChild(card);
        });
    }


    // ==========================================
    // 8. MATCH SCORE TREND CHART
    // ==========================================

    function renderMatchScoreChart(trend) {
        const canvas = document.getElementById("matchScoreChart");

        if (!canvas) {
            return;
        }

        const emptyMessage = document.getElementById(
            "matchScoreChartEmpty"
        );

        if (!Array.isArray(trend) || trend.length === 0) {
            if (matchScoreChartInstance) {
                matchScoreChartInstance.destroy();
                matchScoreChartInstance = null;
            }

            if (emptyMessage) {
                emptyMessage.hidden = false;
                emptyMessage.textContent =
                    "Complete a resume analysis to see your score trend.";
            }

            return;
        }

        if (typeof Chart === "undefined") {
            console.error(
                "Chart.js is not loaded. Check index.html and your internet connection."
            );

            if (emptyMessage) {
                emptyMessage.hidden = false;
                emptyMessage.textContent =
                    "The chart library could not load. Please refresh.";
            }

            return;
        }

        if (emptyMessage) {
            emptyMessage.hidden = true;
        }

        const labels = trend.map(item => {
            return item.created_at || "Analysis";
        });

        const scores = trend.map(item => {
            const score = Number(item.match_score);

            return Number.isFinite(score)
                ? Math.max(0, Math.min(100, score))
                : 0;
        });

        if (matchScoreChartInstance) {
            matchScoreChartInstance.destroy();
            matchScoreChartInstance = null;
        }

        matchScoreChartInstance = new Chart(canvas, {
            type: "line",

            data: {
                labels: labels,

                datasets: [{
                    label: "Match Score (%)",
                    data: scores,

                    borderColor: "#6856df",
                    backgroundColor: "rgba(104, 86, 223, 0.10)",

                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 6,

                    pointBackgroundColor: "#ffffff",
                    pointBorderColor: "#6856df",
                    pointBorderWidth: 2,

                    tension: 0.35,
                    fill: true
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    intersect: false,
                    mode: "index"
                },

                animation: {
                    duration: 500
                },

                plugins: {
                    legend: {
                        display: true,
                        position: "top",
                        align: "start",

                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            boxWidth: 8,
                            padding: 20,
                            color: "#737990",

                            font: {
                                size: 11
                            }
                        }
                    },

                    tooltip: {
                        backgroundColor: "#292740",
                        titleColor: "#ffffff",
                        bodyColor: "#ffffff",
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false,

                        callbacks: {
                            label: function(context) {
                                return `Match Score: ${context.parsed.y}%`;
                            }
                        }
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        min: 0,
                        max: 100,

                        title: {
                            display: true,
                            text: "Match Score (%)",
                            color: "#737990"
                        },

                        grid: {
                            color: "#f0f1f7"
                        },

                        ticks: {
                            stepSize: 25,
                            color: "#85899e",

                            callback: function(value) {
                                return `${value}%`;
                            },

                            font: {
                                size: 10
                            }
                        },

                        border: {
                            display: false
                        }
                    },

                    x: {
                        grid: {
                            display: false
                        },

                        ticks: {
                            color: "#85899e",
                            maxRotation: 0,
                            autoSkip: true,
                            maxTicksLimit: 5,

                            font: {
                                size: 10
                            }
                        },

                        border: {
                            display: false
                        }
                    }
                }
            }
        });
    }


    // ==========================================
    // 9. TOP JOB ROLES
    // ==========================================

    function renderTopJobRoles(roles) {
        const container = document.getElementById("topJobRoles");

        if (!container) {
            return;
        }

        container.replaceChildren();

        if (!Array.isArray(roles) || roles.length === 0) {
            const message = document.createElement("p");

            message.className = "analytics-loading";
            message.textContent =
                "No job role analytics yet. Analyze a resume first.";

            container.appendChild(message);
            return;
        }

        roles.forEach(role => {
            const card = document.createElement("div");

            card.className = "analytics-role-item";

            const title = document.createElement("strong");

            title.textContent = role.job_title || "Untitled role";

            const details = document.createElement("p");

            details.className = "muted";

            const count = Number(role.analysis_count || 0);

            const average = role.average_match_score == null
                ? null
                : Number(role.average_match_score);

            const averageText =
                average === null || !Number.isFinite(average)
                    ? "—"
                    : `${average.toFixed(1)}%`;

            details.textContent =
                `${count} analysis(es) · Average match: ${averageText}`;

            card.append(title, details);
            container.appendChild(card);
        });
    }


    // ==========================================
    // 10. FREQUENTLY MISSING SKILLS
    // ==========================================

    function renderFrequentlyMissingSkills(skills) {
        const container = document.getElementById(
            "frequentlyMissingSkills"
        );

        if (!container) {
            return;
        }

        container.replaceChildren();

        if (!Array.isArray(skills) || skills.length === 0) {
            const message = document.createElement("p");

            message.className = "analytics-loading";
            message.textContent =
                "No missing skill data yet. Analyze a resume first.";

            container.appendChild(message);
            return;
        }

        const validSkills = skills.filter(item => {
            return (
                item &&
                typeof item.skill === "string" &&
                item.skill.trim() !== ""
            );
        });

        if (validSkills.length === 0) {
            const message = document.createElement("p");

            message.className = "analytics-loading";
            message.textContent =
                "No missing skill data is available yet.";

            container.appendChild(message);
            return;
        }

        const maximumCount = Math.max(
            ...validSkills.map(item => {
                const count = Number(item.count);

                return Number.isFinite(count)
                    ? Math.max(0, count)
                    : 0;
            }),
            1
        );

        validSkills.forEach(item => {
            const rawCount = Number(item.count);

            const count = Number.isFinite(rawCount)
                ? Math.max(0, rawCount)
                : 0;

            const row = document.createElement("div");

            row.className = "analytics-skill-item";

            const content = document.createElement("div");

            content.className = "analytics-skill-content";

            const name = document.createElement("span");

            name.className = "analytics-skill-name";
            name.textContent = item.skill;

            const barTrack = document.createElement("div");

            barTrack.className = "analytics-skill-bar-track";

            const barFill = document.createElement("div");

            barFill.className = "analytics-skill-bar-fill";

            barFill.style.width =
                `${(count / maximumCount) * 100}%`;

            barTrack.appendChild(barFill);

            const countBadge = document.createElement("strong");

            countBadge.className = "analytics-skill-count";

            countBadge.textContent =
                `${count} ${count === 1 ? "time" : "times"}`;

            content.append(name, barTrack);
            row.append(content, countBadge);

            container.appendChild(row);
        });
    }


    // ==========================================
    // 11. INITIAL DASHBOARD LOAD
    // ==========================================

    loadDashboardData();

});



