const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("fileInput");
const statusText = document.getElementById("status");

/* Click */
dropZone.addEventListener("click", () => fileInput.click());

/* Drag over */
dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

/* Drag leave */
dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

/* Drop */
dropZone.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    uploadFile(e.dataTransfer.files[0]);
});

/* Manual select */
fileInput.addEventListener("change", () => {
    uploadFile(fileInput.files[0]);
});

function uploadFile(file) {
    if (!file || !file.name.toLowerCase().endsWith(".csv")) {
        statusText.innerText = "❌ Please upload a valid CSV file";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    statusText.innerText = "⏳ Uploading...";

    fetch("/upload_csv", {
        method: "POST",
        body: formData
    })
    .then(async res => {
        let data;
        try {
            data = await res.json();
        } catch {
            throw new Error("Invalid server response");
        }

        if (!res.ok) {
            throw new Error(data.error || "Upload failed");
        }

        return data;
    })
    .then(data => {
        if (data.success) {
            statusText.innerText = "✅ CSV uploaded successfully!";
            setTimeout(() => location.reload(), 800);
        } else {
            statusText.innerText = "❌ " + (data.error || "Upload failed");
        }
    })
    .catch(err => {
        statusText.innerText = "❌ " + err.message;
        console.error("Upload error:", err);
    });
}
