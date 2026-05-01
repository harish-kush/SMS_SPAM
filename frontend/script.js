function setMessage(text) {
    document.getElementById("message").value = text;
}

async function predict() {
    const message = document.getElementById("message").value;
    const resultDiv = document.getElementById("result");

    if (!message.trim()) {
        resultDiv.innerHTML = "⚠️ Please enter a message";
        return;
    }

    resultDiv.innerHTML = "⏳ Checking...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        resultDiv.innerHTML = `
            <p><strong>Prediction:</strong> ${data.prediction}</p>
            <p>Spam Confidence: ${(data.confidence.Spam * 100).toFixed(2)}%</p>
        `;

    } catch (error) {
        resultDiv.innerHTML = "❌ Error connecting to server";
    }
}
