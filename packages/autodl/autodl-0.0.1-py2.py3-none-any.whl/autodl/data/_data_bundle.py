# Author: LIU Zhengying
# Creation Date: 18 June 2018
"""
A class to facilitate the management of datasets for AutoDL. It can keep
track of the files of each component (training set, test set, metadata, etc)
of a dataset, and make manipulations on them such as format transformation,
train/test split, example-label separation, checking, etc.

[IMPORTANT] To use this class, one should be very careful about file names! So
try not to modify file names manually.
Of course, originally this class is only reserved for organizers or their
collaborators, since the participants will only see the result of this class.
"""

import glob
import numpy as np
import os
import sys
import tensorflow as tf
import pandas as pd
import yaml
import hashlib

from ..data._dataset import AutoDLDatasetSubset
from ..data.utils import check_integrity, download_and_extract_archive
from ..data.urls import DATA_URLS, SOLUTION_URLS

__all__ = ["DataBundle"]

REPO_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
)
DATASETS_DIR = os.path.join(REPO_DIR, "datasets")


class DataBundle:
    """A class for managing datasets formatted in AutoDL TFRecord format.
    Each dataset is a directory similar to
        .
        ├── adult.data
        │   ├── test
        │   │   ├── metadata.textproto
        │   │   └── sample-adult-test.tfrecord
        │   └── train
        │           ├── metadata.textproto
        │           └── sample-adult-train.tfrecord
        ├── adult.solution
        ├── adult_private.info (optional)
        └── adult_public.info (optional)

    In each TFRecord file (e.g. `sample-adult-train.tfrecord`), each of its
    examples is of the form
        (example, labels)
    where `example` is a dense 4-D Tensor of shape
        (sequence_size, row_count, col_count, num_channels)
    and `labels` is a 1-D Tensor of shape
        (output_dim,).
    Here `output_dim` represents number of classes of this
    multilabel classification task.

    IMPORTANT: some of the dimensions of `example` might be `None`,
    which means the shape on this dimension might be variable. In this
    case, some preprocessing technique should be applied in order to
    feed the training of a neural network. For example, if an image
    dataset has `example` of shape
        (1, None, None, 3)
    then the images in this datasets may have different sizes. On could
    apply resizing, cropping or padding in order to have a fixed size
    input tensor.
    """

    def __init__(self, dataset_name=None, dataset_dir=None, download=False):
        """
        Args:
            dataset_dir: str, the path to the dataset directory which should be like
                adult/
                ├── adult.data
                │   ├── test
                │   │   ├── metadata.textproto
                │   │   └── sample-adult-test.tfrecord
                │   └── train
                │           ├── metadata.textproto
                │           └── sample-adult-train.tfrecord
                ├── adult.solution (optional for blind test datasets)
                ├── adult_private.info (optional)
                └── adult_public.info (optional)
            dataset_name: str, name of the dataset used in AutoDL challenge.
                See more info at:
                    https://autodl.lri.fr/competitions/162#learn_the_details-get_data
        """
        # Check validity of `dataset_dir` and `dataset_name`
        # When `dataset_dir` is `None`, use `dataset_name`
        if dataset_dir is None:
            if dataset_name is None:
                raise ValueError(
                    "`dataset_dir` and `dataset_name` shouldn't " + "be both `None`."
                )
            else:
                if not dataset_name in DATA_URLS:
                    raise ValueError(
                        "Not a valid AutoDL dataset name: "
                        + "{}. ".format(dataset_name)
                        + "Should be one "
                        + "of {}".format(list(DATA_URLS))
                    )
                else:
                    self.data_url = DATA_URLS[dataset_name]
                    self.solution_url = SOLUTION_URLS[dataset_name]
                    self.dataset_name = dataset_name
                    self.dataset_dir = os.path.join(DATASETS_DIR, dataset_name)
                    if download or not os.path.isdir(self.dataset_dir):
                        if not download:  # No downloaded dataset found
                            print("No dataset found at {}".format(self.dataset_dir))
                            print("Start downloading...")
                        self.download()
        else:
            self.dataset_dir = dataset_dir

        # Create a new graph to avoid side effects in default graph
        with tf.Graph().as_default():
            self.dataset_dir = os.path.abspath(os.path.expanduser(self.dataset_dir))
            self.dataset_name = self.get_dataset_name()
            self.domain = self.get_domain()

    def get_dataset_name(self):
        """Get the name of the dataset.

        Returns:
            a 'string' object.
        """
        files = os.listdir(self.dataset_dir)
        data_files = [x for x in files if x.endswith(".data")]
        if len(data_files) == 0:
            raise ValueError(
                "No '.data' files or folders found ".format(data_files)
                + "at dataset_dir={}. Please ".format(self.dataset_dir)
                + "verify the dataset's integrity or re-download it "
                + "(e.g. by putting download=True)."
            )
        elif len(data_files) > 1:
            raise ValueError(
                "Multiple '.data' files or folders found ({}) ".format(data_files)
                + "at dataset_dir={}".format(self.dataset_dir)
            )
        dataset_name = data_files[0][:-5]
        return dataset_name

    def get_dataset_dir(self):
        return self.dataset_dir

    def download(self):
        data_filename = "{}.data.zip".format(self.dataset_name)
        solution_filename = "{}.solution.zip".format(self.dataset_name)
        download_and_extract_archive(
            self.data_url, self.dataset_dir, filename=data_filename
        )
        download_and_extract_archive(
            self.solution_url, self.dataset_dir, filename=solution_filename
        )

    def _get_path_to_subset(self, subset="train"):
        """Get the path to `subset` (can be 'train' or test).

        For example, givev a valid TFRecord Format dataset of directory 'adult/',
        then return 'adult/adult.data/train/' for the subset 'train'.
        """
        if not subset in ["train", "test"]:
            raise ValueError(
                "`subset` should be 'train' or 'test'. But got '{}'.".format(subset)
            )
        return os.path.join(self.dataset_dir, self.dataset_name + ".data", subset)

    def get_subset(self, subset="train"):
        return self.get_sub_data_bundle(subset=subset).get_dataset()

    def get_sub_data_bundle(self, subset="train"):
        return self._get_autodl_dataset(subset=subset)

    def get_tfrecord_dataset(self, subset="train"):
        """
        Returns:
            A raw tf.data.TFRecordDataset corresponding to `subset`.
        """
        subset_path = self._get_path_to_subset(subset)
        glob_pattern = os.path.join(subset_path, "sample*")
        files = tf.io.gfile.glob(glob_pattern)
        if not files:
            raise IOError(
                "Unable to find training files. data_pattern='"
                + dataset_file_pattern(self.dataset_name_)
                + "'."
            )
        return tf.data.TFRecordDataset(files)

    def get_nth_element(self, num, subset="train"):
        """Get n-th element in `autodl_dataset` using iterator."""
        # -- IG: replaced previous 3d version
        dataset = self.get_subset(subset=subset)
        iterator = tf.compat.v1.data.make_one_shot_iterator(dataset)
        next_element = iterator.get_next()
        with tf.compat.v1.Session() as sess:
            for _ in range(num + 1):
                tensor_4d, labels = sess.run(next_element)
        return tensor_4d, labels

    def _get_autodl_dataset(self, subset="train"):
        subset_path = self._get_path_to_subset(subset)
        return AutoDLDatasetSubset(subset_path)

    def get_output_size(self):
        d_train = self._get_autodl_dataset(subset="train")
        metadata = d_train.get_metadata()
        output_dim = metadata.get_output_size()
        return output_dim

    def get_num_examples(self, subset="train"):
        d = self._get_autodl_dataset(subset=subset)
        return d.get_metadata().size()

    def get_example_shape(self):
        d_train = self._get_autodl_dataset(subset="train").get_dataset()
        example, labels = tf.compat.v1.data.make_one_shot_iterator(d_train).get_next()
        return example.shape

    def get_domain(self):
        """Infer the domain.

        Returns:
            a string in ['tabular', 'image', 'speech', 'text', 'video'].
        """
        d_train = self._get_autodl_dataset(subset="train")
        metadata = d_train.get_metadata()
        row_count, col_count = metadata.get_matrix_size(0)
        sequence_size = metadata.get_sequence_size()
        domain = None
        if sequence_size == 1:
            if row_count == 1 or col_count == 1:
                domain = "tabular"
            else:
                domain = "image"
        else:
            if row_count == 1 and col_count == 1:
                domain = "speech"
            elif row_count == 1 or col_count == 1:
                domain = "text"
            else:
                domain = "video"
        return domain

    def show_info(self):
        print("== Dataset info ==")
        print("Name: {}".format(self.dataset_name))
        print("Domain: {}".format(self.domain))
        print(
            "Numer of training examples: {}".format(self.get_num_examples(subset="train"))
        )
        print(
            "Number of testing examples: {}".format(self.get_num_examples(subset="test"))
        )
        print("Example shape: {}".format(self.get_example_shape()))
        print("Num classes: {}".format(self.get_output_size()))

    def get_classes_list(self):
        """Get list of text label names.

        Returns:
            a list of strings. `None` if not exists.
        """
        d_train = self._get_autodl_dataset(subset="train")
        metadata = d_train.get_metadata()
        output_dim = metadata.get_output_size()
        label_to_index_map = metadata.get_label_to_index_map()
        if not label_to_index_map:
            return None
        classes_list = [None] * output_dim
        for label, index in label_to_index_map.items():
            classes_list[index] = label
        return classes_list

    def _parse_function(self, sequence_example_proto):
        """Parse a SequenceExample in the AutoDL/TensorFlow format.

        Args:
            sequence_example_proto: a SequenceExample with "x_dense_input" or sparse
                input or compressed input representation
        Returns:
            A tuple of (contexts, features) where `contexts` is a dictionary of 3
                Tensor objects of keys 'id', 'label_index', 'label_score' and
                features a dictionary containing key '0_dense_input' for DENSE,
                '0_compressed' for COMPRESSED or '0_sparse_col_index',
                '0_sparse_row_index' and '0_sparse_value' for SPARSE.
        """
        autodl_dataset = self._get_autodl_dataset(subset="train")
        sequence_features = {}
        for i in range(autodl_dataset.metadata_.get_bundle_size()):
            if autodl_dataset.metadata_.is_sparse(i):
                sequence_features[
                    autodl_dataset._feature_key(i, "sparse_col_index")
                ] = tf.io.VarLenFeature(tf.int64)
                sequence_features[
                    autodl_dataset._feature_key(i, "sparse_row_index")
                ] = tf.io.VarLenFeature(tf.int64)
                sequence_features[
                    autodl_dataset._feature_key(i, "sparse_value")
                ] = tf.io.VarLenFeature(tf.float32)
            elif autodl_dataset.metadata_.is_compressed(i):
                sequence_features[
                    autodl_dataset._feature_key(i, "compressed")
                ] = tf.io.VarLenFeature(tf.string)
            else:
                sequence_features[
                    autodl_dataset._feature_key(i, "dense_input")
                ] = tf.io.FixedLenSequenceFeature(
                    autodl_dataset.metadata_.get_tensor_size(i), dtype=tf.float32
                )
        contexts, features = tf.io.parse_single_sequence_example(
            sequence_example_proto,
            context_features={
                # "id": tf.VarLenFeature(tf.int64),
                "id": tf.io.FixedLenFeature([], tf.int64),
                "label_index": tf.io.VarLenFeature(tf.int64),
                "label_score": tf.io.VarLenFeature(tf.float32),
            },
            sequence_features=sequence_features,
        )

        return contexts, features

    def get_contexts_features(self, subset="train"):
        """Read raw TFRecords in training set or test set by parsing
        SequenceExample proto.

        Returns:
            A tuple of (contexts, features) where `contexts` is a dictionary of 3
                Tensor objects of keys 'id', 'label_index', 'label_score' and
                features a dictionary containing key '0_dense_input' for DENSE format,
                '0_compressed' for COMPRESSED format or '0_sparse_col_index',
                '0_sparse_row_index' and '0_sparse_value' for SPARSE format.
        """
        c_name = "contexts_" + subset
        f_name = "features_" + subset
        if hasattr(self, c_name) and hasattr(self, f_name):
            return getattr(self, c_name), getattr(self, f_name)
        else:
            tfrecord_dataset = self.get_tfrecord_dataset(subset=subset)
            tfrecord_dataset = tfrecord_dataset.map(self._parse_function)
            iterator = tf.compat.v1.data.make_one_shot_iterator(tfrecord_dataset)
            contexts, features = iterator.get_next()
            setattr(self, c_name, contexts)
            setattr(self, f_name, features)
            return contexts, features

    def _get_bytes(self, subset="train"):
        """Get raw bytes of the images. Only for COMPRESSED format.

        Returns:
            a 0-D tensor of bytes.
        """
        assert self._get_autodl_dataset().get_metadata().is_compressed(0)
        contexts, features = self.get_contexts_features(subset=subset)
        bytes_tensor = features["0_compressed"].values
        return bytes_tensor[0]

    def _get_image_format(self):
        """Infer image format from bytes.

        Returns:
            a string in ['jpg', 'png', 'bmp', 'gif', 'Unknown'].
        """
        image_bytes = self._get_bytes()
        is_jpeg = tf.image.is_jpeg(image_bytes)

        def is_png(contents):
            return contents[:3] == b"\211PN"

        def is_bmp(contents):
            return contents[:2] == "BM"

        def is_gif(contents):
            return contents[:3] == b"\x47\x49\x46"

        with tf.compat.v1.Session() as sess:
            bytes_value = sess.run(image_bytes)
            if sess.run(is_jpeg):
                return "jpg"
            elif is_png(bytes_value):
                return "png"
            elif is_bmp(bytes_value):
                return "bmp"
            elif is_gif(bytes_value):
                return "gif"
            else:
                return "Unknown"

    def get_index(self, subset="train"):
        """Get a 0-D tensor of the id of examples."""
        contexts, features = self.get_contexts_features(subset=subset)
        return contexts["id"]

    # def get_label_confidence_pairs(self, subset='train'):
    #     """Get list of label-confidence pairs lists if exists.
    #
    #     Returns:
    #         a list of lists of label-confidence pairs or `None`.
    #     """
    #     if subset == 'train':
    #         label_confidence_pairs = []
    #         contexts, features = self.get_contexts_features(subset='train')
    #         label_index = contexts['label_index'].values
    #         label_score = contexts['label_score'].values
    #         while True:
    #             with tf.Session() as sess:
    #                 try:
    #                     index_value, score_value = sess.run((label_index, label_score))
    #                     label_confidence_pairs.append(zip(index_value, score_value))
    #                 except tf.errors.OutOfRangeError:
    #                     break
    #         return label_confidence_pairs
    #     else:
    #         if not subset == 'test':
    #             raise ValueError("`subset` should be in ['train', 'test'] " +
    #                                                "but got {}.".format(subset))
    #         path_to_solution = os.path.join(self.dataset_dir,
    #                                                                         self.dataset_name + '.solution')
    #         if not os.path.exists(path_to_solution):
    #             return None
    #         else:
    #             solution_array = np.loadtxt(path_to_solution)
    #             label_confidence_pairs = to_label_confidence_pairs(solution_array)
    #             return label_confidence_pairs

    def get_train_labels(self):
        contexts, features = self.get_contexts_features(subset="train")
        label_index = contexts["label_index"].values
        label_score = contexts["label_score"].values
        return label_index, label_score

    def get_test_labels(self, return_array=False):
        """Get test solution as NumPy array if exists.

        Returns:
            a list of lists of label-confidence pairs or `None`.
        """
        path_to_solution = os.path.join(self.dataset_dir, self.dataset_name + ".solution")
        if not os.path.exists(path_to_solution):
            return None
        else:
            solution_array = np.loadtxt(path_to_solution)
            if return_array:
                return solution_array
            else:
                label_confidence_pairs = to_label_confidence_pairs(solution_array)
                return label_confidence_pairs

    def get_labels_df(self, write_files=False):
        """Construct a `labels.csv` file just as in File Format."""
        if self.domain != "image":
            raise NotImplementedError(
                "This functionality is not implemented for "
                + "the domain {} yet.".format(browser.domain)
            )

        dataset_name = self.dataset_name
        if write_files and not os.path.exists(dataset_name):
            os.mkdir(dataset_name)

        output_dim = self.get_output_size()

        classes_list = self.get_classes_list()
        if not classes_list:
            classes_list = range(output_dim)

        file_names = []
        label_confidence_pairs = []
        subsets = []
        indices = []
        hash_values = []

        total_num_examples = self.get_num_examples(
            subset="train"
        ) + self.get_num_examples(subset="test")
        le_n = len(str(total_num_examples))

        image_format = self._get_image_format()

        for subset in ["test", "train"]:
            image_bytes_tensor = self._get_bytes(subset)
            index_tensor = self.get_index(subset)

            if subset == "test":
                count = 0
                label_confidence_pairs_test = self.get_test_labels()
                with tf.compat.v1.Session() as sess:
                    while True:
                        try:
                            image_bytes, index = sess.run(
                                (image_bytes_tensor, index_tensor)
                            )
                            index_score_list = label_confidence_pairs_test[count]

                            string_list = [
                                str(l) + " " + str(c) for l, c in index_score_list
                            ]
                            labels_list = [
                                str(classes_list[l]) for l, c in index_score_list
                            ]
                            labels_str = "-".join(labels_list)
                            if len(labels_str) > 20:
                                labels_str = labels_str[:20]
                            label_confidence_pairs_str = " ".join(string_list)
                            file_name = (
                                str(index).zfill(le_n)
                                + "_"
                                + labels_str
                                + "_"
                                + subset
                                + "."
                                + image_format
                            )
                            label_confidence_pairs.append(label_confidence_pairs_str)
                            file_names.append(file_name)
                            subsets.append(subset)
                            indices.append(index)
                            hash_values.append(get_hash_value(image_bytes))
                            count += 1
                            if write_files:
                                file_path = os.path.join(dataset_name, file_name)
                                with open(file_path, "wb") as f:
                                    f.write(image_bytes)
                        except tf.errors.OutOfRangeError:
                            break
            else:  # subset == 'train'
                count = 0
                label_index, label_score = self.get_train_labels()
                with tf.compat.v1.Session() as sess:
                    while True:
                        try:
                            image_bytes, index, label_index_v, label_score_v = sess.run(
                                (
                                    image_bytes_tensor,
                                    index_tensor,
                                    label_index,
                                    label_score,
                                )
                            )
                            index_score_list = list(zip(label_index_v, label_score_v))

                            string_list = [
                                str(l) + " " + str(c) for l, c in index_score_list
                            ]
                            labels_list = [
                                str(classes_list[l]) for l, c in index_score_list
                            ]
                            labels_str = "-".join(labels_list)
                            if len(labels_str) > 20:
                                labels_str = labels_str[:20]
                            label_confidence_pairs_str = " ".join(string_list)
                            file_name = (
                                str(index).zfill(le_n)
                                + "_"
                                + labels_str
                                + "_"
                                + subset
                                + "."
                                + image_format
                            )
                            label_confidence_pairs.append(label_confidence_pairs_str)
                            file_names.append(file_name)
                            subsets.append(subset)
                            indices.append(index)
                            hash_values.append(get_hash_value(image_bytes))
                            count += 1
                            if write_files:
                                file_path = os.path.join(dataset_name, file_name)
                                with open(file_path, "wb") as f:
                                    f.write(image_bytes)
                        except tf.errors.OutOfRangeError:
                            break

        labels_file_name = "labels.csv"
        labels_df = pd.DataFrame(
            {
                "FileName": file_names,
                "LabelConfidencePairs": label_confidence_pairs,
                "Subset": subsets,
                "Index": indices,
                "HashValue": hash_values,
            }
        )

        return labels_df

    def tfrecord_format_to_file_format(self, new_dataset_name=None):
        """Generate a dataset in File Format.

        Args:
            tfdataset_dir: path to dataset in TFRecord Format.
            new_dataset_name: name of the created dataset, is also the folder name

        Returns:
            Create a folder `new_dataset_name` in the parent directory of
                `dataset_dir`.

        For more information on File Format, see:
            https://github.com/zhengying-liu/autodl-contrib/tree/master/file_format
        """
        if self.domain != "image":
            raise NotImplementedError(
                "This functionality is not implemented for "
                + "the domain {} yet.".format(browser.domain)
            )

        dataset_name = self.dataset_name
        if new_dataset_name is None:
            new_dataset_name = dataset_name + "_file_format"

        new_dataset_dir = os.path.abspath(
            os.path.join(self.dataset_dir, os.pardir, new_dataset_name)
        )
        os.makedirs(new_dataset_dir, exist_ok=True)

        output_dim = self.get_output_size()

        classes_list = self.get_classes_list()
        if classes_list:
            label_name_file = os.path.join(new_dataset_dir, "label.name")
            with open(label_name_file, "w") as f:
                f.write("\n".join(classes_list) + "\n")
        else:
            classes_list = range(output_dim)

        file_names = []
        label_confidence_pairs = []
        subsets = []
        indices = []
        hash_values = []

        total_num_examples = self.get_num_examples(
            subset="train"
        ) + self.get_num_examples(subset="test")
        le_n = len(str(total_num_examples))

        image_format = self._get_image_format()

        for subset in ["test", "train"]:
            image_bytes_tensor = self._get_bytes(subset)
            index_tensor = self.get_index(subset)

            if subset == "test":
                count = 0
                label_confidence_pairs_test = self.get_test_labels()
                print("Number of test examples:", len(label_confidence_pairs_test))
                with tf.compat.v1.Session() as sess:
                    while True:
                        try:
                            # image_bytes = sess.run(image_bytes_tensor)
                            # index = sess.run(index_tensor)
                            # print("index:", index)
                            image_bytes, index = sess.run(
                                (image_bytes_tensor, index_tensor)
                            )
                            if count % 100 == 0:
                                print(
                                    "Writing {}-th example for subset {}... Index: {}".format(
                                        count, subset, index
                                    )
                                )
                            index_score_list = label_confidence_pairs_test[count]

                            string_list = [
                                str(l) + " " + str(c) for l, c in index_score_list
                            ]
                            labels_list = [
                                str(classes_list[l]) for l, c in index_score_list
                            ]
                            labels_str = "-".join(labels_list)
                            if len(labels_str) > 20:
                                labels_str = labels_str[:20]
                            label_confidence_pairs_str = " ".join(string_list)
                            file_name = (
                                str(index).zfill(le_n)
                                + "_"
                                + labels_str
                                + "_"
                                + subset
                                + "."
                                + image_format
                            )
                            file_path = os.path.join(new_dataset_dir, file_name)
                            with open(file_path, "wb") as f:
                                f.write(image_bytes)
                            label_confidence_pairs.append(label_confidence_pairs_str)
                            file_names.append(file_name)
                            subsets.append(subset)
                            indices.append(index)
                            hash_values.append(get_hash_value(image_bytes))
                            count += 1
                        except tf.errors.OutOfRangeError:
                            print(
                                "Number of last example in subset {}: {}".format(
                                    subset, count
                                )
                            )
                            break
            else:  # subset == 'train'
                count = 0
                label_index, label_score = self.get_train_labels()
                with tf.compat.v1.Session() as sess:
                    while True:
                        try:
                            image_bytes, index, label_index_v, label_score_v = sess.run(
                                (
                                    image_bytes_tensor,
                                    index_tensor,
                                    label_index,
                                    label_score,
                                )
                            )
                            index_score_list = list(zip(label_index_v, label_score_v))
                            if count % 100 == 0:
                                print(
                                    "Writing {}-th example for subset {}... Index: {}".format(
                                        count, subset, index
                                    )
                                )
                                # print("index_score_list:", index_score_list)

                            string_list = [
                                str(l) + " " + str(c) for l, c in index_score_list
                            ]
                            labels_list = [
                                str(classes_list[l]) for l, c in index_score_list
                            ]
                            labels_str = "-".join(labels_list)
                            if len(labels_str) > 20:
                                labels_str = labels_str[:20]
                            label_confidence_pairs_str = " ".join(string_list)
                            file_name = (
                                str(index).zfill(le_n)
                                + "_"
                                + labels_str
                                + "_"
                                + subset
                                + "."
                                + image_format
                            )
                            file_path = os.path.join(new_dataset_dir, file_name)
                            with open(file_path, "wb") as f:
                                f.write(image_bytes)
                            label_confidence_pairs.append(label_confidence_pairs_str)
                            file_names.append(file_name)
                            subsets.append(subset)
                            indices.append(index)
                            hash_values.append(get_hash_value(image_bytes))
                            count += 1
                        except tf.errors.OutOfRangeError:
                            print(
                                "Number of last example in subset {}: {}".format(
                                    subset, count
                                )
                            )
                            break

        labels_file_name = "labels.csv"
        labels_df = pd.DataFrame(
            {
                "FileName": file_names,
                "LabelConfidencePairs": label_confidence_pairs,
                "Subset": subsets,
                "Index": indices,
                "HashValue": hash_values,
            }
        )
        labels_file_path = os.path.join(new_dataset_dir, labels_file_name)
        labels_df.to_csv(labels_file_path, index=False)

        private_info_file_name = "private.info"
        private_info_file_path = os.path.join(new_dataset_dir, private_info_file_name)
        with open(private_info_file_path, "w") as f:
            f.write("")

        return None
