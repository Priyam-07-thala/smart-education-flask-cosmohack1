function explainStudent(studentId) {
    fetch(`/explain/${studentId}`)
        .then(res => res.json())
        .then(data => {
            console.log("Explanation API response:", data);

            if (!data.success) {
                throw new Error("API returned failure");
            }

            document.getElementById("ai-explanation").innerHTML =
                data.explanation.map(e => `<li>${e}</li>`).join("");

            document.getElementById("positive-factors").innerHTML =
                data.positive_factors.map(e => `<li>${e}</li>`).join("");

            document.getElementById("risk-factors").innerHTML =
                data.risk_factors.map(e => `<li>${e}</li>`).join("");

            document.getElementById("suggested-actions").innerHTML =
                data.suggested_actions.map(e => `<li>${e}</li>`).join("");

            const confidence = data.confidence || 60;
            document.getElementById("confidence-bar").style.width = confidence + "%";
            document.getElementById("confidence-text").innerText = confidence + "%";

            document.getElementById("explanationModal").style.display = "block";
        })
        .catch(err => {
            console.error("Explanation error:", err);
            document.getElementById("ai-explanation").innerHTML =
                "<li>Failed to load explanation.</li>";
        });
}

function closeExplanation() {
    document.getElementById("explanationModal").style.display = "none";
}
