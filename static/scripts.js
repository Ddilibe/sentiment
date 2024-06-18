// Function for logging out
function logout() {
    // Perform logout actions here (clear session, redirect to login page, etc.)
    alert("Logged out successfully!");
    window.location.href = "login.html";
}

// Function for sentiment analysis form submission
document.getElementById("sentimentForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const reviewText = document.getElementById("reviewText").value;
    // Here you can implement AJAX request or any other logic for sentiment analysis
    // For demonstration, let's assume a simple random sentiment result
    const sentiments = ["Positive", "Negative", "Neutral"];
    const randomSentiment = sentiments[Math.floor(Math.random() * sentiments.length)];
    document.getElementById("result").innerHTML = `<div class="alert alert-info" role="alert">Sentiment: ${randomSentiment}</div>`;
});