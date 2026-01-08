console.log("explain.js loaded");

function openExplain(studentId) {
    console.log("Explain clicked for:", studentId);

    const modal = document.getElementById("explainModal");
    if (!modal) {
        alert("Explain modal not found in DOM");
        return;
    }

    modal.style.display = "block";

    const loading = document.getElementById("loading");
    loading.style.display = "block";
    loading.innerText = "Generating explanation...";

    fetch(`/explain/${studentId}`)
        .then(res => {
            if (!res.ok) {
                throw new Error("Failed to fetch explanation");
            }
            return res.json();
        })
        .then(data => {
            console.log("Explain API response:", data);

            loading.style.display = "none";

            document.getElementById("riskLabel").innerHTML =
                "<b>Predicted Risk Level:</b> " + data.risk;

            fill("explanation", data.explanation);
            fill("positives", data.positive_factors);
            fill("risks", data.risk_factors);
            fill("actions", data.suggested_actions);

            document.getElementById("confidenceFill").style.width =
                (data.confidence || 70) + "%";
        })
        .catch(err => {
            console.error(err);
            loading.innerText = "Failed to load explanation.";
        });
}

function fill(id, items) {
    const el = document.getElementById(id);
    if (!el) return;

    el.innerHTML = "";
    (items || []).forEach(text => {
        const li = document.createElement("li");
        li.innerText = text;
        el.appendChild(li);
    });
}

function closeExplain() {
    document.getElementById("explainModal").style.display = "none";
}

function toggleTheme() {
    document.body.classList.toggle("dark");
}
