from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy import ndarray
from seaborn import JointGrid, PairGrid
from typing import TypeVar, Tuple, Iterable

PlotObject = TypeVar('PlotObject', Axes, Figure, JointGrid, PairGrid)
Color = TypeVar('Color', str, Tuple[float, float, float, float])
FontSize = TypeVar('FontSize', str, float, int)
LegendLocation = TypeVar('LegendLocation', str, Tuple[float, float])
FloatOrFloats = TypeVar('FloatOrFloats', float, Iterable[float])
StringOrStrings = TypeVar('StringOrStrings', str, Iterable[str])
ArrayLike = TypeVar('ArrayLike', ndarray, list)
