const messageInput = document.querySelector('#message-input');
const sendButton = document.querySelector('#send-button');
const chatContainer = document.querySelector('#chat-container');

sendButton.addEventListener('click', () => {
  const message = messageInput.value;
  if (!message) return;

  const payload = {
    message: message
  };

  fetch('http://localhost:5005/webhooks/rest/webhook', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    // Display the bot's response in the chat container
    const botResponse = data[0].text;
    const messageElement = document.createElement('div');
    messageElement.classList.add('bot-message');
    messageElement.innerHTML = botResponse;
    chatContainer.appendChild(messageElement);
  })
  .catch(error => console.error(error));

  // Clear the message input field
  messageInput.value = '';
});

// Listen for enter keypresses in the message input field
messageInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    sendButton.click();
    event.preventDefault();
  }
});
