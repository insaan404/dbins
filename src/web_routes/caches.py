import uuid


class UserCache:

    def __init__(self, api_token: str):
        self._api_token = api_token

    def get_api_token(self):
        return self._api_token
    
    def set_api_token(self, token):
        self._api_token = token
    

class UserCacheRepository:
    def __init__(self, data: dict[uuid.UUID, UserCache]=None):
        self.data = {} if data is None else data

    def get_cache(self, id: uuid.UUID) -> UserCache:
        return self.data.get(id)
    
    def add_cache(self, id: uuid.UUID, cache: UserCache):
        self.data[id] = cache


user_cache_repo = UserCacheRepository()