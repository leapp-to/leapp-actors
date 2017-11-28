import os
import unittest

from snactor import loader


class TestSchemaAvailability(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSchemaAvailability, self).__init__(*args, **kwargs)

        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.root_path = os.path.join(current_path, "src")
        self.actors_path = os.path.join(self.root_path, "actors")
        self.schema_path = os.path.join(self.root_path, "schemas")

    def test_actors_and_schemas(self):
        failed = False

        try:
            loader.load(self.actors_path)
            loader.load_schemas(self.schema_path)
            loader.validate_actor_types()
        except loader.ActorTypeValidationError as e:
            for (type_name, direction, actor_name) in e.data:
                print("Schema for type '{}' defined in actor '{}' section '{}' was not found"
                      .format(type_name, actor_name, direction))
            failed = True
        except Exception as e:
            import traceback
            traceback.print_exc()
            failed = True

        self.assertEqual(False, failed)


if __name__ == '__main__':
    unittest.main()
