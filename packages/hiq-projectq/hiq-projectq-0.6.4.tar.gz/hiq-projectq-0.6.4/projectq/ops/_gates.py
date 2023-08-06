#   Copyright 2017 ProjectQ-Framework (www.projectq.ch)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
Contains definitions of standard gates such as
* Hadamard (H)
* Pauli-X (X / NOT)
* Pauli-Y (Y)
* Pauli-Z (Z)
* S and its inverse (S / Sdagger)
* T and its inverse (T / Tdagger)
* SqrtX gate (SqrtX)
* Swap gate (Swap)
* SqrtSwap gate (SqrtSwap)
* Entangle (Entangle)
* Phase gate (Ph)
* Rotation-X (Rx)
* Rotation-Y (Ry)
* Rotation-Z (Rz)
* Rotation-XX on two qubits (Rxx)
* Rotation-YY on two qubits (Ryy)
* Rotation-ZZ on two qubits (Rzz)
* Phase-shift (R)
* Measurement (Measure)

and meta gates, i.e.,
* Allocate / Deallocate qubits
* Flush gate (end of circuit)
* Barrier
* FlipBits
"""

import cmath
import math
import warnings

import numpy as np
import sympy
from sympy.core.basic import Basic as SympyBase

from projectq.ops import get_inverse
from ._basics import (BasicGate,
                      MatrixGate,
                      SelfInverseGate,
                      BasicRotationGate,
                      BasicPhaseGate,
                      ClassicalInstructionGate,
                      FastForwardingGate,
                      BasicMathGate,
                      DispatchGateClass)
from ._parametric_base import ParametricRotationGate, ParametricPhaseGate
from ._command import apply_command


class HGate(SelfInverseGate):
    """ Hadamard gate class """

    def __str__(self):
        return "H"

    @property
    def matrix(self):
        return 1. / cmath.sqrt(2.) * np.matrix([[1, 1], [1, -1]])


#: Shortcut (instance of) :class:`projectq.ops.HGate`
H = HGate()


class XGate(SelfInverseGate):
    """ Pauli-X gate class """

    def __str__(self):
        return "X"

    @property
    def matrix(self):
        return np.matrix([[0, 1], [1, 0]])


#: Shortcut (instance of) :class:`projectq.ops.XGate`
X = NOT = XGate()


class YGate(SelfInverseGate):
    """ Pauli-Y gate class """

    def __str__(self):
        return "Y"

    @property
    def matrix(self):
        return np.matrix([[0, -1j], [1j, 0]])


#: Shortcut (instance of) :class:`projectq.ops.YGate`
Y = YGate()


class ZGate(SelfInverseGate):
    """ Pauli-Z gate class """

    def __str__(self):
        return "Z"

    @property
    def matrix(self):
        return np.matrix([[1, 0], [0, -1]])


#: Shortcut (instance of) :class:`projectq.ops.ZGate`
Z = ZGate()


class SGate(BasicGate):
    """ S gate class """

    @property
    def matrix(self):
        return np.matrix([[1, 0], [0, 1j]])

    def __str__(self):
        return "S"


#: Shortcut (instance of) :class:`projectq.ops.SGate`
S = SGate()
#: Inverse (and shortcut) of :class:`projectq.ops.SGate`
Sdag = Sdagger = get_inverse(S)


class TGate(BasicGate):
    """ T gate class """

    @property
    def matrix(self):
        return np.matrix([[1, 0], [0, cmath.exp(1j * cmath.pi / 4)]])

    def __str__(self):
        return "T"


#: Shortcut (instance of) :class:`projectq.ops.TGate`
T = TGate()
#: Inverse (and shortcut) of :class:`projectq.ops.TGate`
Tdag = Tdagger = get_inverse(T)


class SqrtXGate(BasicGate):
    """ Square-root X gate class """

    @property
    def matrix(self):
        return 0.5 * np.matrix([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]])

    def tex_str(self):
        return r'$\sqrt{X}$'

    def __str__(self):
        return "SqrtX"


#: Shortcut (instance of) :class:`projectq.ops.SqrtXGate`
SqrtX = SqrtXGate()


class SwapGate(SelfInverseGate):
    """ Swap gate class (swaps 2 qubits) """

    def __init__(self):
        SelfInverseGate.__init__(self)
        self.interchangeable_qubit_indices = [[0, 1]]

    def __str__(self):
        return "Swap"

    @property
    def matrix(self):
        return np.matrix([[1, 0, 0, 0],
                          [0, 0, 1, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 1]])


#: Shortcut (instance of) :class:`projectq.ops.SwapGate`
Swap = SwapGate()


class SqrtSwapGate(BasicGate):
    """ Square-root Swap gate class """

    def __init__(self):
        BasicGate.__init__(self)
        self.interchangeable_qubit_indices = [[0, 1]]

    def __str__(self):
        return "SqrtSwap"

    @property
    def matrix(self):
        return np.matrix([[1, 0, 0, 0],
                          [0, 0.5+0.5j, 0.5-0.5j, 0],
                          [0, 0.5-0.5j, 0.5+0.5j, 0],
                          [0, 0, 0, 1]])


#: Shortcut (instance of) :class:`projectq.ops.SqrtSwapGate`
SqrtSwap = SqrtSwapGate()


class EntangleGate(BasicGate):
    """
    Entangle gate (Hadamard on first qubit, followed by CNOTs applied to all
    other qubits).
    """

    def __str__(self):
        return "Entangle"


#: Shortcut (instance of) :class:`projectq.ops.EntangleGate`
Entangle = EntangleGate()


class DispatchAngleGateClass(DispatchGateClass):
    """Dispatch base class for angle gate classes (phase- and rotation- gates)"""
    def __new__(cls, NumClass, ParamClass, angle):
        if angle is not None:
            if isinstance(angle, SympyBase):
                # NB: here we do not consider sympy.Float and sympy.Integer as
                # numbers since operation on them such as +, *, etc. will lead
                # to expressions and not simple numbers
                return super().__new__(ParamClass)
            return super().__new__(NumClass)

        # This statement is only for copy and deepcopy operations
        return super().__new__(cls)

    def __init__(self, angle):
        # pylint: disable=useless-super-delegation
        super().__init__(angle)


# Dispatch class for R gates
class Ph(DispatchAngleGateClass):
    """ Phase gate (global phase) """
    def __new__(cls, angle=None):
        return super().__new__(cls, PhNum, PhParam, angle)


class PhParam(Ph, ParametricPhaseGate):
    @property
    def matrix(self):
        return sympy.Matrix([[sympy.exp(1j * self.angle), 0],
                             [0, sympy.exp(1j * self.angle)]])


class PhNum(Ph, BasicPhaseGate):
    @property
    def matrix(self):
        return np.matrix([[cmath.exp(1j * self.angle), 0],
                          [0, cmath.exp(1j * self.angle)]])


# Dispatch class for Rx gates
class Rx(DispatchAngleGateClass):
    """ RotationX gate class """
    def __new__(cls, angle=None):
        return super().__new__(cls, RxNum, RxParam, angle)


class RxParam(Rx, ParametricRotationGate):
    @property
    def matrix(self):
        return sympy.Matrix([[sympy.cos(0.5 * self.angle),
                              -1j * sympy.sin(0.5 * self.angle)],
                             [-1j * sympy.sin(0.5 * self.angle),
                              sympy.cos(0.5 * self.angle)]])


class RxNum(Rx, BasicRotationGate):
    @property
    def matrix(self):
        return np.matrix([[math.cos(0.5 * self.angle),
                           -1j * math.sin(0.5 * self.angle)],
                          [-1j * math.sin(0.5 * self.angle),
                           math.cos(0.5 * self.angle)]])


# Dispatch class for Ry gates
class Ry(DispatchAngleGateClass):
    """ RotationY gate class """
    def __new__(cls, angle=None):
        return super().__new__(cls, RyNum, RyParam, angle)


class RyParam(Ry, ParametricRotationGate):
    @property
    def matrix(self):
        return sympy.Matrix([[sympy.cos(0.5 * self.angle),
                              -sympy.sin(0.5 * self.angle)],
                             [sympy.sin(0.5 * self.angle),
                              sympy.cos(0.5 * self.angle)]])


class RyNum(Ry, BasicRotationGate):
    @property
    def matrix(self):
        return np.matrix([[math.cos(0.5 * self.angle),
                           -math.sin(0.5 * self.angle)],
                          [math.sin(0.5 * self.angle),
                           math.cos(0.5 * self.angle)]])


# Dispatch class for Rz gates
class Rz(DispatchAngleGateClass):
    """ RotationZ gate class """
    def __new__(cls, angle=None):
        return super().__new__(cls, RzNum, RzParam, angle)


class RzParam(Rz, ParametricRotationGate):
    @property
    def matrix(self):
        return sympy.Matrix([[sympy.exp(-.5 * 1j * self.angle), 0],
                             [0, sympy.exp(.5 * 1j * self.angle)]])


class RzNum(Rz, BasicRotationGate):
    @property
    def matrix(self):
        return np.matrix([[cmath.exp(-.5 * 1j * self.angle), 0],
                          [0, cmath.exp(.5 * 1j * self.angle)]])


# Dispatch class for Rxx gates
class Rxx(DispatchAngleGateClass):
    """ RotationXX gate class """
    def __new__(cls, angle=None):
        return super().__new__(cls, RxxNum, RxxParam, angle)


class RxxParam(Rxx, ParametricRotationGate):
    @property
    def matrix(self):
        return sympy.Matrix([[sympy.cos(.5 * self.angle), 0, 0, -1j*sympy.sin(.5 * self.angle)],
                             [0, sympy.cos( .5 * self.angle), -1j*sympy.sin(.5 * self.angle), 0],
                             [0, -1j*sympy.sin(.5 * self.angle), sympy.cos( .5 * self.angle), 0],
                             [-1j*sympy.sin(.5 * self.angle), 0, 0, sympy.cos( .5 * self.angle)]])


class RxxNum(Rxx, BasicRotationGate):
    @property
    def matrix(self):
        return np.matrix([
            [cmath.cos(.5 * self.angle), 0, 0, -1j*cmath.sin(.5 * self.angle)],
            [0, cmath.cos(.5 * self.angle), -1j*cmath.sin(.5 * self.angle), 0],
            [0, -1j*cmath.sin(.5 * self.angle), cmath.cos(.5 * self.angle), 0],
            [-1j*cmath.sin(.5 * self.angle), 0, 0, cmath.cos(.5 * self.angle)]
        ])


# Dispatch class for Ryy gates
class Ryy(DispatchAngleGateClass):
    """ RotationYY gate class """
    def __new__(cls, angle=None):
        return super().__new__(cls, RyyNum, RyyParam, angle)


class RyyParam(Ryy, ParametricRotationGate):
    @property
    def matrix(self):
        return sympy.Matrix([[sympy.cos(.5 * self.angle), 0, 0, 1j*sympy.sin(.5 * self.angle)],
                             [0, sympy.cos( .5 * self.angle), -1j*sympy.sin(.5 * self.angle), 0],
                             [0, -1j*sympy.sin(.5 * self.angle), sympy.cos( .5 * self.angle), 0],
                             [1j*sympy.sin(.5 * self.angle), 0, 0, sympy.cos( .5 * self.angle)]])


class RyyNum(Ryy, BasicRotationGate):
    @property
    def matrix(self):
        return np.matrix([
            [cmath.cos(.5*self.angle), 0, 0, 1j*cmath.sin(.5 * self.angle)],
            [0, cmath.cos(.5 * self.angle), -1j*cmath.sin(.5 * self.angle), 0],
            [0, -1j*cmath.sin(.5 * self.angle), cmath.cos(.5 * self.angle), 0],
            [1j*cmath.sin(.5 * self.angle), 0, 0, cmath.cos(.5 * self.angle)]])


# Dispatch class for Rzz gates
class Rzz(DispatchAngleGateClass):
    """ RotationZZ gate class """
    def __new__(cls, angle=None):
        return super().__new__(cls, RzzNum, RzzParam, angle)


class RzzParam(Rzz, ParametricRotationGate):
    @property
    def matrix(self):
        return sympy.Matrix([[sympy.exp(-.5 * 1j * self.angle), 0, 0, 0],
                             [0, sympy.exp( .5 * 1j * self.angle), 0, 0],
                             [0, 0, sympy.exp( .5 * 1j * self.angle), 0],
                             [0, 0, 0, sympy.exp(-.5 * 1j * self.angle)]])


class RzzNum(Rzz, BasicRotationGate):
    @property
    def matrix(self):
        return np.matrix([
            [cmath.exp(-.5 * 1j * self.angle), 0, 0, 0],
            [0, cmath.exp(.5 * 1j * self.angle), 0, 0],
            [0, 0, cmath.exp(.5 * 1j * self.angle), 0],
            [0, 0, 0, cmath.exp(-.5 * 1j * self.angle)]])


# Dispatch class for R gates
class R(DispatchAngleGateClass):
    """ Phase-shift gate (equivalent to Rz up to a global phase) """
    def __new__(cls, angle=None):
        return super().__new__(cls, RNum, RParam, angle)


class RParam(R, ParametricPhaseGate):
    @property
    def matrix(self):
        return sympy.Matrix([[1, 0], [0, sympy.exp(1j * self.angle)]])


class RNum(R, BasicPhaseGate):
    @property
    def matrix(self):
        return np.matrix([[1, 0], [0, cmath.exp(1j * self.angle)]])


class FlushGate(FastForwardingGate):
    """
    Flush gate (denotes the end of the circuit).

    Note:
        All compiler engines (cengines) which cache/buffer gates are obligated
        to flush and send all gates to the next compiler engine (followed by
        the flush command).

    Note:
        This gate is sent when calling

        .. code-block:: python

            eng.flush()

        on the MainEngine `eng`.
    """

    def __str__(self):
        return ""


class MeasureGate(FastForwardingGate):
    """ Measurement gate class (for single qubits)."""

    def __str__(self):
        return "Measure"

    def __or__(self, qubits):
        """
        Previously (ProjectQ <= v0.3.6) MeasureGate/Measure was allowed to be
        applied to any number of quantum registers. Now the MeasureGate/Measure
        is strictly a single qubit gate. In the coming releases the backward
        compatibility will be removed!
        """
        num_qubits = 0
        for qureg in self.make_tuple_of_qureg(qubits):
            for qubit in qureg:
                num_qubits += 1
                cmd = self.generate_command(([qubit], ))
                apply_command(cmd)
        if num_qubits > 1:
            warnings.warn("Pending syntax change in future versions of "
                          "ProjectQ: \n Measure will be a single qubit gate "
                          "only. Use `All(Measure) | qureg` instead to "
                          "measure multiple qubits.")


#: Shortcut (instance of) :class:`projectq.ops.MeasureGate`
Measure = MeasureGate()


class AllocateQubitGate(ClassicalInstructionGate):
    """ Qubit allocation gate class """

    def __str__(self):
        return "Allocate"

    def get_inverse(self):
        return DeallocateQubitGate()


#: Shortcut (instance of) :class:`projectq.ops.AllocateQubitGate`
Allocate = AllocateQubitGate()


class DeallocateQubitGate(FastForwardingGate):
    """ Qubit deallocation gate class """

    def __str__(self):
        return "Deallocate"

    def get_inverse(self):
        return Allocate


#: Shortcut (instance of) :class:`projectq.ops.DeallocateQubitGate`
Deallocate = DeallocateQubitGate()


class AllocateDirtyQubitGate(ClassicalInstructionGate):
    """ Dirty qubit allocation gate class """

    def __str__(self):
        return "AllocateDirty"

    def get_inverse(self):
        return Deallocate


#: Shortcut (instance of) :class:`projectq.ops.AllocateDirtyQubitGate`
AllocateDirty = AllocateDirtyQubitGate()


class BarrierGate(BasicGate):
    """ Barrier gate class """

    def __str__(self):
        return "Barrier"

    def get_inverse(self):
        return Barrier


#: Shortcut (instance of) :class:`projectq.ops.BarrierGate`
Barrier = BarrierGate()


class FlipBits(SelfInverseGate):
    """ Gate for flipping qubits by means of XGates """
    def __init__(self, bits_to_flip):
        """
        Initialize FlipBits gate.

        Example:
            .. code-block:: python

                qureg = eng.allocate_qureg(2)
                FlipBits([0, 1]) | qureg

        Args:
            bits_to_flip(list[int]|list[bool]|str|int): int or array of 0/1,
               True/False, or string of 0/1 identifying the qubits to flip.
               In case of int, the bits to flip are determined from the
               binary digits, with the least significant bit corresponding
               to qureg[0]. If bits_to_flip is negative, exactly all qubits
               which would not be flipped for the input -bits_to_flip-1 are
               flipped, i.e., bits_to_flip=-1 flips all qubits.
        """
        SelfInverseGate.__init__(self)
        if isinstance(bits_to_flip, int):
            self.bits_to_flip = bits_to_flip
        else:
            self.bits_to_flip = 0
            for i in reversed(list(bits_to_flip)):
                bit = 0b1 if i == '1' or i == 1 or i is True else 0b0
                self.bits_to_flip = (self.bits_to_flip << 1) | bit

    def __str__(self):
        return "FlipBits("+str(self.bits_to_flip)+")"

    def __or__(self, qubits):
        quregs_tuple = self.make_tuple_of_qureg(qubits)
        if len(quregs_tuple) > 1:
            raise ValueError(self.__str__()+' can only be applied to qubits,'
                             'quregs, arrays of qubits, and tuples with one'
                             'individual qubit')
        for qureg in quregs_tuple:
            for i, qubit in enumerate(qureg):
                if (self.bits_to_flip >> i) & 1:
                    XGate() | qubit

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.bits_to_flip == other.bits_to_flip
        return False

    def __hash__(self):
        return hash(self.__str__())
