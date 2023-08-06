import json

from isc_common.http.RPCRequest import RPCRequest


class RequestData:
    def __init__(self, _dict=None, request=None):
        if request:
            self.__data_dict__ = request.get_data()
        elif _dict:
            self.__data_dict__ = _dict
        else:
            self.__data_dict__ = dict()
        super()

    def getDataOfKey(self, key, default=None):
        return self.__data_dict__.get(key, default)

    def update(self, key, value):
        self.__data_dict__.update((key, value))
        return RequestData(self.__data_dict__)

    def getDataWithOutField(self, list_fields):
        if isinstance(list_fields, list):
            return RequestData({key: self.__data_dict__[key] for key in self.__data_dict__ if not key in list_fields})
        else:
            return RequestData(self.__data_dict__)

    def getDataNotContain(self, *sub_strs):
        res = RequestData()
        for sub in sub_strs:
            self.__data_dict__ = {key: self.__data_dict__[key] for key in self.__data_dict__ if not str(key).__contains__(sub)}
        return RequestData(self.__data_dict__)

    def dict(self):
        return self.__data_dict__


class DSRequest(RPCRequest):
    startRow = None
    endRow = None

    def __init__(self, request):
        if request and isinstance(request.body, bytes):
            try:
                bodyStr = request.body.decode("utf-8")
                self.json = json.loads(bodyStr)
            except:
                self.json = None

            RPCRequest.__init__(self, self.json)

    def get_data(self, excluded_keys=['grid']):
        res = None
        if isinstance(self.json, dict):
            if self.json.get('data', None) and isinstance(self.json.get('data', None), dict):
                res = self.json.get('data')
            else:
                res = self.json

            res = dict((key, value) for (key, value) in res.items() if value is not None and not str(key).startswith('_') and key not in excluded_keys)
            # res = dict((key, value) for (key, value) in res.items() if value is not None and key not in excluded_keys)
        return res

    def get_oldValues(self, excluded_keys=['grid']):
        res = None
        if isinstance(self.json, dict):
            if self.json.get('oldValues', None) and isinstance(self.json.get('oldValues', None), dict):
                res = self.json.get('oldValues')
            else:
                res = self.json

            res = dict((key, value) for (key, value) in res.items() if value is not None and not str(key).startswith('_') and key not in excluded_keys)
        return res

    def get_id(self):
        return self.get_data().get('id', self.get_oldValues().get('id'))
