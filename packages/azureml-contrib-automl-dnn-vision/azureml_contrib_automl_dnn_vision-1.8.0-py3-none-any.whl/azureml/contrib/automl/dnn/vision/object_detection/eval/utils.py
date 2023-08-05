# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Utils for running evaluation metrics."""

import logging

logger = logging.getLogger(__name__)


def prepare_dataset_for_eval(dataset):
    """Convert a dataset object to a dictionary that can be consumed by cocotools/vocmap during evaluation.

    :param dataset: Dataset with ground truth data used for evaluation
    :type dataset: CommonObjectDetectionDatasetWrapper object (see object_detection.data.datasets)
    :return: Dataset in format that can be converted into a cocotools index.
    :rtype: Dict of dicts
    """
    images = []
    ann_id = 0
    annotations = []
    categories = []

    for _, box_info, image_info in dataset:

        if not box_info or not image_info:
            logger.warning("Since box_info or images_info is not found, image will be ignored")
            continue

        image_id = image_info["filename"]

        img_dict = {}

        img_dict["id"] = image_id
        img_dict["height"] = image_info["height"]
        img_dict["width"] = image_info["width"]

        images.append(img_dict)

        boxes = box_info["boxes"]
        labels = box_info["labels"]
        areas = image_info["areas"]
        is_crowds = image_info["iscrowd"]

        for box, label, area, is_crowd in zip(boxes, labels, areas, is_crowds):

            ann = {}

            box_width = box[2] - box[0]
            box_height = box[3] - box[1]

            ann["bbox"] = [box[0], box[1], box_width, box_height]
            classification = dataset.index_to_label(label)

            ann["category_id"] = classification
            ann["image_id"] = image_id
            ann["id"] = ann_id
            ann["area"] = area
            ann["iscrowd"] = is_crowd
            ann_id += 1

            annotations.append(ann)

        categories = [{"id": cat} for cat in dataset.classes]

    return {"images": images, "annotations": annotations, "categories": categories}


def prepare_bounding_boxes_for_eval(bounding_box_list):
    """Converts a list of  bounding box records to a format that can be consumed by cocotools/vocmap.

    :param bounding_box_list: Bounding box records for a set of images
    :type bounding_box_list: List of ImageBoxes (see object_detection.common.bounding_box)
    :return: Detections in format that can be consumed by cocotools/vocmap
    :rtype: List of dicts
    """
    detections = []

    for bounding_box_record in bounding_box_list:
        image_id = bounding_box_record.image_name

        for box_record in bounding_box_record._boxes:
            box = box_record.bounding_box
            category = box_record.label
            score = box_record.score

            record = {"image_id": image_id,
                      "bbox": box,
                      "category_id": category,
                      "score": score}

            detections.append(record)

    return detections
