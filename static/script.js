async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value;

    if(question.trim() === "")
        return;

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    chatBox.innerHTML += `
        <div class="user-message">
            ${question}
        </div>
    `;

    document.getElementById(
        "question"
    ).value = "";

    const response =
        await fetch(
            "/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    question
                })
            }
        );

    const data =
        await response.json();

    chatBox.innerHTML += `
        <div class="bot-message">
            ${data.answer}
        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;
}