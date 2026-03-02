/** @odoo-module **/

(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {

        const wrapper = document.querySelector(".o_ai_ama_chat_wrapper");
        const toggleBtn = document.querySelector(".o_sidebar_toggle");
        const tabs = document.querySelectorAll(".tab");
        const contents = document.querySelectorAll(".tab-content");
        const input = document.getElementById("chatInput");
        const clearBtn = document.getElementById("clearBtn");
        const form = document.getElementById("aiForm");
        const overlay = document.getElementById("loadingOverlay");
        const errorFlag = document.getElementById("ai_error_flag");
        const voiceBtn = document.getElementById("voiceBtn");

        // ======== DataTable Auto Re-adjust =========
        function fixTableAlignment() {
            if ($.fn.DataTable && $.fn.DataTable.isDataTable("#ai_result_table")) {
                setTimeout(() => {
                    $("#ai_result_table").DataTable().columns.adjust().draw();
                }, 200);
            }
        }

        // Sidebar Toggle
        if (toggleBtn) {
            toggleBtn.addEventListener("click", () => {
                wrapper.classList.toggle("sidebar-collapsed");
                const icon = toggleBtn.querySelector("i");
                icon.classList.toggle("fa-chevron-left");
                icon.classList.toggle("fa-chevron-right");

                fixTableAlignment();   // 🔥 fix header/body shift
            });
        }

        // Tabs
        window.openTab = (evt, id) => {
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            evt.currentTarget.classList.add("active");
            document.getElementById(id).classList.add("active");

            fixTableAlignment();   // 🔥 fix shift after switching tab
        };

        // Search history click
        window.setChatInput = (el) => {
            input.value = el.innerText.trim();
            clearBtn.style.display = "block";
            input.focus();
        };

        // Clear button
        const updateClear = () => {
            clearBtn.style.display = input.value ? "block" : "none";
        };
        input?.addEventListener("input", updateClear);
        clearBtn?.addEventListener("click", () => {
            input.value = "";
            updateClear();
            input.focus();
        });

        // Loading overlay
        form?.addEventListener("submit", () => {
            overlay.style.display = "flex";
        });

        // If backend sent error_message → show overlay + error screen
    if (errorFlag) {
        overlay.style.display = "flex";
    }

//        // === Voice Recognition (Toggle Start / Stop) ===
//        if (window.isSecureContext && "webkitSpeechRecognition" in window) {
//
//            const rec = new webkitSpeechRecognition();
//            rec.continuous = false;
//            rec.interimResults = false;
//            let isRecording = false;   // <-- toggle flag
//
//            const updateLang = () => {
//                const selectedLang = document.getElementById("selected_lang").value || "en-US";
//                rec.lang = selectedLang.replace("_", "-");
//            };
//
//            // When recording starts
//            rec.onstart = () => {
//                isRecording = true;
//                voiceBtn.style.background = "#dc3545";
//                voiceBtn.style.color = "#fff";
//                voiceBtn.innerHTML = '<i class="fa fa-microphone-slash"></i>';  // optional icon change
//            };
//
//            // When recording stops
//            rec.onend = () => {
//                isRecording = false;
//                voiceBtn.style.background = "";
//                voiceBtn.style.color = "";
//                voiceBtn.innerHTML = '<i class="fa fa-microphone"></i>';  // optional icon change
//            };
//
//            rec.onresult = e => {
//                input.value = e.results[0][0].transcript;
//                updateClear();
//            };
//
//            // === Toggle Button ===
//            voiceBtn?.addEventListener("click", () => {
//                updateLang();
//                if (!isRecording) {
//                    rec.start();   // first click → start
//                } else {
//                    rec.stop();    // second click → stop
//                }
//            });
//
//        } else {
//            if (voiceBtn) {
//                voiceBtn.disabled = true;
//                voiceBtn.style.opacity = 0.6;
//            }
//        }


if (window.isSecureContext && "webkitSpeechRecognition" in window) {

    const rec = new webkitSpeechRecognition();
    rec.continuous = true;             // keep listening between results
    rec.interimResults = false;

    let isRecording = false;           // toggle flag
    let shouldRestart = false;         // auto-restart flag

    const updateLang = () => {
        const selectedLang = document.getElementById("selected_lang").value || "en-US";
        rec.lang = selectedLang.replace("_", "-");
    };

    // When recognition starts
    rec.onstart = () => {
        console.log("🎤 Voice STARTED");
        voiceBtn.style.background = "#dc3545";
        voiceBtn.title = "Click To Stop";
        voiceBtn.style.color = "#fff";
        voiceBtn.innerHTML = '<i class="fa fa-microphone-slash"></i>';
    };

    // When recognition ends
    rec.onend = () => {
        console.log("🎤 Voice ENDED");
        voiceBtn.style.background = "";
        voiceBtn.style.color = "";
        voiceBtn.innerHTML = '<i class="fa fa-microphone"></i>';

        if (shouldRestart) {
            console.log("⟳ Restarting recognition");
            rec.start();
        }
    };

    rec.onresult = (e) => {
        input.value = e.results[0][0].transcript;
        updateClear();
    };

    // === Toggle Button ===
    voiceBtn?.addEventListener("click", () => {
        updateLang();

        if (!isRecording) {
            // START RECORDING
            isRecording = true;
            shouldRestart = true;
            rec.start();
        } else {
            // STOP RECORDING
            isRecording = false;
            shouldRestart = false;
            rec.stop();
        }
    });

} else {
    if (voiceBtn) {
        voiceBtn.disabled = true;
        voiceBtn.style.opacity = 0.6;
    }
}


        // === Language Dropdown ===
const btn = document.getElementById("langDropdownBtn");
const dropdown = document.getElementById("langDropdown");

if (btn && dropdown) {

    // Toggle dropdown below button
    btn.addEventListener("click", function (e) {
        e.stopPropagation();

        dropdown.style.display =
            dropdown.style.display === "block" ? "none" : "block";

        if (dropdown.style.display === "block") {
            dropdown.style.left = "0px";  // inside .lang-selector
            // show above button
        dropdown.style.bottom = (btn.offsetHeight + 8) + "px";
        dropdown.style.top = "auto";
        }
    });

    // Select language
    document.querySelectorAll(".lang-item").forEach(item => {
        item.addEventListener("click", function () {
            btn.innerHTML = this.innerText;
            document.getElementById("selected_lang").value = this.dataset.lang;
            dropdown.style.display = "none";
        });
    });

    // Close on outside click
    document.addEventListener("click", function (e) {
        if (!btn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = "none";
        }
    });
}




    });

})();
