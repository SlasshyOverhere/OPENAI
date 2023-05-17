from flask import Flask, render_template, request
import openai

app = Flask(__name__)

openai.api_key = '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'

index_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chat App</title>
    <style>
        body {
            background-color: #f3f3f3;
            font-family: Arial, sans-serif;
        }

        h1 {
            color: #333;
            text-align: center;
            padding-top: 20px;
        }

        #chat-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        #messages {
            margin-bottom: 20px;
        }

        #messages p {
            margin: 10px 0;
        }

        #message-input {
            width: 80%;
            padding: 10px;
            border: 1px solid #ccc;
        }

        button[type="submit"] {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: #fff;
            border: none;
            cursor: pointer;
        }

        button[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>Chat App</h1>
    <div id="chat-container">
        <div id="messages"></div>
        <form id="message-form" action="/chat" method="POST">
            <input type="text" id="message-input" name="message" autofocus autocomplete="off">
            <button type="submit">Send</button>
        </form>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#message-form').on('submit', function(e) {
                e.preventDefault();
                var message = $('#message-input').val().trim();
                if (message !== '') {
                    $('#message-input').val('');
                    $('#messages').append('<p><strong>You:</strong> ' + message + '</p>');
                    scrollToBottom();
                    $.ajax({
                        type: 'POST',
                        url: '/chat',
                        data: { message: message },
                        success: function(response) {
                            var reply = response.message;
                            $('#messages').append('<p><strong>CHAT_SLASSHY:</strong> ' + reply + '</p>');
                            scrollToBottom();
                        }
                    });
                }
            });

            function scrollToBottom() {
                var messagesContainer = $('#messages');
                messagesContainer.scrollTop(messagesContainer[0].scrollHeight);
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return index_html

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=256,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    reply = response.choices[0].text.strip()

    return {'message': reply}

if __name__ == '__main__':
    app.run()
