from db_models_base import DBModel

class DBPersistence(metaclass=DBModel, metaattr=['key', 'value']): pass
class DBUpdateChannel(metaclass=DBModel, metaattr=['server_id', 'channel_id']): pass