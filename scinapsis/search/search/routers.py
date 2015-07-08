class SearchDbRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'search':
            return 'search_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'search':
            return 'search_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'search' or obj2._meta.app_label == 'search':
            return True
        return None

    def allow_syncdb(self, db, model):

        if db == 'search_db':
            return model._meta.app_label == 'search'
        elif model._meta.app_label == 'search':
            return False
        return None