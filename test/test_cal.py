import sys
from pathlib import Path

pth = Path(__file__).parent.parent
sys.path.append(pth)

print(pth)

from ths_slj.analysis import bh_method


def test_bh():
    x = np.array([0.01, 0.023, 0.3, 0.52])
    x_adjusted, k = bh_method(x)
    assert k == 2
