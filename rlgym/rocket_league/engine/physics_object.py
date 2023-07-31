import numpy as np
from rlgym.utils import math


class PhysicsObject:

    position: np.ndarray
    linear_velocity: np.ndarray
    angular_velocity: np.ndarray
    _quaternion: np.ndarray
    _rotation_mtx: np.ndarray
    _euler_angles: np.ndarray

    @property
    def quaternion(self) -> np.ndarray:
        if self._quaternion is None:
            if self._rotation_mtx is not None:
                self._quaternion = math.rotation_to_quaternion(self._rotation_mtx)
            elif self._euler_angles is not None:
                #TODO support from euler for RLBot compat
                raise NotImplementedError
            else:
                raise ValueError
        return self._quaternion

    @quaternion.setter
    def quaternion(self, val: np.ndarray):
        self._quaternion = val

    @property
    def rotation_mtx(self) -> np.ndarray:
        if self._rotation_mtx is None:
            if self._quaternion is not None:
                self._rotation_mtx = math.quat_to_rot_mtx(self._quaternion)
            elif self._euler_angles is not None:
                self._rotation_mtx = math.euler_to_rotation(self._euler_angles)
            else:
                raise ValueError
        return self._rotation_mtx

    @rotation_mtx.setter
    def rotation_mtx(self, val: np.ndarray):
        self._rotation_mtx = val

    @property
    def euler_angles(self) -> np.ndarray:
        if self._euler_angles is None:
            if self._quaternion is not None:
                self._euler_angles = math.quat_to_euler(self._quaternion)
            elif self._rotation_mtx is not None:
                #TODO support from rot mtx
                raise NotImplementedError
            else:
                raise ValueError
        return self._euler_angles

    @euler_angles.setter
    def euler_angles(self, val: np.ndarray):
        self._euler_angles = val

    @property
    def forward(self) -> np.ndarray:
        return self.rotation_mtx[:, 0]

    @property
    def right(self) -> np.ndarray:
        return self.rotation_mtx[:, 1]

    @property
    def left(self) -> np.ndarray:
        return self.rotation_mtx[:, 1] * -1

    @property
    def up(self) -> np.ndarray:
        return self.rotation_mtx[:, 2]

    @property
    def pitch(self) -> float:
        return self.euler_angles[0]

    @property
    def yaw(self) -> float:
        return self.euler_angles[1]

    @property
    def roll(self) -> float:
        return self.euler_angles[2]

    def __str__(self):
        return "{} | {} | {} | {} | {} | {}".format(self.position.tolist(),
                                                    self.linear_velocity.tolist(),
                                                    self.angular_velocity.tolist(),
                                                    self.quaternion.tolist(),
                                                    self.euler_angles.tolist(),
                                                    self.rotation_mtx.ravel().tolist())
