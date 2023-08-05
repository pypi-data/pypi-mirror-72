import json
import os
import pytest
import tempfile

from pathlib import Path
from PIL import Image

from azureml.contrib.automl.dnn.vision.object_detection.common.boundingbox import BoundingBox
from azureml.contrib.automl.dnn.vision.object_detection.writers.score import _score_with_model
from .utils import CocoBaseModelWrapper
from .run_mock import RunMock, ExperimentMock, WorkspaceMock, DatastoreMock, LabeledDatasetFactoryMock


@pytest.mark.usefixtures('new_clean_dir')
class TestModelWrappers:
    def test_inference_base_model_wrapper(self, data_root):
        model_wrapper = CocoBaseModelWrapper()
        # TODO: Both of the following lines should be removed once this moves to initialization
        model_wrapper.classes = ['A'] * 91
        model_wrapper.to_device('cpu')
        im = Image.open(os.path.join(data_root, 'coco_classes_image.jpg'))
        bounding_boxes = model_wrapper.predict([im, im])
        assert len(bounding_boxes) == 2

        for box in bounding_boxes[0]:
            assert isinstance(box, BoundingBox)
            assert box.label == 'A'

    def test_score(self, data_root, image_list_file_name):
        image_dir = os.path.join(data_root, 'images')
        image_od_list_file_path = os.path.join(data_root, image_list_file_name)
        with open(image_od_list_file_path) as fp:
            expected_score_file_length = len(fp.readlines())
        # batch_size 1
        self._scoring_test(image_dir, image_od_list_file_path, 1, expected_score_file_length)
        # batch_size 2
        self._scoring_test(image_dir, image_od_list_file_path, 2, expected_score_file_length)

    def test_score_invalid_image_file(self, data_root, image_list_file_name):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            image_dir = os.path.join(data_root, 'images')
            temp_image_od_list_file_path = os.path.join(tmp_output_dir, image_list_file_name)
            # copy list from src_image_od_list_file.txt and add one extra file.
            image_od_list_file_path = os.path.join(data_root, image_list_file_name)
            with open(image_od_list_file_path) as input_fp:
                lines = input_fp.readlines()
                with open(temp_image_od_list_file_path, 'w') as fp:
                    fp.writelines(lines)
                    fp.write("\n")
                    fp.write("invalid_image_file.jpg" + "\n")

            with open(temp_image_od_list_file_path) as fp:
                expected_score_file_length = len(fp.readlines()) - 1  # One invalid image file in the images folder.

            self._scoring_test(image_dir, temp_image_od_list_file_path, 1, expected_score_file_length)
            self._scoring_test(image_dir, temp_image_od_list_file_path, 3, expected_score_file_length)

    @staticmethod
    def _scoring_test(image_dir, image_od_list_file_path, batch_size, expected_score_file_length):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_wrapper = CocoBaseModelWrapper()
            # TODO: Both of the following lines should be removed once this moves to initialization
            model_wrapper.classes = ['A'] * 91
            model_wrapper.to_device('cpu')

            # run predictions
            predictions_file = 'predictions_od.txt'
            predictions_output_file = os.path.join(tmp_output_dir, predictions_file)

            datastore_name = "TestDatastoreName"
            datastore_mock = DatastoreMock(datastore_name)
            workspace_mock = WorkspaceMock(datastore_mock)
            experiment_mock = ExperimentMock(workspace_mock)
            run_mock = RunMock(experiment_mock)
            test_dataset_id = 'b2458938-7966-4ca0-b4ba-a97d89d4eb2b'
            labeled_dataset_factory_mock = LabeledDatasetFactoryMock(test_dataset_id)
            test_target_path = "TestTargetPath"

            Path(predictions_output_file).touch()

            _score_with_model(model_wrapper, run_mock, test_target_path,
                              root_dir=image_dir, output_file=predictions_output_file,
                              image_list_file=image_od_list_file_path, batch_size=batch_size,
                              labeled_dataset_factory=labeled_dataset_factory_mock,
                              always_create_dataset=True,
                              num_workers=0)

            with open(predictions_output_file) as fp:
                for line in fp:
                    obj = json.loads(line.strip())
                    assert 'filename' in obj
                    assert 'boxes' in obj
                    assert len(obj['boxes']) > 0
                    assert 'box' in obj['boxes'][0]
                    assert 'label' in obj['boxes'][0]
                    assert 'score' in obj['boxes'][0]
            with open(predictions_output_file) as fp:
                lines = fp.readlines()
            assert len(lines) == expected_score_file_length

            assert labeled_dataset_factory_mock.task == 'ObjectDetection'
            expected_path = test_target_path + "/labeled_dataset.json"
            assert labeled_dataset_factory_mock.path == expected_path

            assert len(datastore_mock.files) == 1

            (files, root_dir, target_path, overwrite) = datastore_mock.files[0]
            assert len(files) == 1
            assert root_dir is None
            assert target_path == test_target_path
            assert overwrite

            assert len(datastore_mock.dataset_file_content) == expected_score_file_length

            for line in datastore_mock.dataset_file_content:
                line_contents = json.loads(line)
                assert line_contents['image_url'].startswith('AmlDatastore://')
                assert 'label' in line_contents
                assert 'label_confidence' in line_contents

            assert run_mock.properties['labeled_dataset_id'] == test_dataset_id
