# -*- coding: utf-8 -*-
import base64, io, numpy as np
import face_recognition
from PIL import Image
from odoo import http
from odoo.http import request

THRESHOLD = 0.45  # Tune: 0.38–0.55 depending on your dataset

class FaceAuthController(http.Controller):

    @http.route("/face_auth/local_login", type="json", auth="public", csrf=False)
    def local_face_login(self, image_b64=None):
        """
        1) Decode webcam frame
        2) Encode face (128-d)
        3) Query pgvector: ORDER BY embedding_vec <-> query LIMIT 1
        4) If distance < THRESHOLD -> login matched user's account
        """
        try:
            if not image_b64:
                return {"ok": False, "error": "No image provided"}

            if image_b64.startswith("data:image"):
                image_b64 = image_b64.split(",", 1)[1]

            img_bytes = base64.b64decode(image_b64)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            np_img = np.array(img)

            encs = face_recognition.face_encodings(np_img)
            if not encs:
                return {"ok": False, "error": "No face detected"}
            query_vec = encs[0].tolist()
            vec_str = "[" + ",".join(str(float(x)) for x in query_vec) + "]"

            cr = request.env.cr
            cr.execute("""
                SELECT fe.partner_id, (fe.embedding_vec <-> %s::vector) AS dist
                  FROM face_embedding fe
                 WHERE fe.active = true
                   AND fe.embedding_vec IS NOT NULL
                 ORDER BY fe.embedding_vec <-> %s::vector
                 LIMIT 1
            """, (vec_str, vec_str))
            row = cr.fetchone()
            if not row:
                return {"ok": False, "message": "No enrolled faces"}

            partner_id, distance = int(row[0]), float(row[1])
            if distance >= THRESHOLD:
                return {"ok": False, "message": f"No match (distance {distance:.3f})"}

            partner = request.env["res.partner"].sudo().browse(partner_id)
            user = partner.user_ids[:1].sudo()
            if not user:
                return {"ok": False, "message": "Matched partner has no user"}

            # Create Odoo session (login user)
            request.session.uid = user.id
            request.session.login = user.login
            request.session.session_token = request.session._generate_session_token()
            request.env.cr.commit()

            return {"ok": True, "redirect": "/web", "user": user.name, "distance": round(distance, 4)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
