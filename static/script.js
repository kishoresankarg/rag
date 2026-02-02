document.getElementById('userInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;

    // Add user message to UI
    appendMessage(message, 'user');
    input.value = '';

    // Show loading indicator (optional)
    const loadingId = appendMessage('Searching...', 'bot', true);

    // Call API
    fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: message })
    })
        .then(response => response.json())
        .then(data => {
            // Remove loading
            removeMessage(loadingId);
            // Show bot response
            appendMessage(data.answer, 'bot');
        })
        .catch(error => {
            removeMessage(loadingId);
            appendMessage('❌ Error connecting to server.', 'bot');
            console.error('Error:', error);
        });
}

function appendMessage(text, sender, isLoading = false) {
    const chatContainer = document.getElementById('chatContainer');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message msg-${sender}`;
    if (isLoading) msgDiv.id = 'loading-msg';

    // Format text (convert newlines to br, bold markers to strong tags)
    let formattedText = text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Simple MD bold

    msgDiv.innerHTML = formattedText;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return msgDiv.id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// Modal Functions
function openModal() {
    document.getElementById('orderModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('orderModal').style.display = 'none';
}

// Handle Add Order
document.getElementById('orderForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    // basic conversions
    data.quantity = parseFloat(data.quantity);
    data.unit_price = parseFloat(data.unit_price);

    fetch('/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {
            if (response.success) {
                alert('✅ Order added successfully!');
                closeModal();
                this.reset();
                appendMessage(`✅ I've added a new order for **${data.vendor_name}**.`, 'bot');
            } else {
                alert('❌ Failed to add order.');
            }
        });
});

// Close modal on outside click
window.onclick = function (event) {
    if (event.target == document.getElementById('orderModal')) {
        closeModal();
    }
}
