from django.apps import AppConfig

class ApplicationPrincipaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application_principale'

    def ready(self):
        # Contournement pour l'erreur de version MariaDB 10.4 vs 10.6 requise par Django 6
        import django.db.backends.base.base
        django.db.backends.base.base.BaseDatabaseWrapper.check_database_version_supported = lambda self: None

        # Contournement pour l'erreur de syntaxe MariaDB avec les requetes RETURNING
        from django.db.backends.mysql.features import DatabaseFeatures
        DatabaseFeatures.can_return_rows_from_bulk_insert = False
        DatabaseFeatures.can_return_columns_from_insert = False
