# -*- coding: utf-8 -*-

from datetime import datetime

from pytz import timezone

import config


def fix_date(value):
    local_tz = timezone(config.TIME_ZONE)
    try:
        value = datetime.strptime(value, config.LOCAL_TIME_FORMAT)
        value = local_tz.localize(value)
        return value.isoformat()
    except (ValueError, TypeError):
        # Not a valid time. Just ignore.
        return ""


def update_job(job, percent, status_msg, status, error=False):
    """
    Update job status.
    """
    job.meta["percent"] = percent
    job.meta["status"] = status
    job.meta["status_msg"] = status_msg
    job.meta["error"] = error

    job.save()


def get_base_dates(all_dates):
    """
    Extract the base dates for an assignment from a list of all dates.

    :param all_dates: List of dictionaries representing all the dates
        in a course, as returned from a Canvas assignment object.
    :type all_dates: list of dicts

    :returns: A dictionary containing the base dates for the assignment.
    :rtype: dict
    """
    for date in all_dates:
        if date.get("base", False):
            return date
