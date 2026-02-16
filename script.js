function startSpeech() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.onresult = function(event) {
        document.getElementById("output").innerText =
            event.results[0][0].transcript;
    };
    recognition.start();
}

function speakText() {
    const text = document.getElementById("output").innerText;
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
}
