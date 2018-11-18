from leapp.actors import Actor
from leapp.models import AugeasOutput, AugeasLensesList, AugeasLensItem
from leapp.tags import FactsPhaseTag

import augeas
import json

import augeaslib


class AugeasScanner(Actor):
    name = 'augeas_scanner'
    description = 'Actor scans config files using Augeas'
    consumes = ()
    produces = (AugeasOutput,)
    tags = (FactsPhaseTag.Common,)

    def process(self):
        self.log.info("Starting augeas scanner")

        self.log.info("Facts: {}".format(FactsPhaseTag.__dict__))

        # path to folder with custom lenses
        custom_lenses_folder = 'files/lenses'
        use_custom_lenses = True

        augeas_tree = augeas.Augeas()

        augeas_config = {
            'required_lenses': ['Httpd'],  # empty list for all lenses supported by augeas
            'use_custom_lenses': use_custom_lenses,
            'custom_lenses_folder': custom_lenses_folder,
            'lens_transforms': [
                # {
                #     'lens_name': 'httpd',
                #     'directives': ['ScriptAlias'],
                #     'load_files': ['/path/to/some/httpd.conf'],
                #     'prefix_for_relative': '/etc/httpd'
                # }
            ]
        }

        metadata = augeaslib.process_augeas_data(augeas_config, augeas_tree)

        output = AugeasOutput()
        for lens_name in metadata:
            lens_data = metadata[lens_name]

            lens_list = []

            for lens_item in lens_data:
                lens_list.append(
                    AugeasLensItem(
                        name=lens_item['name'],
                        properties=json.dumps(lens_item.get('properties')),
                        absolute_path=lens_item['absolute_path']
                    )
                )

            output.items.append(
                AugeasLensesList(
                    lens_name=lens_name,
                    lens_items=lens_list
                )
            )

        self.produce(output)

        self.log.info("Augeas scanner finished")
