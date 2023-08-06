#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
import functools

__project_ = 'bzjsons'
__file_name__ = 'bzjsons'
__author__ = 'bright.zhang'
__time__ = '2020/6/21 9:31'
__version__ = '0.0.5'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


# datetime / date serialization support.
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        global DATETIME_FORMAT, DATE_FORMAT
        if isinstance(obj, datetime):
            return obj.strftime(DATETIME_FORMAT)
        elif isinstance(obj, date):
            return obj.strftime(DATE_FORMAT)
        else:
            return json.JSONEncoder.default(self, obj)


# The entry of json serialization / deserialization instead of built-in json.
class Jsoner:
    # Public entry method for user to dumps object into json string (serialization).
    # To keep accordance to json serialization in other main languages, like fastjson/java etc.,
    # the parameter: ensure_ascii is set to False as its default value.
    # When unicode characters like Chinese is used, then these characters will be shown normally instead of bytes.
    # If in some cases ascii is required, you can set it to True explicitly.
    @staticmethod
    def dumps(obj, *, skipkeys=False, ensure_ascii=False, check_circular=True,
              allow_nan=True, indent=None, separators=None,
              default=None, sort_keys=False, **kw):
        json.dumps = functools.partial(json.dumps, cls=DateTimeEncoder)
        dict_ = Jsoner._to_dict(obj)
        return json.dumps(dict_,
                          skipkeys=skipkeys,
                          ensure_ascii=ensure_ascii,
                          check_circular=check_circular,
                          allow_nan=allow_nan,
                          indent=indent,
                          separators=separators,
                          default=default,
                          sort_keys=sort_keys,
                          **kw)

    # loads is just encapsulation of json.loads directly, which purpose is to keep accordance to built-in json.
    # The json string will be loaded as dict.
    @staticmethod
    def loads(s, *, cls=None, object_hook=None, parse_float=None,
              parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
        return json.loads(s, cls=cls,
                          object_hook=object_hook,
                          parse_float=parse_float,
                          parse_int=parse_int,
                          parse_constant=parse_constant,
                          object_pairs_hook=object_pairs_hook, **kw)

    # Public entry method for user to loads json string into instance (deserialization).
    @staticmethod
    def loads_as_instance(s, *, cls=None, **kw):
        d = json.loads(s)
        if cls is None:
            return d
        c = Jsoner._loads_object(d, cls=cls, **kw)
        return c

    # Check if the obj is of basic type, including python base types and datetime, date.
    @staticmethod
    def _is_basic_data_type(obj):
        value_type = type(obj)
        return value_type in (int, str, float, datetime, date, bool, None)

    # Check if the obj is of collection types, such as list, tuple, set and dict.
    @staticmethod
    def _is_collection_type(obj):
        value_type = type(obj)
        return value_type in (list, tuple, set, dict)

    # check if obj is the instance of a simple customized class,
    # which means no nested references to other customized classes, and is NOT of collection type.
    @staticmethod
    def _is_simple_class_object(obj):
        if type(obj) in (list, tuple, dict, set):
            return False
        if not hasattr(obj, '__dict__'):
            return False
        for k, v in obj.__dict__.items():
            if not Jsoner._is_basic_data_type(v):
                return False
        return True

    # Corresponding to simple_class_object, complex_class_object means references to other customized classes exist.
    @staticmethod
    def _is_complex_class_object(obj):
        if Jsoner._is_basic_data_type(obj):
            return False
        elif Jsoner._is_collection_type(obj):
            return False
        elif Jsoner._is_simple_class_object(obj):
            return False
        else:
            return True

    # Convert to dict recursively before dumps.
    # This is the core of dumps in Jsoner.
    @staticmethod
    def _to_dict(obj):
        if obj is None:
            return None
        elif isinstance(obj, dict):
            return obj
        elif Jsoner._is_basic_data_type(obj):
            return obj
        elif Jsoner._is_simple_class_object(obj):
            return obj.__dict__
        elif Jsoner._is_collection_type(obj):
            sub_dict_list = []
            for sub in obj:
                sub_dict = Jsoner._to_dict(sub)
                sub_dict_list.append(sub_dict)
            return sub_dict_list
        elif Jsoner._is_complex_class_object(obj):
            # for complicated class, recursion is required for its complex attributes.
            obj_dict = dict()
            for k, v in obj.__dict__.items():
                # bug fixed: AttributeError: 'getset_descriptor' object has no attribute '__dict__'
                # if k is internal attribute, then continue.
                if str(k).startswith('_'):
                    continue
                if Jsoner._is_simple_class_object(v):
                    obj_dict[k] = v.__dict__
                else:
                    sub_dict = Jsoner._to_dict(v)
                    obj_dict[k] = sub_dict
            return obj_dict
        else:
            print('The obj is not supported when converted to dict:')
            print(obj)  # print to the console.
            raise AttributeError('The object is not supported, please try to extend Jsoner, thanks.')

    # Loads dict to instance recursively.
    # This is the core of loads_as_instance of Jsoner.
    @staticmethod
    def _loads_object(loads_data, cls, **kw):
        if isinstance(loads_data, dict):
            try:
                obj = cls()
            except TypeError:
                raise Exception('%s\'s __init__() should support param-less construction.' % cls.__name__)
            for k, v in loads_data.items():
                # if k is internal members and start with underscore(s), it will continue.
                if str(k).startswith('_'):
                    continue
                if Jsoner._is_basic_data_type(v):
                    # 检查是否datetime / date
                    if isinstance(v, str):
                        is_dt, dt = Jsoner._is_datetime_str(v)
                        if is_dt:
                            obj.__setattr__(k, dt)
                            continue
                        is_d, loads_data = Jsoner._is_date_str(v)
                        if is_d:
                            obj.__setattr__(k, loads_data)
                            continue
                    obj.__setattr__(k, v)
                elif isinstance(v, dict):
                    v_type = Jsoner._get_attr_type(k, **kw)
                    if v_type is not None:
                        dict_attribute = Jsoner._loads_object(v, v_type, **kw)
                        obj.__setattr__(k, dict_attribute)
                    else:
                        # if a dict is used in a customized class instead of dedicated class, it will leads to error here.
                        # so if no classes specified in **kw, dict would be taken instead.
                        # raise AttributeError(
                        #     "the attribute: %s\'s type is not clear, please make sure it\'s prepared in the **kw." % k)
                        obj.__setattr__(k, v)
                elif isinstance(v, list):
                    list_attribute = []
                    inner_obj_type = Jsoner._get_attr_type(k, **kw)
                    # Please be attention: dict list is not supported. in other word, if list exists here, it must be a dedicated class referenced in it.
                    # because of dynamic feature of Python, it's a convention.
                    if inner_obj_type is None:
                        raise AttributeError("the attribute: %s\'s inner type is not clear." % k)
                    for sub_item in v:
                        sub_obj = Jsoner._loads_object(sub_item, inner_obj_type, **kw)
                        list_attribute.append(sub_obj)
                    obj.__setattr__(k, list_attribute)
            return obj
        elif isinstance(loads_data, list):
            # because all collections will be dumped as '[]', so it's a list here.
            # TODO: if tuple / dict / set is used in your customized classes, this needs more process here.
            result_list = []
            for d_item in loads_data:
                d_obj = Jsoner._loads_object(d_item, cls, **kw)
                result_list.append(d_obj)
            return result_list
        else:
            print('The dict data is not supported when loaded to object:')
            print(loads_data)  # print to the console.
            raise AttributeError('The dict is not supported, please try to extend Jsoner, thanks.')

    @staticmethod
    def _get_attr_type(attr_name, **kw):
        # get the attribute's type from **kw
        if attr_name in kw.keys():
            return kw[attr_name]
        return None

    # Check if the string is of date format. If YES, then it will be treated as a date.
    @staticmethod
    def _is_date_str(s):
        # check if s is a valid date string.
        try:
            global DATE_FORMAT
            d = datetime.strptime(s, DATE_FORMAT).date()
            return True, d
        except:
            return False, None

    # Check if the string is of datetime format. If YES, then it will be treated as a datetime.
    @staticmethod
    def _is_datetime_str(s):
        # check if s is a valid datetime string.
        try:
            global DATETIME_FORMAT
            dt = datetime.strptime(s, DATETIME_FORMAT)
            return True, dt
        except:
            return False, None
