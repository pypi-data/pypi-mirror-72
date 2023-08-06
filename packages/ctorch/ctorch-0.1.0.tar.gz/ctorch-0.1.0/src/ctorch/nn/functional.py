import torch
from torch.nn import functional as F

Tensor = torch.Tensor


def complex_linear(
    input: Tensor, real: Tensor, imag: Tensor, bias: Tensor = None
) -> Tensor:
    combined_real = torch.cat([real, -imag], dim=1)
    combined_imag = torch.cat([imag, real], dim=1)
    weight_complex = torch.cat([combined_real, combined_imag], dim=0)
    return F.linear(input, weight_complex, bias)


__all__ = ["complex_linear"]
