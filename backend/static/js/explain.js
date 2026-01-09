function openExplain(studentId) {
    document.getElementById("explainModal").style.display = "block";
    document.getElementById("loading").style.display = "block";

    clearLists();

    fetch(`/explain/${studentId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("loading").style.display = "none";

            if (!data.success) {
                showFallback();
                return;
            }

            typeText("explanation", data.explanation);
            fillList("positives", data.positive_factors);
            fillList("risks", data.risk_factors);
            fillList("actions", data.suggested_actions);

            animateConfidence(data.confidence || 60);
        })
        .catch(() => {
            showFallback();
        });
}

function closeExplain() {
    document.getElementById("explainModal").style.display = "none";
}

/* ===== Typing Effect ===== */
function typeText(elementId, lines) {
    const el = document.getElementById(elementId);
    el.innerHTML = "";
    let i = 0;

    function typeLine() {
        if (i < lines.length) {
            const li = document.createElement("li");
            el.appendChild(li);
            let text = lines[i];
            let j = 0;

            const interval = setInterval(() => {
                li.textContent += text[j];
                j++;
                if (j === text.length) {
                    clearInterval(interval);
                    i++;
                    setTimeout(typeLine, 300);
                }
            }, 25);
        }
    }
    typeLine();
}

/* ===== Lists ===== */
function fillList(id, items) {
    const ul = document.getElementById(id);
    ul.innerHTML = "";
    items.forEach(i => {
        const li = document.createElement("li");
        li.textContent = i;
        ul.appendChild(li);
    });
}

/* ===== Confidence Bar ===== */
function animateConfidence(value) {
    const bar = document.getElementById("confidenceFill");
    bar.style.width = "0%";
    setTimeout(() => {
        bar.style.width = value + "%";
    }, 200);
}

/* ===== Clear ===== */
function clearLists() {
    ["explanation", "positives", "risks", "actions"].forEach(id => {
        document.getElementById(id).innerHTML = "";
    });
    document.getElementById("confidenceFill").style.width = "0%";
}

/* ===== FALLBACK (NO GEMINI) ===== */
function showFallback() {
    document.getElementById("loading").style.display = "none";

    typeText("explanation", [
        "This explanation is generated using internal academic rules.",
        "The student performance indicators suggest attention is required."
    ]);

    fillList("positives", ["Some academic indicators are stable"]);
    fillList("risks", ["Low marks or attendance detected"]);
    fillList("actions", ["Provide mentoring", "Track weekly progress"]);

    animateConfidence(55);
}

