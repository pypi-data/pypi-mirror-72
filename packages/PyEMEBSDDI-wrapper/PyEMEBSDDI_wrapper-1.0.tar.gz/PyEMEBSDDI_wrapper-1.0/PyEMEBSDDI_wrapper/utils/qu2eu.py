"""
BSD 3-Clause License

Copyright (c) 2020, Zihao Ding, Marc De Graef Research Group/Carnegie Mellon University
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from math import sin, cos, pi, sqrt, atan2
import numpy as np

def qu2eu(qu):
    '''
    input: quaternions, 1darray (4,)
    output: euler angles, 1darray (3,), unit is in rad
    default value of eps = 1
    '''

    eps = 1

    q03 = qu[0]**2 + qu[3]**2
    q12 = qu[1]**2 + qu[2]**2
    chi = sqrt(q03*q12)

    if chi == 0 and q12 == 0:
        result = np.array([atan2(-2*eps*qu[0]*qu[3], qu[0]**2-qu[3]**2), 0, 0])
    elif chi == 0 and q03 == 0:
        result = np.array([atan2(2*qu[1]*qu[2], qu[1]**2-qu[2]**2), pi, 0])
    else:
        result = np.array([atan2((qu[1]*qu[3]-eps*qu[0]*qu[2])/chi, (-eps*qu[0]*qu[1]-qu[2]*qu[3])/chi),
                            atan2(2*chi, q03-q12),
                            atan2((eps*qu[0]*qu[2]+qu[1]*qu[3])/chi, (-eps*qu[0]*qu[1]+qu[2]*qu[3])/chi)])

    # reduce Euler angles to definition ranges (and positive values only)
    if result[0] < 0.0:
        result[0] = (result[0]+100.*pi)%(2.*pi)
    if result[1] < 0.0:
        result[1] = (result[1]+100.*pi)%pi
    if result[2] < 0.0:
        result[2] = (result[2]+100.*pi)%(2.*pi)

    return result