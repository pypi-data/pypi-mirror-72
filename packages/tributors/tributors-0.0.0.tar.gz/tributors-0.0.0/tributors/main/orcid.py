"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os


def get_orcid(email):
    """Given a GitHub repository address, retrieve a lookup of contributors
       from the API endpoint. We look to use the GITHUB_TOKEN if exported
       to the environment, and exit if the response has any issue
    """
    orcid_token = os.environ.get("ORCID_TOKEN")
    if not email or not orcid_token:
        return
    # TODO: not sure how this is expected to work given OAuth2...
