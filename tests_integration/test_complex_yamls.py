import unittest
import os
import kappaconfig as kc
import yaml

class TestComplexYamls(unittest.TestCase):
    def test_testcase_exists_for_every_yaml_file(self):
        # there probably are libraries that allow this implicitly (e.g. ddt should be able to do this)
        # but this makes running/debugging individual tests a hassle, so just check it manually
        files = os.listdir("tests_integration/complex_yamls")
        with open(__file__) as f:
            yaml_files_test_content = f.read()
        # basic check if filename is contained
        for file in files:
            if ".result.yaml" in file: continue
            self.assertTrue(file in yaml_files_test_content, f"no testcase for {file}")

    def resolve_yaml(self, src_file_name):
        kc_obj = kc.from_file_uri(f"tests_integration/complex_yamls/{src_file_name}")
        resolver = kc.DefaultResolver(template_path="tests_integration/templates")
        expected_file_name = src_file_name.replace(".yaml", "") + ".result.yaml"
        with open(f"tests_integration/complex_yamls/{expected_file_name}") as f:
            expected = yaml.safe_load(f)
        self.assertEqual(expected, resolver.resolve(kc_obj))

    def test_test(self):
        self.resolve_yaml("test.yaml")