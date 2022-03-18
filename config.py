import typing
from configer import types
from configer.utils.db_helper import DBHelper


class Config:

    """
    Class for manage static and dynamic params
    """

    def __init__(self,
                 storage_path: str,
                 param_dict: typing.Dict[str, typing.Union[types.StaticParam, types.DynamicParam]] = None,
                 **params: typing.Union[types.StaticParam, types.DynamicParam]):
        """
        Use param_dict if you need to add params with incorrect symbols in their names, else use **params
        :param storage_path: Path, where storage file will be, it should contain filename
        :param param_dict: Var, which is contains params
        :param params: Var, which is contains params
        """
        self._db: DBHelper = DBHelper(storage_path)
        self._params: typing.Dict[typing.Union[types.StaticParam, types.DynamicParam]] = params

        if param_dict:
            self._params.update(param_dict)

        for name in self._params:
            if not self._db.exists(name):
                param = self._params[name]
                self._db.add(
                    name=name,
                    value=param.to_input(param.last_value))


    def __getitem__(self, name: str) -> typing.Any:
        """
        Method for recieveing value of param
        :param name: Name of the param
        :return: The value of param with the name
        """
        return self.get(name)


    def __setitem__(self, name: str, value: typing.Any):
        """
        Method for setting value of the param
        :param name: Name of the param
        :param value: New value for the param
        :return: None
        """
        self.set(name, value)


    def get(self, name: str) -> typing.Any:
        """
        Method for recieveing value of the param
        :param name: Name of the param
        :return: The value of param with the name
        """
        param = self._params.get(name)
        if param:
            value = param.to_output(self._db.get(name)[0])
            param.last_value = value
            return value
        return None


    def set(self, name: str, value: typing.Any):
        """
        Method for setting value of the param
        :param name: Name of the param
        :param value: New value for the param
        :return: None
        """
        param = self._params.get(name)
        if param:
            if isinstance(param, types.DynamicParam):
                self._db.update(name, param.content_type.to_input(value))