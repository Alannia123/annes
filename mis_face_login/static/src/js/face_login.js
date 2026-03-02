/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector("#o_face_login_btn");
    const modal = document.querySelector("#o_face_modal");
    const closeBtn = document.querySelector("#o_face_close");
    console.log('ddddddddddddddddddddddd')

    if (!btn || !modal) {
        console.warn("Face Login elements not found");
        return;
    }

    // 🔹 Open modal
    btn.addEventListener("click", () => {
        modal.style.display = "block";
        const video = document.getElementById("o_face_video");
        if (navigator.mediaDevices?.getUserMedia) {
            navigator.mediaDevices
                .getUserMedia({ video: true })
                .then(stream => {
                    video.srcObject = stream;
                    video.play();
                })
                .catch(err => {
                    console.error("Camera error:", err);
                    document.getElementById("o_face_result").innerText = "Camera access denied";
                });
        }
    });

    // 🔹 Close modal
    closeBtn?.addEventListener("click", () => {
        modal.style.display = "none";
        const video = document.getElementById("o_face_video");
        video?.srcObject?.getTracks().forEach(t => t.stop());
    });

    // 🔹 Capture image and send to backend
    const captureBtn = document.getElementById("o_face_capture");
    captureBtn?.addEventListener("click", async () => {
        const video = document.getElementById("o_face_video");
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL("image/jpeg");

        document.getElementById("o_face_result").innerText = "Scanning...";

        try {
            const result = await jsonrpc("/face_auth/local_login", { image: imageData });
            if (result?.success) {
                document.getElementById("o_face_result").innerText = "✅ Face recognized! Redirecting...";
                window.location.href = "/web";
            } else {
                document.getElementById("o_face_result").innerText = "❌ Face not recognized.";
            }
        } catch (err) {
            console.error(err);
            document.getElementById("o_face_result").innerText = "Error during recognition.";
        }
    });
});
