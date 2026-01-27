async function askBot(question) {
    const res = await fetch(`${API_URL}/chatbot/ask`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question})
    });
    const data = await res.json();
    return data.answer;
}

document.getElementById("askBtn")?.addEventListener("click", async () => {
    const question = document.getElementById("question").value;
    const answer = await askBot(question);
    document.getElementById("answer").innerText = answer;
});
