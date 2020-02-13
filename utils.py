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


def get_section_override(overrides, section_id):
    """
    Search the provided overrides for an override matching the provided
    section ID.

    :param overrides: List of assignment overrides to search through
    :type overrides: iterable of :class:`canvasapi.assignment.AssignmentGroup` objects
    :param section_id: The Canvas ID of the section to search for
    :type section_id: int

    :returns: The assignment override for the specified section, if any.
    :rtype: :class:`canvasapi.assignment.AssignmentGroup` or None
    """
    for override in overrides:
        if hasattr(override, 'course_section_id') and override.course_section_id == section_id:
            return override
    return None
