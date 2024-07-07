{
    'name': "Account Move Reconcile",

    'summary': """Reconcile invoices by another method""",
    'author': "Tonny Velazquez Juarez",
    'website': "corner.store59@gmail.com",
    'category': 'account',
    'version': '15.0.0.0.10',
    'depends': ['account', 'l10n_latam_base', 'l10n_cl_fe'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_facturacion_conciliacion_views.xml',
        'views/account_move_views.xml',
    ],
    "license": "Other proprietary",
}
