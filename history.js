
document.addEventListener("DOMContentLoaded", async () => {
    const status = document.querySelector("#historyStatus");
    const historyList = document.querySelector("#historyList");

    try {
        const response = await fetch("/api/history");
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not load history.");
        }

        const analyses = result.analyses || [];

        if (analyses.length === 0) {
            status.textContent = "No saved analyses yet.";
            return;
        }

        status.textContent = `${analyses.length} recent analysis record(s)`;

        analyses.forEach((analysis) => {
            const card = document.createElement("article");
            card.className = "history-card";

            const title = document.createElement("h2");
            title.textContent = analysis.job_title || "Untitled job";

            const company = document.createElement("p");
            company.className = "history-company";
            company.textContent = analysis.company_name || "Company not specified";

            const score = document.createElement("p");
            score.className = "history-score";
            score.textContent =
                `${Number(analysis.match_score).toFixed(2)}% match`;

            const date = document.createElement("p");
            date.className = "history-date";
            date.textContent = analysis.created_at || "Date unavailable";

            card.append(title, company, score, date);
            historyList.appendChild(card);
        });

    } catch (error) {
        status.textContent = error.message;
    }
});
