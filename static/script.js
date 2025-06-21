function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message); // 👈 USER
  input.value = "";

  appendMessage("bot", "Typing..."); // 👈 TEMP BOT

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: message })
  })
    .then(res => {
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      return res.json();
    })
    .then(data => {
      clearLastBotMessage(); // remove "Typing..."
      appendMessage("bot", `🧠 professional: ${data.professional}`);
      appendMessage("bot", `🌱 simple:${data.simple}`);
      appendMessage("bot", `🚀 approach:${data.approach}`);
    })
    .catch(err => {
      clearLastBotMessage();
      appendMessage("bot", "⚠️ " + err.message);
    });
}

function appendMessage(sender, message) {
  const chatBox = document.getElementById("chat-box");
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message");

  if (sender === "user") {
    msgDiv.classList.add("user-message");
  } else {
    msgDiv.classList.add("bot-message");
  }

  msgDiv.textContent = message;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function clearLastBotMessage() {
  const chatBox = document.getElementById("chat-box");
  const lastMsg = chatBox.lastChild;
  if (lastMsg && lastMsg.classList.contains("bot-message")) {
    chatBox.removeChild(lastMsg);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const chatContainer = document.querySelector('.chat-container');
  if (chatContainer) {
    // Expand on click
    chatContainer.addEventListener('click', function() {
      chatContainer.classList.add('expanded');
    });

    // Optional: collapse if clicked outside
    document.addEventListener('click', function(event) {
      if (!chatContainer.contains(event.target)) {
        chatContainer.classList.remove('expanded');
      }
    });
  }
});
