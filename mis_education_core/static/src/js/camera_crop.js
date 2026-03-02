/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useRef, onMounted, onWillUnmount, useState } from "@odoo/owl";

export class CameraCropDialog extends Component {

    setup() {
        this.videoRef = useRef("video");
        this.canvasRef = useRef("canvas");

        this.state = useState({
            facingMode: "environment", // default back camera
        });

        this.cropper = null;
        this.stream = null;

        onMounted(() => {
            this.startCamera();
        });

        onWillUnmount(() => {
            this.stopCamera();
        });
    }

    async startCamera() {
        this.stopCamera();

        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: this.state.facingMode },
            });

            this.videoRef.el.srcObject = this.stream;
        } catch (error) {
            console.error("Camera access denied:", error);
            alert("Unable to access camera.");
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
    }

    switchCamera() {
        this.state.facingMode =
            this.state.facingMode === "environment"
                ? "user"
                : "environment";

        this.startCamera();
    }

    cancel() {
        this.stopCamera();
        if (this.cropper) {
            this.cropper.destroy();
            this.cropper = null;
        }
        this.props.close();
    }

    captureImage() {
        const video = this.videoRef.el;
        const canvas = this.canvasRef.el;
        const ctx = canvas.getContext("2d");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);

        this.stopCamera();
        video.style.display = "none";

        const image = document.createElement("img");
        image.src = canvas.toDataURL("image/png");
        image.style.maxWidth = "100%";
        image.style.marginTop = "10px";

        video.parentNode.appendChild(image);

        if (!window.Cropper) {
            alert("Cropper not loaded.");
            return;
        }

        this.cropper = new window.Cropper(image, {
            aspectRatio: 1,
            viewMode: 1,
            autoCropArea: 1,
            responsive: true,
        });
    }

    async saveImage() {
        if (!this.cropper) {
            alert("Please capture image first.");
            return;
        }

        const croppedCanvas = this.cropper.getCroppedCanvas({
            width: 500,
            height: 500,
        });

        const base64 = croppedCanvas.toDataURL("image/png").split(",")[1];

        try {
            await this.env.services.orm.write(
                this.props.model,
                [this.props.record_id],
                { [this.props.field_name]: base64 }
            );

            this.env.services.notification.add("Image saved successfully", {
                type: "success",
            });

            this.cancel();

            // Reload form properly
            this.env.services.action.doAction({
                type: "ir.actions.act_window",
                res_model: this.props.model,
                res_id: this.props.record_id,
                views: [[false, "form"]],
                target: "current",
            });

        } catch (error) {
            console.error(error);
            alert("Failed to save image.");
        }
    }
}

CameraCropDialog.template = "mis_education_core.CameraCropTemplate";

registry.category("actions").add("open_camera_widget", (env, action) => {
    env.services.dialog.add(CameraCropDialog, {
        model: action.params.model,
        record_id: action.params.record_id,
        field_name: action.params.field_name,
    });
});