import os
import unittest

import yaml

import kappaconfig as kc


class TestComplexYamls(unittest.TestCase):
    @staticmethod
    def get_file_uris(root_path):
        file_or_dir_list = os.listdir(root_path)
        file_uris = []
        for file_or_dir in file_or_dir_list:
            file_or_dir_uri = f"{root_path}/{file_or_dir}"
            if file_or_dir_uri.endswith(".result.yaml"): continue

            if os.path.isdir(file_or_dir_uri):
                file_uris += TestComplexYamls.get_file_uris(file_or_dir_uri)
            else:
                file_uris += [file_or_dir_uri]
        return file_uris

    def test_testcase_exists_for_every_yaml_file(self):
        # there probably are libraries that allow this implicitly (e.g. ddt should be able to do this)
        # but this makes running/debugging individual tests a hassle, so just check it manually
        root_path = "tests_integration/complex_yamls"
        file_uris = self.get_file_uris(root_path)
        file_uris = list(map(lambda fu: fu[len(root_path) + 1:], file_uris))
        with open(__file__) as f:
            yaml_files_test_content = f.read()
        # basic check if filename is contained
        for file_uri in file_uris:
            self.assertTrue(file_uri in yaml_files_test_content, f"no testcase for {file_uri}")

    def resolve_yaml(self, src_file_name):
        kc_obj = kc.from_file_uri(f"tests_integration/complex_yamls/{src_file_name}")
        resolver = kc.DefaultResolver(template_path="tests_integration/templates")
        expected_file_name = src_file_name.replace(".yaml", "") + ".result.yaml"
        with open(f"tests_integration/complex_yamls/{expected_file_name}") as f:
            expected = yaml.safe_load(f)
        self.assertEqual(expected, resolver.resolve(kc_obj))

    def test_data_cifar(self):
        self.resolve_yaml("data/cifar.yaml")

    def test_data_mvtec(self):
        self.resolve_yaml("data/mvtec.yaml")

    def test_data_toy(self):
        self.resolve_yaml("data/toy.yaml")

    def test_loggers_default_epochs(self):
        self.resolve_yaml("loggers/default_epochs.yaml")

    def test_loggers_default_updates(self):
        self.resolve_yaml("loggers/default_updates.yaml")

    def test_loggers_discriminator_epochs(self):
        self.resolve_yaml("loggers/discriminator_epochs.yaml")

    def test_models_mae(self):
        self.resolve_yaml("models/mae.yaml")

    def test_models_mae_with_schedule(self):
        self.resolve_yaml("models/mae_with_schedule.yaml")

    def test_models_vit(self):
        self.resolve_yaml("models/vit.yaml")

    def test_optim_mae_pretrain(self):
        self.resolve_yaml("optims/mae_pretrain.yaml")

    def test_optim_scaled_lr(self):
        self.resolve_yaml("optims/scaled_lr.yaml")

    def test_schedule_warmup_cosine(self):
        self.resolve_yaml("schedules/warmup_cosine.yaml")

    def test_parameters_doesnt_require_template(self):
        self.resolve_yaml("parameters/doesnt_require_template.yaml")

    def test_parameters_floats_arent_converted_to_string(self):
        self.resolve_yaml("parameters/floats_arent_converted_to_string.yaml")
