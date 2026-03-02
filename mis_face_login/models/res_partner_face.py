# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    face_enabled = fields.Boolean("Enable Face Login", default=False)
    embedding_ids = fields.One2many("face.embedding", "partner_id", string="Embeddings")

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if vals.get("face_enabled"):
            rec._rebuild_embedding()
        return rec

    def write(self, vals):
        res = super().write(vals)
        if "image_1920" in vals or "face_enabled" in vals:
            for rec in self:
                if rec.face_enabled:
                    rec._rebuild_embedding()
        return res

    def _rebuild_embedding(self):
        Emb = self.env["face.embedding"].sudo()
        for p in self:
            Emb.create_or_update_for_partner(p)
