document.getElementById("checkBtn").addEventListener("click", function() {
    const email = document.getElementById("emailInput").value;

    fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = "Prediction: " + data.result;
    })
    .catch(err => {
        document.getElementById("result").innerText = "Error connecting to server.";
    });
});
