# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64, io
import numpy as np
import face_recognition
from PIL import Image

class FaceEmbedding(models.Model):
    _name = "face.embedding"
    _description = "Face encodings cached for pgvector search"
    _table = "face_embedding"  # explicit to match hooks
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade", index=True)
    encoding_json = fields.Text("Face Encoding (JSON Array)")  # JSON-like string "[...]"
    active = fields.Boolean(default=True)
    note = fields.Char("Note")

    _sql_constraints = [
        ('unique_partner_embedding', 'unique(partner_id)',
         'Each partner may have only one face embedding.'),
    ]

    @api.model
    def _encode_from_partner(self, partner):
        """Return 128-d list (or None) from partner.image_1920."""
        if not partner.image_1920:
            return None
        try:
            img_data = base64.b64decode(partner.image_1920)
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
            np_img = np.array(img)
            encs = face_recognition.face_encodings(np_img)
            if not encs:
                return None
            return encs[0].tolist()
        except Exception:
            return None

    @api.model
    def create_or_update_for_partner(self, partner):
        vec = self._encode_from_partner(partner)
        if not vec:
            return None
        rec = self.sudo().search([("partner_id", "=", partner.id)], limit=1)
        j = str(vec)  # "[...]"
        if rec:
            rec.sudo().write({"encoding_json": j, "active": True})
        else:
            rec = self.sudo().create({
                "partner_id": partner.id,
                "encoding_json": j,
                "note": "Generated from res.partner.image_1920",
            })
        # Keep pgvector column in sync
        self.env.cr.execute("""
            UPDATE face_embedding SET embedding_vec = (%s)::vector WHERE id = %s
        """, (j, rec.id))
        return rec

    def action_rebuild_selected(self):
        for rec in self:
            self.create_or_update_for_partner(rec.partner_id)
