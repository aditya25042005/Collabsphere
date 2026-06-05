import re
from firebase_admin import auth


def transform_email(username: str):
    """
    Convert a college e-mail username like '21bcs0042@iiitk.ac.in'
    into a canonical roll-number string '2021BCS0042'.
    Returns None when the pattern does not match.
    """
    username = username.split("@")[0]
    match = re.search(r"(\d{2})([a-zA-Z]+)(\d+)$", username)
    if match:
        year, branch, roll = match.groups()
        return f"20{year}{branch}{roll.zfill(4)}"
    return None


def get_roll_no(uid: str) -> str:
    """Return the roll-number portion of the Firebase user's e-mail."""
    user = auth.get_user(uid)
    return user.email.split("@")[0]
