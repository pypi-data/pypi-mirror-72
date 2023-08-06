from django.conf import settings


class DjangoCoreRouter:
    """
    A router to control all database operations on models in the
    calc application.
    """

    route_app_labels = {
        'auth', 'users', 'contenttypes', 'sessions', 'messages',
        'staticfiles', 'sites',
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read user models go to django_core_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'django_core_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write user models go to django_core_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'django_core_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the user app is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'django_core_db'
        database.
        """
        if app_label in self.route_app_labels:
            return db == 'django_core_db'
        return False
