function openExplain(studentId) {
    // Show modal
    document.getElementById("explainModal").style.display = "block";

    // Reset UI
    document.getElementById("explanation").innerHTML = "";
    document.getElementById("positives").innerHTML = "";
    document.getElementById("risks").innerHTML = "";
    document.getElementById("actions").innerHTML = "";
    document.getElementById("confidenceFill").style.width = "0%";

    fetch(`/explain/${studentId}`)
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                document.getElementById("explanation").innerHTML =
                    "<li>Failed to load explanation</li>";
                return;
            }

            data.explanation.forEach(e =>
                document.getElementById("explanation").innerHTML += `<li>${e}</li>`
            );

            data.positive_factors.forEach(e =>
                document.getElementById("positives").innerHTML += `<li>${e}</li>`
            );

            data.risk_factors.forEach(e =>
                document.getElementById("risks").innerHTML += `<li>${e}</li>`
            );

            data.suggested_actions.forEach(e =>
                document.getElementById("actions").innerHTML += `<li>${e}</li>`
            );

            document.getElementById("confidenceFill").style.width =
                data.confidence + "%";
        })
        .catch(() => {
            document.getElementById("explanation").innerHTML =
                "<li>Error loading explanation</li>";
        });
}

function closeExplain() {
    document.getElementById("explainModal").style.display = "none";
}
