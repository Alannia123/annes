odoo.define("mis_student_portal.portal_tts", function () {
    "use strict";

    window.speakText = function (id) {
        const span = document.getElementById("speechText_" + id);
        if (!span) return;

        const text = span.getAttribute("data-speak");
        if (!text) return;

        // Android WebView
        if (window.AndroidTTS && typeof window.AndroidTTS.speakText === "function") {
            window.AndroidTTS.speakText(text);
            return;
        }

        // Browser fallback
        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = "en-US";
            window.speechSynthesis.speak(msg);
        }
    };
});
