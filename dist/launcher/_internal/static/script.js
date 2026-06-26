const datasetButton = document.getElementById('dataset-file');
const trainEvaluateButton = document.getElementById('train-evaluate-button');
const askButton = document.getElementById("ask-button");
const knowledgebaseButton = document.getElementById('knowledgebase-file');

datasetButton.addEventListener('change', function() {
    const file = this.files[0];

    const formData = new FormData();
    formData.append("file", file);

    sendFile(formData);
});

knowledgebaseButton.addEventListener('change', function() {
    const file = this.files[0];

    const knowledgebase = new FormData();
    knowledgebase.append("file", file);

    sendKnowledgebase(knowledgebase);
});

trainEvaluateButton.addEventListener('click', function() {

    const selectedTraingMethod = document.getElementById("model-select").value;
    const selectedTrainingSize = document.getElementById("train-size").value;
    const selectedTestSize = document.getElementById("test-size").value;
    const selectedFeatures = Array.from(document.querySelectorAll('input[name="features"]:checked')).map(el => el.value);
    const selectedTarget = document.querySelector('input[name="target"]:checked')?.value;

    if (selectedFeatures.length === 0) {
        alert("No features have been selected");
        return;
    }

    if (!selectedTarget) {
        alert("No target has been selected");
        return;
    }

    const payload = {
        file_id: localStorage.getItem("fileId"),
        model: selectedTraingMethod,
        train_size: selectedTrainingSize,
        test_size: selectedTestSize,
        features: selectedFeatures,
        target: selectedTarget
    };

    sendModelParams(payload);
});

askButton.addEventListener("click", function() {
    const userQuestion = document.getElementById("question-textarea").value;
    const chatAnswer = document.getElementById("chatbot-answer");
    const chatConfidence = document.getElementById("chatbot-confidence");

    fetch("http://127.0.0.1:8000/question", {
        method: "POST",
        body: JSON.stringify({question: userQuestion}),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(async (res) => {
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            throw new Error(data.detail || `HTTP error: ${res.status}`);
        }

        return data;
    })
    .then(data => {
        console.log("Question sent successfully:", data);
        chatAnswer.innerHTML = `<p>${data.answer}</p>`;
        chatConfidence.innerHTML = `<p>Confidence score: ${data.confidence}</p>`;
    })
    .catch(err => {
        console.error("Error sending question:", err);
        alert(err.message);
    });
});

function sendFile(formData) {
    const fileName = document.getElementById("dataset-name");

    fetch("http://127.0.0.1:8000/upload-csv", {
        method: "POST",
        body: formData
    })
    .then(async (res) => {
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            throw new Error(data.detail || `HTTP error: ${res.status}`);
        }

        return data;
    })
    .then(data => {
        console.log("Server response:", data);
        buildFeatureUI(data.columns);
        localStorage.setItem("fileId", data.file_id);
        fileName.textContent = data.file_name;
    })
    .catch(err => {
        console.error("Upload failed:", err.message);
        alert(err.message);
    });
}

function buildFeatureUI(columns) {
    const featureContainer = document.getElementById('feature-container');
    const targetContainer = document.getElementById('target-container');

    // Clear previous options
    featureContainer.innerHTML = '';
    targetContainer.innerHTML = '';

    columns.forEach(column => {
        // Create checkbox for each feature
        const featureLabel = document.createElement('label');
        featureLabel.textContent = ` ${column}`;
        featureLabel.setAttribute('for', `feature-${column}`);
        
        const featureCheckbox = document.createElement('input');
        featureCheckbox.type = 'checkbox';
        featureCheckbox.id = `feature-${column}`;
        featureCheckbox.name = 'features';
        featureCheckbox.value = column;

        featureContainer.appendChild(featureCheckbox);
        featureContainer.appendChild(featureLabel);
        featureContainer.appendChild(document.createElement('br'));

        // Create radio button for target variable
        const targetLabel = document.createElement('label');
        targetLabel.textContent = ` ${column}`;
        targetLabel.setAttribute('for', `target-${column}`);

        const targetRadio = document.createElement('input');
        targetRadio.type = 'radio';
        targetRadio.id = `target-${column}`;
        targetRadio.name = 'target';
        targetRadio.value = column;

        targetContainer.appendChild(targetRadio);
        targetContainer.appendChild(targetLabel);
        targetContainer.appendChild(document.createElement('br'));

        // Make parameters section visible
        document.querySelector(".options").style.display = "flex";
        document.getElementById("train-evaluate").style.display = "block";
    });
}

function sendModelParams(payload) {
    const evaluationResults = document.getElementById("evaluation-results");

    fetch("http://127.0.0.1:8000/train-test", {
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(async (res) => {
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            throw new Error(data.detail || `HTTP error: ${res.status}`);
        }

        return data;
    })
    .then(data => {
        console.log("Model parameters sent successfully:", data);
        evaluationResults.innerHTML =
            `<p>Accuracy: ${data.test_results.accuracy}</p>
            <p>Precision: ${data.test_results.precision}</p>
            <p>Recall: ${data.test_results.recall}</p>
            <p>F1 score: ${data.test_results.f1_score}</p>`;
    })
    .catch(err => {
        console.error("Error sending model parameters:", err);
        alert(err.message);
    });
}

function sendKnowledgebase(knowledgebase) {
    const knowledgebaseName = document.getElementById("knowledgebase-name");

    fetch("http://127.0.0.1:8000/upload-knowledgebase", {
        method: "POST",
        body: knowledgebase
    })
    .then(async (res) => {
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            throw new Error(data.detail || `HTTP error: ${res.status}`);
        }

        return data;
    })
    .then(data => {
        knowledgebaseName.textContent = data.file_name;
    })
    .catch(err => {
        console.error("Upload failed:", err.message);
        alert(err.message);
    });
}