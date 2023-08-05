# Copyright 1999-2020 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
import logging
import operator
import pickle
import random
from collections import defaultdict
from functools import reduce

import numpy as np

from .... import opcodes
from ....context import get_context, RunningMode
from ....core import ExecutableTuple
from ....serialize import DictField, Int32Field, KeyField, ListField, StringField, ValueType
from ...operands import LearnMergeDictOperand, OutputType
from ...utils import concat_chunks
from .align import align_data_set
from .core import LGBMModelType, get_model_cls_from_type

logger = logging.getLogger(__name__)


class LGBMTrain(LearnMergeDictOperand):
    _op_type_ = opcodes.LGBM_TRAIN

    _model_type = Int32Field('model_type', on_serialize=lambda x: x.value,
                             on_deserialize=LGBMModelType)
    _params = DictField('params', key_type=ValueType.string)
    _data = KeyField('data')
    _label = KeyField('label')
    _sample_weight = KeyField('sample_weight')
    _init_score = KeyField('init_score')
    _kwds = DictField('kwds', key_type=ValueType.string)

    _eval_datas = ListField('eval_datas', ValueType.key)
    _eval_labels = ListField('eval_labels', ValueType.key)
    _eval_sample_weights = ListField('eval_sample_weights', ValueType.key)
    _eval_init_scores = ListField('eval_init_scores', ValueType.key)

    _lgbm_endpoints = ListField('lgbm_endpoints', ValueType.string)
    _lgbm_port = Int32Field('lgbm_port')
    _tree_learner = StringField('tree_learner')
    _timeout = Int32Field('timeout')

    def __init__(self, model_type=None, data=None, label=None, sample_weight=None, init_score=None,
                 eval_datas=None, eval_labels=None, eval_sample_weights=None, eval_init_scores=None,
                 params=None, kwds=None, lgbm_endpoints=None, lgbm_port=None, tree_learner=None,
                 timeout=None, merge=False, output_types=None, **kw):
        super().__init__(_model_type=model_type, _params=params, _data=data, _label=label,
                         _sample_weight=sample_weight, _init_score=init_score, _eval_datas=eval_datas,
                         _eval_labels=eval_labels, _eval_sample_weights=eval_sample_weights,
                         _eval_init_scores=eval_init_scores, _kwds=kwds, _lgbm_endpoints=lgbm_endpoints,
                         _lgbm_port=lgbm_port, _tree_learner=tree_learner, _timeout=timeout, _merge=merge,
                         _output_types=output_types, **kw)
        if self._output_types is None:
            self._output_types = [OutputType.object]

    @property
    def model_type(self) -> LGBMModelType:
        return self._model_type

    @property
    def data(self):
        return self._data

    @property
    def label(self):
        return self._label

    @property
    def sample_weight(self):
        return self._sample_weight

    @property
    def init_score(self):
        return self._init_score

    @property
    def eval_datas(self) -> list:
        return self._eval_datas or []

    @property
    def eval_labels(self) -> list:
        return self._eval_labels or []

    @property
    def eval_sample_weights(self) -> list:
        return self._eval_sample_weights or []

    @property
    def eval_init_scores(self) -> list:
        return self._eval_init_scores or []

    @property
    def params(self) -> dict:
        return self._params or dict()

    @property
    def kwds(self) -> dict:
        return self._kwds or dict()

    @property
    def lgbm_endpoints(self) -> list:
        return self._lgbm_endpoints

    @property
    def lgbm_port(self) -> int:
        return self._lgbm_port

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def tree_learner(self) -> str:
        return self._tree_learner

    def _set_inputs(self, inputs):
        super()._set_inputs(inputs)
        it = iter(inputs)
        for attr in ['_data', '_label', '_sample_weight', '_init_score']:
            if getattr(self, attr) is not None:
                setattr(self, attr, next(it))
        for attr in ['_eval_datas', '_eval_labels', '_eval_sample_weights', '_eval_init_scores']:
            new_list = []
            for c in getattr(self, attr, None) or []:
                if c is not None:
                    new_list.append(next(it))
            setattr(self, attr, new_list or None)

    def __call__(self):
        inputs = []
        for attr in ['_data', '_label', '_sample_weight', '_init_score']:
            if getattr(self, attr) is not None:
                inputs.append(getattr(self, attr))
        for attr in ['_eval_datas', '_eval_labels', '_eval_sample_weights', '_eval_init_scores']:
            for c in getattr(self, attr, None) or []:
                if c is not None:
                    inputs.append(c)
        return self.new_tileable(inputs)

    @staticmethod
    def _get_data_chunks_workers(ctx, data):
        # data_chunk.inputs is concat, and concat's input is the co-allocated chunks
        metas = ctx.get_chunk_metas([c.key for c in data.chunks])
        return [m.workers[0] for m in metas]

    @staticmethod
    def _concat_chunks_by_worker(chunks, chunk_workers):
        worker_to_chunks = defaultdict(list)
        for chunk, worker in zip(chunks, chunk_workers):
            worker_to_chunks[worker].append(chunk)
        worker_to_concat = dict()
        for worker, chunks in worker_to_chunks.items():
            worker_to_concat[worker] = concat_chunks(chunks)
        return worker_to_concat

    @staticmethod
    def _build_lgbm_endpoints(workers, base_port):
        worker_to_endpoint = dict()
        workers = set(workers)
        base_port = base_port or random.randint(10000, 65535 - len(workers))
        for idx, worker in enumerate(workers):
            worker_to_endpoint[worker] = '%s:%d' % (worker.split(':', 1)[0], base_port + idx)
        return worker_to_endpoint

    @classmethod
    def tile(cls, op: "LGBMTrain"):
        ctx = get_context()
        if ctx.running_mode != RunningMode.distributed:
            assert all(len(inp.chunks) == 1 for inp in op.inputs)

            chunk_op = op.copy().reset_key()
            out_chunk = chunk_op.new_chunk([inp.chunks[0] for inp in op.inputs],
                                           shape=(1,), index=(0,))
            new_op = op.copy()
            return new_op.new_tileables(op.inputs, chunks=[out_chunk], nsplits=((1,),))
        else:
            data = op.data
            worker_to_args = defaultdict(dict)

            workers = cls._get_data_chunks_workers(ctx, data)
            worker_to_endpoint = cls._build_lgbm_endpoints(workers, op.lgbm_port)
            worker_endpoints = list(worker_to_endpoint.values())

            for arg in ['_data', '_label', '_sample_weight', '_init_score']:
                if getattr(op, arg) is not None:
                    for worker, chunk in cls._concat_chunks_by_worker(
                            getattr(op, arg).chunks, workers).items():
                        worker_to_args[worker][arg] = chunk

            eval_workers_list = [cls._get_data_chunks_workers(ctx, d) for d in op.eval_datas]
            extra_workers = reduce(operator.or_, (set(w) for w in eval_workers_list)) - set(workers)
            worker_remap = dict(zip(extra_workers, itertools.cycle(workers)))
            if worker_remap:
                eval_workers_list = [[worker_remap.get(w, w) for w in wl] for wl in eval_workers_list]

            for arg in ['_eval_datas', '_eval_labels', '_eval_sample_weights', '_eval_init_scores']:
                if getattr(op, arg):
                    for tileable, eval_workers in zip(getattr(op, arg), eval_workers_list):
                        for worker, chunk in cls._concat_chunks_by_worker(
                                tileable.chunks, eval_workers).items():
                            if arg not in worker_to_args[worker]:
                                worker_to_args[worker][arg] = []
                            worker_to_args[worker][arg].append(chunk)

            out_chunks = []
            for worker in workers:
                chunk_op = op.copy().reset_key()

                chunk_op._expect_worker = worker
                chunk_op._lgbm_endpoints = worker_endpoints
                chunk_op._lgbm_port = int(worker_to_endpoint[worker].rsplit(':', 1)[-1])

                input_chunks = []
                concat_args = worker_to_args.get(worker, {})
                for arg in ['_data', '_label', '_sample_weight', '_init_score',
                            '_eval_datas', '_eval_labels', '_eval_sample_weights', '_eval_init_scores']:
                    arg_val = getattr(op, arg)
                    if arg_val:
                        arg_chunk = concat_args.get(arg)
                        setattr(chunk_op, arg, arg_chunk)
                        if isinstance(arg_chunk, list):
                            input_chunks.extend(arg_chunk)
                        else:
                            input_chunks.append(arg_chunk)

                data_chunk = concat_args['_data']
                out_chunk = chunk_op.new_chunk(input_chunks, shape=(np.nan,), index=data_chunk.index[:1])
                out_chunks.append(out_chunk)

            new_op = op.copy()
            return new_op.new_tileables(op.inputs, chunks=out_chunks,
                                        nsplits=((np.nan for _ in out_chunks),))

    @classmethod
    def execute(cls, ctx, op: "LGBMTrain"):
        if op.merge:
            return super().execute(ctx, op)

        from lightgbm.basic import _safe_call, _LIB

        data_val = ctx[op.data.key]
        label_val = ctx[op.label.key]
        sample_weight_val = ctx[op.sample_weight.key] if op.sample_weight is not None else None
        init_score_val = ctx[op.init_score.key] if op.init_score is not None else None

        if op.eval_datas is None:
            eval_set, eval_sample_weight, eval_init_score = None, None, None
        else:
            eval_set, eval_sample_weight, eval_init_score = [], [], []
            for data, label in zip(op.eval_datas, op.eval_labels):
                eval_set.append((ctx[data.key], ctx[label.key]))
            for weight in op.eval_sample_weights:
                eval_sample_weight.append(ctx[weight.key] if weight is not None else None)
            for score in op.eval_init_scores:
                eval_init_score.append(ctx[score.key] if score is not None else None)

            eval_set = eval_set or None
            eval_sample_weight = eval_sample_weight or None
            eval_init_score = eval_init_score or None

        params = op.params.copy()
        if ctx.running_mode == RunningMode.distributed:
            params['machines'] = ','.join(op.lgbm_endpoints)
            params['time_out'] = op.timeout
            params['num_machines'] = len(op.lgbm_endpoints)
            params['local_listen_port'] = op.lgbm_port

            if (op.tree_learner or '').lower() not in {'data', 'feature', 'voting'}:
                logger.warning('Parameter tree_learner not set or set to incorrect value %s, '
                               'using "data" as default' % op.tree_learner)
                params['tree_learner'] = 'data'
            else:
                params['tree_learner'] = op.tree_learner

        try:
            model_cls = get_model_cls_from_type(op.model_type)
            model = model_cls(**params)
            model.fit(data_val, label_val, sample_weight=sample_weight_val, init_score=init_score_val,
                      eval_set=eval_set, eval_sample_weight=eval_sample_weight,
                      eval_init_score=eval_init_score, **op.kwds)

            if hasattr(label_val, 'dtype'):
                model.set_params(out_dtype_=label_val.dtype)
            else:
                model.set_params(out_dtype_=label_val.dtypes[0])

            ctx[op.outputs[0].key] = pickle.dumps(model)
        finally:
            _safe_call(_LIB.LGBM_NetworkFree())


