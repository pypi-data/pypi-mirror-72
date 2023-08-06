import json
from datetime import datetime, timedelta

import bson
import pytz
from bson import SON, iteritems, text_type, EPOCH_AWARE, DBRef, Code

try:
    json.loads("{}", object_pairs_hook=dict)
    _HAS_OBJECT_PAIRS_HOOK = True
except TypeError:
    _HAS_OBJECT_PAIRS_HOOK = False

from bson.json_util import (
    DEFAULT_JSON_OPTIONS,
    default,
    object_hook,
    _parse_canonical_datetime,
    DatetimeRepresentation,
)
from bson.tz_util import FixedOffset


def _bson_timezone_default(obj, json_options):
    """
    Parses all existing types exactly like ~bson.json_util.default but dumps
    datetimes in a timezone aware way
    """
    result = default(obj, json_options)
    if isinstance(obj, DBRef):
        # This needs to call the timezone aware _json_convert method in case
        # there are further nested datetimes
        return _bson_timezone_json_convert(
            obj.as_doc(), json_options=json_options
        )
    if isinstance(obj, Code):
        # This needs to call the timezone aware _json_convert method in case
        # there are further nested datetimes
        if obj.scope is None:
            return {"$code": str(obj)}
        return SON(
            [
                ("$code", str(obj)),
                (
                    "$scope",
                    _bson_timezone_json_convert(obj.scope, json_options),
                ),
            ]
        )
    if isinstance(obj, datetime):
        if (
            json_options.datetime_representation
            == DatetimeRepresentation.ISO8601
        ):
            if obj.tzinfo and obj >= EPOCH_AWARE:
                _millis = int(obj.microsecond / 1000)
                _fracsecs = ".%03d" % (_millis,) if _millis else ""
                return {
                    "$date": "%s%s"
                    % (obj.strftime("%Y-%m-%dT%H:%M:%S"), _fracsecs),
                    "$zone": obj.tzinfo.zone,
                    # Offset data is stored in the `zone`
                    "$offset": None,
                }

        millis = bson._datetime_to_millis(obj)
        offset = None
        if obj.utcoffset():
            # Store the offset to allow handling of DST when converting the
            # naive timestamp to a TZ aware timestamp
            offset = {"total_seconds": obj.utcoffset().total_seconds()}

        if (
            json_options.datetime_representation
            == DatetimeRepresentation.LEGACY
        ):
            return {
                "$date": millis,
                "$zone": getattr(obj.tzinfo, "zone", None),
                "$offset": offset,
            }
        # Handles `NUMBER_LONG` and TZ naive ISO8601 timestamps
        return {
            "$date": {"$numberLong": str(millis)},
            "$zone": getattr(obj.tzinfo, "zone", None),
            "$offset": offset,
        }
    return result


def _bson_timezone_json_convert(obj, json_options=DEFAULT_JSON_OPTIONS):
    """Recursive helper method that converts BSON types so they can be
    converted into json.  This is copied verbatim from
    ~bson.json_util._json_convert but calls a different `default` function
    to handle timezone aware datetimes
    """
    if hasattr(obj, "iteritems") or hasattr(obj, "items"):  # PY3 support
        return SON(
            (
                (k, _bson_timezone_json_convert(v, json_options))
                for k, v in iteritems(obj)
            )
        )
    elif hasattr(obj, "__iter__") and not isinstance(obj, (text_type, bytes)):
        return list((_bson_timezone_json_convert(v, json_options) for v in obj))
    try:
        return _bson_timezone_default(obj, json_options)
    except TypeError:
        return obj


def _bson_timezone_parse_canonical_datetime(doc, json_options, *args, **kwargs):
    """
    Parses $date objects in a timezone aware manner.   Uses the base
    ~bson.json_util._parse_canonical_datetime to first parse the datetime,
    then extra timezone information is added that is stored as part of
    `~bson_timezone.bson_tz_dumps`
    """
    zone = doc.pop("$zone")
    offset = doc.pop("$offset")
    dt = _parse_canonical_datetime(doc, json_options)
    if not dt.tzinfo or isinstance(dt.tzinfo, FixedOffset):
        dt = dt.replace(tzinfo=None)
        if zone:
            tz = pytz.timezone(zone)

            if offset:
                dt = dt + timedelta(seconds=offset["total_seconds"])
            dt = tz.localize(dt)
    return dt


def bson_timezone_object_hook(dct, *args, **kwargs):
    """
    An object hook that mirrors ~bson.json_util.object_hook but handles $date
    fields in a timezone aware manner.  Any other type gets handled by the
    based ~bson.json_util.object_hook function
    """
    if "$date" in dct:
        return _bson_timezone_parse_canonical_datetime(dct, *args, **kwargs)
    return object_hook(dct, *args, **kwargs)


def bson_timezone_object_pairs_hook(pairs, json_options=DEFAULT_JSON_OPTIONS):
    """
    An object hook that mirrors ~bson.json_util.object_pairs_hook but handles
    $date fields in a timezone aware manner.  Any other type gets handled by
    the based ~bson.json_util.object_hook function
    """
    return bson_timezone_object_hook(
        json_options.document_class(pairs), json_options
    )


def _bson_loads_kwargs(*args, **kwargs):
    """
    The kwargs provided to `bson_tz_loads`.  Separated out for easier use
    with external packages (i.e `requests`).
    """
    json_options = kwargs.pop("json_options", DEFAULT_JSON_OPTIONS)
    if _HAS_OBJECT_PAIRS_HOOK:
        kwargs[
            "object_pairs_hook"
        ] = lambda pairs: bson_timezone_object_pairs_hook(pairs, json_options)
    else:
        kwargs["object_hook"] = lambda obj: bson_timezone_object_hook(
            obj, json_options
        )
    return kwargs


def bson_tz_loads(s, *args, **kwargs):
    """Helper function that wraps :func:`json.loads`.

    Automatically passes the object_hook for BSON type conversion and handles
    timezone aware datetimes

    Raises ``TypeError``, ``ValueError``, ``KeyError``, or
    :exc:`~bson.errors.InvalidId` on invalid MongoDB Extended JSON.

    :Parameters:
      - `json_options`: A :class:`JSONOptions` instance used to modify the
        decoding of MongoDB Extended JSON types. Defaults to
        :const:`DEFAULT_JSON_OPTIONS`.
    """
    return json.loads(s, *args, **_bson_loads_kwargs(*args, **kwargs))


def bson_tz_dumps(obj, *args, **kwargs):
    """Helper function that wraps :func:`json.dumps`.

    Recursive function that handles all BSON types including
    :class:`~bson.binary.Binary` and :class:`~bson.code.Code`.  Handles
    timezone aware datetimes if given in a format output from `bson_tz_loads`

    :Parameters:
      - `json_options`: A :class:`JSONOptions` instance used to modify the
        encoding of MongoDB Extended JSON types. Defaults to
        :const:`DEFAULT_JSON_OPTIONS`.
    """
    json_options = kwargs.pop("json_options", DEFAULT_JSON_OPTIONS)
    return json.dumps(
        _bson_timezone_json_convert(obj, json_options), *args, **kwargs
    )
