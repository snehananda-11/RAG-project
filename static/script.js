console.log("MY NEW SCRIPT");

let currentConversationId = null;

window.createConversation = async function() {

    const response =
        await fetch(
            "/conversation",
            {
                method:"POST"
            }
        );

    const data =
        await response.json();

    currentConversationId =
        data.conversation_id;

    document.getElementById(
        "chat-box"
    ).innerHTML = "";

    loadConversations();
}


window.loadConversations = async function() {

    const response =
        await fetch(
            "/conversations"
        );

    const data =
        await response.json();

    const list =
        document.getElementById(
            "conversation-list"
        );

    list.innerHTML = "";

    data.forEach(chat => {

        list.innerHTML += `
            <div
                class="conversation-item"
                onclick="openConversation(${chat.id})">

                ${chat.title}

            </div>
        `;
    });

    return data;

}


window.openConversation = async function(id) {

    currentConversationId = id;

    const response =
        await fetch(
            `/conversation/${id}`
        );

    const messages =
        await response.json();

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    chatBox.innerHTML = "";

    messages.forEach(msg => {

        if(msg.role === "user"){

            chatBox.innerHTML += `
                <div class="user-message">
                    ${msg.content}
                </div>
            `;
        }

        else{

            chatBox.innerHTML += `
                <div class="bot-message">
                    ${marked.parse(msg.content)}
                </div>
            `;
        }

    });

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


window.askQuestion = async function() {

    if(!currentConversationId){

        alert(
            "Please create a new chat first."
        );

        return;
    }

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
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({

                    conversation_id:
                    currentConversationId,

                    question:
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

    loadConversations();
}


window.onload = async () => {

    const conversations =
        await loadConversations();

    if(conversations.length === 0){

        await createConversation();

    }

};