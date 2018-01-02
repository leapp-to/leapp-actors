#!/usr/bin/python

"""
Actor for extracting PostgreSQL related data from augeas output. This is useful for offline
detection of PostgreSQL installation. 

Output structure:

"postgresql_scanner": {
    "instances": [
        {
            "postgresql_conf": {
                "path": String,
                "properties": [
                    {
                        "name": string,
                        "value": string
                    },
                    ...
                ]
            },
            "pg_hba_conf": {
                "path": String,
                "properties": [
                    {
                        "name": string,
                        "properties": [
                            {
                                "name": string,
                                "value": string
                            }
                        ],
                        ...
                    },
                    ...
                ]
            }
        },
        ...
    ]
}

Improvements:
  Currently the actor can detect only postgresql installed in default location reported by augeas.
It would be nice, if it cold detect also non-standard installations used by i.e. Satellite 5 and
probably few other RH products.
"""

import sys
import json


if __name__ == "__main__":
    augeas_input = json.load(sys.stdin)

    instances = [] 

    # aug_postgresql might be undefined, that usually means the postgresql data
    # were not initialized.
    try:
        augeas_postgresql = augeas_input["aug_postgresql"][0]
        augeas_hba = augeas_input["aug_pg_hba"][0]
        instance = {}

        instance["postgresql_conf"] = {
            "path": augeas_postgresql["absolute_path"],
            "properties": augeas_postgresql["properties"]
        }

        instance["pg_hba_conf"] = {
            "path": augeas_hba["absolute_path"],
            "properties": augeas_hba["properties"]
        }

        instances.append(instance)

    except KeyError as e:
        pass

    if len(instances):
        print(json.dumps({"postgresql_scanner": [{"instances": instances}]}))
