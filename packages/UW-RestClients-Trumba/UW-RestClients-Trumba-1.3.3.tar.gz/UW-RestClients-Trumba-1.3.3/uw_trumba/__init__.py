"""
This module directly interacts with campus specific web services on
It will log the http requests and responses.
Be sure to set the logging configuration if you use the LiveDao!
"""

import logging
import json
import time
from lxml import etree
from icalendar import Calendar, Event
from restclients_core.exceptions import DataFailureException
from uw_trumba.dao import (
    TrumbaBot_DAO, TrumbaSea_DAO, TrumbaTac_DAO, TrumbaCalendar_DAO)

logger = logging.getLogger(__name__)
TrumbaCalendar = TrumbaCalendar_DAO()
TrumbaBot = TrumbaBot_DAO()
TrumbaSea = TrumbaSea_DAO()
TrumbaTac = TrumbaTac_DAO()


def get_calendar_by_name(calendar_name):
    url = "/calendars/{0}.ics".format(calendar_name)

    response = TrumbaCalendar.getURL(url)

    if response.status != 200:
        raise DataFailureException(url, response.status, str(response.data))

    try:
        calendar = Calendar.from_ical(response.data)
    except Exception as ex:
        # turn data errors (ie, UnicodeEncodeError) into
        # DataFailureException
        raise DataFailureException(url, 503, ex)

    return calendar


def _log_xml_resp(campus, url, response):
    if response.status == 200 and response.data is not None:
        root = etree.fromstring(response.data)
        resp_msg = ''
        for el in root.iterchildren():
            resp_msg += str(el.attrib)
        logger.debug({'campus': campus,
                      'url': url,
                      'resp': resp_msg})
    else:
        logger.error({'campus': campus,
                      'url': url,
                      'status': response.status,
                      'reason': response.reason})


def _log_json_resp(campus, url, body, response):
    if response.status == 200 and response.data is not None:
        logger.debug({'campus': campus,
                      'url': url,
                      'resp': response.data})
    else:
        logger.error({'campus': campus,
                      'url': url,
                      'body': body,
                      'status': response.status,
                      'reason': response.reason})


def get_bot_resource(url):
    """
    Get the requested resource or update resource using Bothell account
    :returns: http response with content in xml
    """
    response = None
    response = TrumbaBot.getURL(url, {"Content-Type": "application/xml"})
    _log_xml_resp("Bothell", url, response)
    return response


def get_sea_resource(url):
    """
    Get the requested resource or update resource using Seattle account
    :returns: http response with content in xml
    """
    response = None
    response = TrumbaSea.getURL(url, {"Accept": "application/xml"})
    _log_xml_resp("Seattle", url, response)
    return response


def get_tac_resource(url):
    """
    Get the requested resource or update resource using Tacoma account
    :returns: http response with content in xml
    """
    response = None
    response = TrumbaTac.getURL(url, {"Accept": "application/xml"})
    _log_xml_resp("Tacoma", url, response)
    return response


def post_bot_resource(url, body):
    """
    Get the requested resource of Bothell calendars
    :returns: http response with content in json
    """
    response = None
    response = TrumbaBot.postURL(
        url, {"Content-Type": "application/json"}, body)
    _log_json_resp("Bothell", url, body, response)
    return response


def post_sea_resource(url, body):
    """
    Get the requested resource using the Seattle account
    :returns: http response with content in json
    """
    response = None
    response = TrumbaSea.postURL(
        url, {"Content-Type": "application/json"}, body)
    _log_json_resp("Seattle", url, body, response)
    return response


def post_tac_resource(url, body):
    """
    Get the requested resource of Tacoma calendars
    :returns: http response with content in json
    """
    response = None
    response = TrumbaTac.postURL(
        url, {"Content-Type": "application/json"}, body)
    _log_json_resp("Tacoma", url, body, response)
    return response
