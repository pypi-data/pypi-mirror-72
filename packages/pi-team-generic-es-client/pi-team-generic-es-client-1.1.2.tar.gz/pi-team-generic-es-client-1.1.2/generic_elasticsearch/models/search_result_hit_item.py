# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from generic_elasticsearch.configuration import Configuration


class SearchResultHitItem(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'index': 'str',
        'type': 'str',
        'id': 'str',
        'score': 'str',
        'source': 'object'
    }

    attribute_map = {
        'index': '_index',
        'type': '_type',
        'id': '_id',
        'score': '_score',
        'source': '_source'
    }

    def __init__(self, index=None, type=None, id=None, score=None, source=None, local_vars_configuration=None):  # noqa: E501
        """SearchResultHitItem - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._index = None
        self._type = None
        self._id = None
        self._score = None
        self._source = None
        self.discriminator = None

        self.index = index
        self.type = type
        self.id = id
        self.score = score
        self.source = source

    @property
    def index(self):
        """Gets the index of this SearchResultHitItem.  # noqa: E501


        :return: The index of this SearchResultHitItem.  # noqa: E501
        :rtype: str
        """
        return self._index

    @index.setter
    def index(self, index):
        """Sets the index of this SearchResultHitItem.


        :param index: The index of this SearchResultHitItem.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and index is None:  # noqa: E501
            raise ValueError("Invalid value for `index`, must not be `None`")  # noqa: E501

        self._index = index

    @property
    def type(self):
        """Gets the type of this SearchResultHitItem.  # noqa: E501


        :return: The type of this SearchResultHitItem.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this SearchResultHitItem.


        :param type: The type of this SearchResultHitItem.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def id(self):
        """Gets the id of this SearchResultHitItem.  # noqa: E501


        :return: The id of this SearchResultHitItem.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SearchResultHitItem.


        :param id: The id of this SearchResultHitItem.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def score(self):
        """Gets the score of this SearchResultHitItem.  # noqa: E501


        :return: The score of this SearchResultHitItem.  # noqa: E501
        :rtype: str
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this SearchResultHitItem.


        :param score: The score of this SearchResultHitItem.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and score is None:  # noqa: E501
            raise ValueError("Invalid value for `score`, must not be `None`")  # noqa: E501

        self._score = score

    @property
    def source(self):
        """Gets the source of this SearchResultHitItem.  # noqa: E501


        :return: The source of this SearchResultHitItem.  # noqa: E501
        :rtype: object
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this SearchResultHitItem.


        :param source: The source of this SearchResultHitItem.  # noqa: E501
        :type: object
        """
        if self.local_vars_configuration.client_side_validation and source is None:  # noqa: E501
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501

        self._source = source

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SearchResultHitItem):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SearchResultHitItem):
            return True

        return self.to_dict() != other.to_dict()
