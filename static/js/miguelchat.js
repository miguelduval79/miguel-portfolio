const input = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const typingIndicator = document.getElementById("typing-indicator");

function createMessage(text, sender) {

    const message = document.createElement("div");

    message.className =
        sender === "user"
            ? "user-message"
            : "assistant-message";

    message.innerHTML = text;

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    createMessage(message, "user");

    input.value = "";

    typingIndicator.style.display = "block";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        typingIndicator.style.display = "none";

        createMessage(data.reply, "assistant");

    }
    catch (error) {

        typingIndicator.style.display = "none";

        createMessage(
            "Unable to connect to the server.",
            "assistant"
        );

        console.error(error);

    }

}

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keydown", function(event){

    if(event.key === "Enter"){

        sendMessage();

    }

});