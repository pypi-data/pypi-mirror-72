import inspect
import pickle
import platform

import pytest

import tests.base.develop_utils as tutils
from pytorch_lightning import Trainer, Callback
from pytorch_lightning.loggers import (
    TensorBoardLogger,
    MLFlowLogger,
    NeptuneLogger,
    TestTubeLogger,
    CometLogger,
    WandbLogger,
)
from pytorch_lightning.loggers.base import DummyExperiment
from tests.base import EvalModelTemplate


def _get_logger_args(logger_class, save_dir):
    logger_args = {}
    if 'save_dir' in inspect.getfullargspec(logger_class).args:
        logger_args.update(save_dir=str(save_dir))
    if 'offline_mode' in inspect.getfullargspec(logger_class).args:
        logger_args.update(offline_mode=True)
    if 'offline' in inspect.getfullargspec(logger_class).args:
        logger_args.update(offline=True)
    return logger_args


@pytest.mark.parametrize("logger_class", [
    TensorBoardLogger,
    CometLogger,
    MLFlowLogger,
    NeptuneLogger,
    TestTubeLogger,
    # WandbLogger,  # TODO: add this one
])
def test_loggers_fit_test(tmpdir, monkeypatch, logger_class):
    """Verify that basic functionality of all loggers."""
    # prevent comet logger from trying to print at exit, since
    # pytest's stdout/stderr redirection breaks it
    import atexit
    monkeypatch.setattr(atexit, 'register', lambda _: None)

    model = EvalModelTemplate()

    class StoreHistoryLogger(logger_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.history = []

        def log_metrics(self, metrics, step):
            super().log_metrics(metrics, step)
            self.history.append((step, metrics))

    logger_args = _get_logger_args(logger_class, tmpdir)
    logger = StoreHistoryLogger(**logger_args)

    trainer = Trainer(
        max_epochs=1,
        logger=logger,
        limit_train_batches=0.2,
        limit_val_batches=0.5,
        fast_dev_run=True,
    )
    trainer.fit(model)

    trainer.test()

    log_metric_names = [(s, sorted(m.keys())) for s, m in logger.history]
    assert log_metric_names == [(0, ['epoch', 'val_acc', 'val_loss']),
                                (0, ['epoch', 'train_some_val']),
                                (1, ['epoch', 'test_acc', 'test_loss'])]


@pytest.mark.parametrize("logger_class", [
    TensorBoardLogger,
    CometLogger,
    MLFlowLogger,
    NeptuneLogger,
    TestTubeLogger,
    # WandbLogger,  # TODO: add this one
])
def test_loggers_pickle(tmpdir, monkeypatch, logger_class):
    """Verify that pickling trainer with logger works."""
    # prevent comet logger from trying to print at exit, since
    # pytest's stdout/stderr redirection breaks it
    import atexit
    monkeypatch.setattr(atexit, 'register', lambda _: None)

    logger_args = _get_logger_args(logger_class, tmpdir)
    logger = logger_class(**logger_args)

    # test pickling loggers
    pickle.dumps(logger)

    trainer = Trainer(
        max_epochs=1,
        logger=logger,
    )
    pkl_bytes = pickle.dumps(trainer)

    trainer2 = pickle.loads(pkl_bytes)
    trainer2.logger.log_metrics({'acc': 1.0})


@pytest.mark.parametrize("extra_params", [
    pytest.param(dict(max_epochs=1, auto_scale_batch_size=True), id='Batch-size-Finder'),
    pytest.param(dict(max_epochs=3, auto_lr_find=True), id='LR-Finder'),
])
def test_logger_reset_correctly(tmpdir, extra_params):
    """ Test that the tuners do not alter the logger reference """
    tutils.reset_seed()

    model = EvalModelTemplate()

    trainer = Trainer(
        default_root_dir=tmpdir,
        **extra_params,
    )
    logger1 = trainer.logger
    trainer.fit(model)
    logger2 = trainer.logger
    logger3 = model.logger

    assert logger1 == logger2, \
        'Finder altered the logger of trainer'
    assert logger2 == logger3, \
        'Finder altered the logger of model'


class RankZeroLoggerCheck(Callback):
    # this class has to be defined outside the test function, otherwise we get pickle error
    # due to the way ddp process is launched

    def on_batch_start(self, trainer, pl_module):
        is_dummy = isinstance(trainer.logger.experiment, DummyExperiment)
        if trainer.is_global_zero:
            assert not is_dummy
        else:
            assert is_dummy
            assert pl_module.logger.experiment.something(foo="bar") is None


@pytest.mark.skipif(platform.system() == "Windows", reason="Distributed training is not supported on Windows")
@pytest.mark.parametrize("logger_class", [
    TensorBoardLogger,
    CometLogger,
    #MLFlowLogger,
    NeptuneLogger,
    TestTubeLogger,
    WandbLogger,
])
def test_logger_created_on_rank_zero_only(tmpdir, logger_class):
    logger_args = _get_logger_args(logger_class, tmpdir)
    logger = logger_class(**logger_args)
    model = EvalModelTemplate()
    trainer = Trainer(
        logger=logger,
        default_root_dir=tmpdir,
        distributed_backend='ddp_cpu',
        num_processes=2,
        max_steps=1,
        checkpoint_callback=True,
        callbacks=[RankZeroLoggerCheck()],
    )
    result = trainer.fit(model)
    assert result == 1
