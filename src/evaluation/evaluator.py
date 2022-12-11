from io import BytesIO, StringIO

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, Type, Union
import pandas as pd
import os

from src.evaluation.metric import Metric

import numpy as np

class Evaluator(ABC):
    @classmethod
    @abstractmethod
    def metrics(cls) -> Tuple[Type[Metric], ...]:
        pass

    @abstractmethod
    def evaluate(self, filepath: Path) -> Tuple[Metric, ...]:
        pass

    @abstractmethod
    def validate_submission(self, io_stream: Union[StringIO, BytesIO]) -> bool:
        pass

class Accuracy(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Accuracy'

    @classmethod
    def higher_is_better(cls) -> bool:
        return True

class Parameters(Metric):
    @classmethod
    def name(cls) -> str:
        return 'Parameters'

    @classmethod
    def higher_is_better(cls) -> bool:
        return False

class PokemonEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        self.y = pd.read_csv(os.path.join('src', 'evaluation', 'assets', 'test.csv'))

    @classmethod
    def metrics(cls) -> Tuple[Type[Metric], ...]:
        return (Accuracy, Parameters)

    def evaluate(self, filepath: Path):
        pred = pd.read_csv(filepath)[['filename', 'prediction']]
        parameters = pred.iloc[-1]['filename']
        pred.drop(pred.index[-1], inplace=True)
        df = pd.concat([self.y.set_index('filename'), pred.set_index('filename')], axis=1, join='inner')
        acc = np.count_nonzero(df['label'] == df['prediction']) / df.shape[0]
        return [acc, parameters]
    
    def validate_submission(self, io_stream: Union[StringIO, BytesIO]) -> bool:
        return True