def train(params, train_set, eval_sets=None, **kwargs):
    eval_sets = eval_sets or []
    model_type = kwargs.pop('model_type', LGBMModelType.CLASSIFIER)

    evals_result = kwargs.pop('evals_result', dict())
    session = kwargs.pop('session', None)
    run_kwargs = kwargs.pop('run_kwargs', dict())
    timeout = kwargs.pop('timeout', 120)
    base_port = kwargs.pop('base_port', None)

    aligns = align_data_set(train_set)
    for eval_set in eval_sets:
        aligns += align_data_set(eval_set)

    aligned_iter = iter(ExecutableTuple(aligns).execute(session))
    datas, labels, sample_weights, init_scores = [], [], [], []
    for dataset in [train_set] + eval_sets:
        train_kw = dict()
        for arg in ['data', 'label', 'sample_weight', 'init_score']:
            if getattr(dataset, arg) is not None:
                train_kw[arg] = next(aligned_iter)
            else:
                train_kw[arg] = None

        datas.append(train_kw['data'])
        labels.append(train_kw['label'])
        sample_weights.append(train_kw['sample_weight'])
        init_scores.append(train_kw['init_score'])

    op = LGBMTrain(params=params, data=datas[0], label=labels[0], sample_weight=sample_weights[0],
                   init_score=init_scores[0], eval_datas=datas[1:], eval_labels=labels[1:],
                   eval_weights=sample_weights[1:], eval_init_score=init_scores[1:],
                   model_type=model_type, timeout=timeout, lgbm_port=base_port, kwds=kwargs)
    ret = op().execute(session=session, **run_kwargs).fetch(session=session)

    bst = pickle.loads(ret)
    evals_result.update(bst.evals_result_ or {})
    return bst
