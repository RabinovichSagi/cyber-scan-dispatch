class MockCache:
    def put(self, key, value):
        pass

    def get(self, key):
        '''

        returns value from cache or None if not exists

        :param key:
        :return:
        '''
        return None

    def invalidate(self, key):
        pass