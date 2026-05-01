function setMessage(text) {
    document.getElementById("message").value = text;
}

async function predict() {
    const message = document.getElementById("message").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "⏳ Checking...";

    try {
        const response = await fetch("https://sms-spam-2-jsrh.onrender.com/predict", {
            method: "POST",   // 🔥 MUST
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        resultDiv.innerHTML = `
            <p><strong>${data.prediction}</strong></p>
        `;

    } catch (error) {
        resultDiv.innerHTML = "❌ Error connecting to server";
    }
}
