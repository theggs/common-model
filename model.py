import traceback


class CommonModel(object):
    def __init__(self, json_dict):
        self._obj_from_json(json_dict)

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
        mapper = self.key_mapper()
        print('mapper', mapper)
        for k, v in mapper.items():
            try:
                paths = v.split('.')
                v = self._parser(json_obj)
                for p in paths:
                    v = v[p]
            except Exception as e:
                print(e)
                traceback.print_exc()
                v = None
            setattr(self, k, v)


# example
class User(CommonModel):
    def key_mapper(self):
        mapper = {
            'id': 'id',
            'name': 'name',
            'real_name': 'profile.real_name',
        }
        return mapper
