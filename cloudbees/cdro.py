# coding=utf-8
import logging

from .rest_client import CloudBeesRestAPI

log = logging.getLogger(__name__)


class CDRO(CloudBeesRestAPI):
    def __init__(self, url, *args, **kwargs):
        super(CDRO, self).__init__(url, *args, **kwargs)

    def get_groups(self, filter=None, includeAll=None, maximum=None, sortOrder=None):
        """
        REST endpoint for searching groups in a group.
        :param filter: str
        :param exclude: str
        :param limit: int
        :return: Returned even if no groups match the given substring
        """
        url = self.resource_url("groups")
        params = {}
        if filter:
            params["filter"] = filter
        if includeAll:
            params["includeAll"] = includeAll
        if maximum:
            params["maximum"] = maximum
        if sortOrder:
            params["sortOrder"] = sortOrder
        return self.get(url, params=params)
