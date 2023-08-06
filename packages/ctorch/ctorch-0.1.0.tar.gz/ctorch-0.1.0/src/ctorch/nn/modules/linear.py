import math

import torch
from torch import nn
from torch.nn import init

from .. import functional as C

Tensor = torch.Tensor


class ComplexLinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features
        self.weight_real = nn.Parameter(torch.Tensor(out_features, in_features))
        self.weight_imag = nn.Parameter(torch.Tensor(out_features, in_features))
        if bias:
            self.bias = nn.Parameter(torch.Tensor(2 * out_features))
            # self.bias_imag = nn.Parameter(torch.Tensor(out_features))
        else:
            self.bias = self.register_parameter("bias", None)
            # self.bias_imag = self.register_parameter("bias_imag", None)
        self.reset_parameters()

    def reset_parameters(self):
        init.kaiming_uniform_(self.weight_real, a=math.sqrt(5))
        init.kaiming_uniform_(self.weight_imag, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight_real)
            bound = 1 / math.sqrt(fan_in)
            init.uniform_(self.bias, -bound, bound)

    def forward(self, x: Tensor) -> Tensor:
        return C.complex_linear(x, self.weight_real, self.weight_imag, self.bias)


__all__ = ["ComplexLinear"]
