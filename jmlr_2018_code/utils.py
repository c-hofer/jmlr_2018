import torch
import numpy
from chofer_torchex.utils.functional import collection_cascade
from chofer_torchex.utils.data.collate import dict_sample_target_iter_concat
from chofer_torchex.nn.slayer import SLayer


def numpy_to_torch_cascade(input):
    def numpy_to_torch(array):
        return_value = None
        try:
            return_value = torch.from_numpy(array)
        except Exception as ex:
            if len(array) == 0:
                return_value = torch.Tensor()
            else:
                raise ex

        return return_value.float()

    return collection_cascade(input,
                              stop_predicate=lambda x: isinstance(x, numpy.ndarray),
                              function_to_apply=numpy_to_torch)


def bar_code_slayer_collate_fn(sample_target_iter):
    x, y = dict_sample_target_iter_concat(sample_target_iter)
    x = numpy_to_torch_cascade(x)
    x = collection_cascade(x, stop_predicate=lambda x: isinstance(x, list),
                           function_to_apply=lambda x: SLayer.prepare_batch(x, 2))
    y = torch.LongTensor(y)
    return x, y
