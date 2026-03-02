/** @odoo-module */

import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { _t } from "@web/core/l10n/translation";

export class VoiceToTextButton extends Component {
    static template = "voice_to_text.VoiceToTextButton";
    static props = ["record", "fieldName", "selectedLang"];

    setup() {
        this.notification = useService("notification");

        this.state = useState({
            isListening: false,
            isError: false,
            recognition: null,
        });

        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            console.warn("Speech Recognition not supported");
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = this.props.selectedLang;

        // 🎤 START
        recognition.onstart = () => {
            this.state.isListening = true;
            this.state.isError = false;
        };

        // ⏹ END
        recognition.onend = () => {
            this.state.isListening = false;
        };

        recognition.onerror = (event) => this.onRecognitionError(event);
        recognition.onresult = (event) => this.onRecognitionResult(event);

        this.state.recognition = recognition;
    }

    // 🔁 TOGGLE BUTTON (CLICK)
    toggleRecording(ev) {
        ev.preventDefault();

        if (!this.state.recognition) return;

        try {
            if (!this.state.isListening) {
                // ▶️ START
                this.state.recognition.lang = this.props.selectedLang;
                this.state.recognition.start();
            } else {
                // ⏹ STOP
                this.state.recognition.stop();
            }
        } catch (e) {
            console.warn("Speech toggle failed", e);
        }
    }

    // ❌ Error handler
    onRecognitionError(event) {
        this.state.isError = true;
        this.state.isListening = false;

        let msg = _t(`Error: ${event.error}`);
        if (event.error === "not-allowed") {
            msg = _t("Microphone permission denied");
        } else if (event.error === "no-speech") {
            msg = _t("No speech detected");
        }

        this.notification.add(msg, { type: "danger" });

        try {
            this.state.recognition.stop();
        } catch (_) {}
    }

    // 🎧 Speech result
    onRecognitionResult(event) {
        let transcript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                transcript += event.results[i][0].transcript;
            }
        }

        if (!transcript) return;

        const current =
            this.props.record.data[this.props.fieldName] || "";

        const updated = current
            ? `${current}\n${transcript}`
            : transcript;

        this.props.record.update({
            [this.props.fieldName]: updated,
        });
    }
}



// 2. Define the Custom Widget that uses the component
export class VoiceToTextField extends Component {
    static template = "voice_to_text.VoiceWidget";
    static components = { CharField, VoiceToTextButton };
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.state = useState({
            selectedLang: 'en-US', // Default language
        });

        this.languages = [
            { code: 'en_IN', name: 'English (IN)' },
//            { code: 'en-GB', name: 'English (UK)' },
//            { code: 'ta-IN', name: 'Tamil (தமிழ்)' },
//            { code: 'es-ES', name: 'Spanish (Spain)' },
//            { code: 'es-MX', name: 'Spanish (Mexico)' },
//            { code: 'fr-FR', name: 'French (France)' },
//            { code: 'de-DE', name: 'German (Germany)' },
//            { code: 'it-IT', name: 'Italian (Italy)' },
//            { code: 'pt-BR', name: 'Portuguese (Brazil)' },
//            { code: 'ja-JP', name: 'Japanese' },
//            { code: 'ko-KR', name: 'Korean' },
//            { code: 'cmn-Hans-CN', name: 'Chinese (Mandarin)' },
            { code: 'hi_IN', name: 'Hindi / हिंदी' },
            { code: 'bn_IN', name: 'Bengali / বাংলা' },
//            { code: 'ar-EG', name: 'Arabic (Egypt)' },
//            { code: 'ru-RU', name: 'Russian' },
        ];
    }

    get record() {
        return this.props.record;
    }

    clearText() {
        this.props.record.update({ [this.props.name]: "" });
    }

    _onLangChange(ev) {
        this.state.selectedLang = ev.target.value;
    }
}

// 3. Register the new widget in Odoo's field registry
registry.category("fields").add("voice_to_text", {
    component: VoiceToTextField,
});