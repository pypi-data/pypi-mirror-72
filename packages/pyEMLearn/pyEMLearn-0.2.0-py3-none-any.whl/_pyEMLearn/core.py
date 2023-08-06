import numpy as np

from cmath import sqrt as _sqrt
sqrt = np.vectorize(_sqrt)


class Modes:
    def __init__(self):
        pass

    def __repr__(self):
        return "<Base Modes Object>"

    def __call__(self):
        raise NotImplementedError("Virtual Method")

class HILMModes(Modes):
    def __init__(self):
        self.update(0j,0j,1,1)

    def update(self,kx,ky,er,mr):
        # self.kx, self.ky = kx, ky
        ks = er*mr
        kxs, kys, kxy = kx*kx, ky*ky ,kx*ky
        self.kz = _sqrt(ks - kxs - kys)

        R = np.array([
            [    kxy, ks-kxs ],
            [ kys-ks,   -kxy ]
        ])
        self.P, self.Q = R/er, R/mr

    def solve(self):
        _lam = sqrt((1j * self.kz)**2)
        self.lam = np.array([_lam, _lam])
        self.X = lambda zp: np.diag(np.exp(self.lam * zp))

        self.W = np.eye(2) + 0j
        self.W_inv = self.W.copy()
        self.V = self.Q @ np.diag(1/self.lam)
        self.V_inv = np.diag(1/self.lam) @ self.P

class HALMModes(Modes):
    # TODO:
    raise NotImplementedError("TODO: Implement")

class RCWAModes(Modes):
    def __init__(self,S):
        self.update(np.zeros((S,S))+0j,np.zeros((S,S))+0j,
                    np.ones((S,S))+0j,np.ones((S,S))+0j)

    def update(self, Kx, Ky, Er, Mr):
        # Kx,Ky,Er,Mr are all SxS matricies in the nu basis

        Er_inv = np.linalg.inv(Er)
        Mr_inv = np.linalg.inv(Mr)

        Er_inv_x = Kx @ Er_inv
        Er_inv_y = Ky @ Er_inv
        Mr_inv_x = Kx @ Mr_inv
        Mr_inv_y = Ky @ Mr_inv

        Er_inv_xx = Er_inv_x @ Kx
        Er_inv_xy = Er_inv_x @ Ky
        Er_inv_yx = Er_inv_y @ Kx
        Er_inv_yy = Er_inv_y @ Ky

        Mr_inv_xx = Mr_inv_x @ Kx
        Mr_inv_xy = Mr_inv_x @ Ky
        Mr_inv_yx = Mr_inv_y @ Kx
        Mr_inv_yy = Mr_inv_y @ Ky

        self.P = np.bmat([
            [      Er_inv_xy, Mr - Er_inv_xx ],
            [ Er_inv_yy - Mr,    - Er_inv_yx ]
        ])
        self.Q = np.bmat([
            [      Mr_inv_xy, Er - Mr_inv_xx ],
            [ Mr_inv_yy - Er,    - Mr_inv_yx ]
        ])

    def solve(self):
        Osq = self.P @ self.Q
        lamsq, self.W = np.linalg.eig(Osq)
        self.lam = sqrt(lamsq)
        self.W_inv = W.T.conj() # np.linalg.inv(W)
        self.V = self.Q @ self.W @ np.diag(1/self.lam)
        self.V_inv = np.diag(1/self.lam) @ self.W_inv @ self.P# np.linalg.inv(V)

class RCWAModesDiagonal(Modes):
    def __init__(self,S):
        self.update(np.zeros((S,S))+0j,np.zeros((S,S))+0j,
                    np.ones((S,S))+0j,np.ones((S,S))+0j)

    def update(self, Kx, Ky, Er, Mr):
        # Kx,Ky,Er,Mr are all S vectors in the nu basis
        # self.Kx, self.Ky = Kx, Ky
        Ks = Er * Mr
        Kxs, Kys, Kxy = Kx*Kx, Ky*Ky ,Kx*Ky
        self.Kz = sqrt(Ks - Kxs - Kys)

        self.P = np.array([
            [         np.diag(Kxy/Er), np.diag(Ks/Er - Kxs/Er) ],
            [ np.diag(Kys/Er - Ks/Er),        -np.diag(Kxy/Er) ]
        ])
        self.Q = np.array([
            [         np.diag(Kxy/Mr), np.diag(Ks/Mr - Kxs/Mr) ],
            [ np.diag(Kys/Mr - Ks/Mr),        -np.diag(Kxy/Mr) ]
        ])


    def solve(self):
        _lam = sqrt((1j*self.Kz)**2)
        self.lam = np.append(_lam,_lam)
        self.W = np.eye(len(self.lam)) + 0j
        self.W_inv = W.copy() # np.linalg.inv(W)
        self.V = self.Q @ np.diag(1/self.lam)
        self.V_inv = np.diag(1/self.lam) @ self.P# np.linalg.inv(V)
