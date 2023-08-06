from datetime import datetime, timezone, timedelta
from enum import Enum
import operator
import hashlib
from typing import Union

import html2text
import requests
from mastodon import Mastodon  # type: ignore

"""
An Enum containing types of comparisons that can be used to check Criterion.
"""
Comparison = Enum("Comparison", "GT GE LT LE EQ NE")

"""
A dict mapping each Comparison to a function that takes two arguments and returns a boolean as a result of the comparison.
"""
COMP_FUNCTIONS = {
    Comparison.GT: operator.gt,
    Comparison.GE: operator.ge,
    Comparison.LT: operator.lt,
    Comparison.LE: operator.le,
    Comparison.EQ: operator.eq,
    Comparison.NE: operator.ne,
}


class Criterion:
    """
    A defined Criterion on which to reject a follow request.

    Attributes
    ----------
    comparison_type : Comparison
        A member of the `Comparison` enum defining what type of comparison this `Criterion` will evaluate on.
    user_dict_key : str
        The key in a Mastodon.py user dict that denotes the value to compare to. See here for details: https://mastodonpy.readthedocs.io/en/stable/#user-dicts
        Note that you can also modify the user dict to add extra keys/values, which can also be specified as a key here. This is done by the default defined criteria
        to support `min_age` and `has_avatar`, for instance.

    Methods
    -------

    check(use_dict, check_value)
        Check whether a given user dict passes the Crtierion with the value (`check_value`) to compare against.
    """

    def __init__(self, comparison_type: Comparison, user_dict_key: str):
        self.comparison_type = comparison_type
        self.user_dict_key = user_dict_key

    TestValue = Union[str, dict, timedelta]

    """
    Checks whether the Criterion passed given a `user_dict` to take the value from, and compares against the `check_value`.

    Parameters
    ----------
    user_dict : dict
        The user dict from which to get the value to compare from. The method will use the Criterion object's `user_dict_key` to get the value.
    
    check_value : Value to compare against. For instance, if it's a `Comparison.GE` comparison, `check` will return True if the value from the `user_dict` >= `check_value`.

    Returns
    -------
    bool
        Whether the comparison passed (True) or failed (False)
    """

    def check(self, user_dict: dict, check_value: TestValue):
        user_value = user_dict[self.user_dict_key]

        return COMP_FUNCTIONS[self.comparison_type](user_value, check_value)


"""
The default-defined criteria. All these keys can be used in a dict containing the values to check the user against.
"""
CRITERIA = {
    "min_age": Criterion(Comparison.GE, "account_age"),
    "min_follows": Criterion(Comparison.GE, "following_count"),
    "min_followers": Criterion(Comparison.GE, "followers_count"),
    "max_follows": Criterion(Comparison.LE, "following_count"),
    "max_followers": Criterion(Comparison.LE, "followers_count"),
    "has_bio": Criterion(Comparison.EQ, "has_bio"),
    "no_bots": Criterion(Comparison.NE, "bot"),
    "has_avatar": Criterion(Comparison.EQ, "has_avatar"),
    "min_posts": Criterion(Comparison.GE, "statuses_count"),
    "max_posts": Criterion(Comparison.LE, "statuses_count")
}

"""
A list of MD5 hashes corresponding to possible default profile pictures used by various fediverse software.
"""
DEFAULT_AVATAR_HASHES = [
    "eeaef47cc60d52c0f50edfa2bfae1388",  # Mastodon's missing.png
    "de7b5ead3476d53f3b943779699b7fa0"  # Pleroma's avi.png
]


def check_criteria(user_dict: dict, criteria_settings: dict) -> list:
    """
    Check an account against a set of criteria for auto-rejection.

    Parameters
    ----------
    user_dict : dict
        A user dict as returned directly from Mastodon.py, without modification.
        See here: https://mastodonpy.readthedocs.io/en/stable/#user-dicts
    criteria_settings : dict
        A dict containing settings for the criteria that the request will be checked against.

    Returns
    -------
    list of str
        A list of criteria that the account was rejected on. The values in the list are the keys from the `criteria_settings` dict for which a criteria failed.
    """
    # Initialize the rejected criteria as an empty list. If it stays empty, the user wasn't rejected.
    rejected_criteria = []

    created_date = user_dict["created_at"]
    now = datetime.now(timezone.utc)
    account_age = now - created_date

    # Add the user's account age to the dict
    user_dict["account_age"] = account_age

    note_text = html2text.html2text(user_dict["note"]).strip()

    # Add whether the user has a bio to the dict
    # this will be False if note_text is empty.
    user_dict["has_bio"] = bool(note_text)

    # Fetch the user's avatar and MD5 hash it for comparing with default avatars.
    r = requests.get(user_dict["avatar"], stream=True)
    r.raw.decode_content = True
    m = hashlib.md5()
    m.update(r.content)

    # Add a value to the dictionary corresponding to if the user's avatar is a default one.
    user_dict["has_avatar"] = not (m.hexdigest() in DEFAULT_AVATAR_HASHES)

    for key, value in criteria_settings.items():
        criterion = CRITERIA[key]

        passed = criterion.check(user_dict, value)

        if not passed:
            rejected_criteria.append(key)

    return rejected_criteria


def reject_follows(masto: Mastodon, criteria_settings: dict):
    """
    Performs automatic follow request rejection based on a set of criteria.

    Parameters
    ----------
    masto : Mastodon 
        An instance of mastodon.py's Mastodon class that is logged into an account.
    criteria_settings : dict 
        A dict containing settings for the criteria that the request will be checked against.
    """
    follow_requests = masto.follow_requests()

    rejections = []

    for req in follow_requests:
        rejected_on = check_criteria(req, criteria_settings)
        if rejected_on:
            masto.follow_request_reject(req['id'])
            req['rejected_on'] = rejected_on
            rejections.append(req)

    return rejections
