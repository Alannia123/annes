# -*- coding: utf-8 -*-
{
    "name": "Face Recognition Login (Local, pgvector)",
    "summary": "Passwordless login by matching webcam face to res.partner photo via pgvector",
    "version": "17.0.1.0.0",
    "author": "Alannia Infotechz",
    "license": "LGPL-3",
    "category": "Authentication",
    "depends": ["base", "web", "auth_signup", 'mis_website'],
    "data": [
        "security/ir.model.access.csv",
        "views/login_inherit.xml",
        "views/res_partner_views.xml",
        "views/face_embedding_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/mis_face_login/static/src/js/face_login.js",
            "/mis_face_login/static/src/css/face_login.css",
        ],
    },
    "post_init_hook": "post_init",
    "uninstall_hook": "uninstall_hook",
    "installable": True,
    "application": False,
}
