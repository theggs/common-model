import traceback


class CommonModel(object):
    def __init__(self, raw_input):
        obj = self._parser(raw_input)
        self._obj_from_json(obj)

    def __repr__(self):
        # properties = json.dumps(self.__dict__, sort_keys=True, indent=2)
        # return "<{0}: {1}>".format(self.__class__.__name__, properties)
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def _parser(self, raw_input):
        return raw_input

    def key_mapper(self):
        """Force subclasses to implement this method"""
        raise NotImplementedError

    def _obj_from_json(self, json_obj):
        """Private method"""
        def _default_handler(v):
            paths = v.split('.')
            v = json_obj
            for p in paths:
                v = v[p]
            return v

        def _obj_handler(v):
            assert len(v) == 2
            model = v[0]
            assert issubclass(model, CommonModel)
            value = v[1]
            assert isinstance(value, str)
            arg = _default_handler(value)
            return model(arg)

        def _list_obj_handler(v):
            result_list = []
            assert len(v) == 2
            model = v[0]
            assert issubclass(model, CommonModel)
            value = v[1]
            assert isinstance(value, str)
            arg_list = _default_handler(value)
            for arg in arg_list:
                result_list.append(
                    model(arg)
                )
            return result_list

        handler_map = {
            str: _default_handler,
            tuple: _obj_handler,
            list: _list_obj_handler,
        }

        mapper = self.key_mapper()
        for k_, v_ in mapper.items():
            try:
                handler = handler_map[type(v_)]
                final_value = handler(v_)
            except Exception as e:
                print(e)
                traceback.print_exc()
                final_value = None
            setattr(self, k_, final_value)
