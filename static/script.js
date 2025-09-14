async function sendMessage() {
    let input = document.getElementById("user_input").value;
    if (!input) return;

    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="user-msg"><b>You:</b> ${input}</div>`;

    const response = await fetch("/get_response", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: input})
    });

    const data = await response.json();
    chatbox.innerHTML += `<div class="bot-msg"><b>Bot:</b> ${data.response}</div>`;

    chatbox.scrollTop = chatbox.scrollHeight; // auto scroll
    document.getElementById("user_input").value = "";
}

