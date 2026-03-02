{
    "name": "MIS Firebase Push Notification",
    "version": "17.0.1.0.0",
    "category": "Tools",
    "summary": "Firebase Push Notification for Android (MIS App)",
    "description": """
Send Firebase push notifications from Odoo 17 to Android apps.
Automatically registers FCM tokens and sends notifications.
""",
    "author": "MIS / Alannia Infotechz",
    "depends": ["base", "web"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/fcm_token_views.xml",
        "views/res_users_views.xml",
    ],
    "installable": True,
    "application": False,
}
