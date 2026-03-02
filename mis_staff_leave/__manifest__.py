{
    "name": "School Staff Leave Management",
    "version": "1.0",
    "category": "School",
    "summary": "Staff Leave Request & Principal Approval",
    "author": "Alannia Infotechz",
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/staff_leave_views.xml",
        "views/menu.xml",
    ],
    "application": True,
    "installable": True,
}
