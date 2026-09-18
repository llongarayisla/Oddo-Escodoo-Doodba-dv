{
    "name": "Meu Primeiro Módulo",
    "summary": "Central EPI & Equipamentos com Timeline",
    "author": "isla_longaray",
    "license": "LGPL-3",
    "category": "Human Resources",
    "version": "14.0.1.0.0",
    "depends": [
        "base",
        "stock",
        "hr",
        "hr_employee_ppe",
        "hr_personal_equipment_request",
        "hr_personal_equipment_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/epi_timeline_views.xml",
    ],
    "installable": True,
    "application": True,
}
