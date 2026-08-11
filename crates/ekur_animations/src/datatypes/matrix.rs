use std::ops::Mul;

use crate::datatypes::{quaternion::Quaternion, vector::Vector3};

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Matrix4 {
    pub m: [[f32; 4]; 4],
}

impl Matrix4 {
    pub const IDENTITY: Self = Self {
        m: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
    };

    pub fn from_loc_rot_scale(t: Vector3, q: Quaternion, s: f32) -> Self {
        let r = q.normalized();
        // 3×3 rotation from the quaternion.
        let (x, y, z, w) = (r.x, r.y, r.z, r.w);
        let (xx, yy, zz) = (x * x, y * y, z * z);
        let (xy, xz, yz) = (x * y, x * z, y * z);
        let (wx, wy, wz) = (w * x, w * y, w * z);
        let r00 = 1.0 - 2.0 * (yy + zz);
        let r01 = 2.0 * (xy - wz);
        let r02 = 2.0 * (xz + wy);
        let r10 = 2.0 * (xy + wz);
        let r11 = 1.0 - 2.0 * (xx + zz);
        let r12 = 2.0 * (yz - wx);
        let r20 = 2.0 * (xz - wy);
        let r21 = 2.0 * (yz + wx);
        let r22 = 1.0 - 2.0 * (xx + yy);
        Self {
            m: [
                [r00 * s, r01 * s, r02 * s, t.x],
                [r10 * s, r11 * s, r12 * s, t.y],
                [r20 * s, r21 * s, r22 * s, t.z],
                [0.0, 0.0, 0.0, 1.0],
            ],
        }
    }

    pub fn inverse(&self) -> Self {
        let a = &self.m;
        let (a00, a01, a02) = (a[0][0], a[0][1], a[0][2]);
        let (a10, a11, a12) = (a[1][0], a[1][1], a[1][2]);
        let (a20, a21, a22) = (a[2][0], a[2][1], a[2][2]);
        let det = a00 * (a11 * a22 - a12 * a21) - a01 * (a10 * a22 - a12 * a20)
            + a02 * (a10 * a21 - a11 * a20);
        if det.abs() < 1e-20 {
            return Self::IDENTITY;
        }
        let inv = 1.0 / det;
        // Inverse of the 3×3 (transpose of cofactor matrix × 1/det).
        let i00 = (a11 * a22 - a12 * a21) * inv;
        let i01 = (a02 * a21 - a01 * a22) * inv;
        let i02 = (a01 * a12 - a02 * a11) * inv;
        let i10 = (a12 * a20 - a10 * a22) * inv;
        let i11 = (a00 * a22 - a02 * a20) * inv;
        let i12 = (a02 * a10 - a00 * a12) * inv;
        let i20 = (a10 * a21 - a11 * a20) * inv;
        let i21 = (a01 * a20 - a00 * a21) * inv;
        let i22 = (a00 * a11 - a01 * a10) * inv;
        let (tx, ty, tz) = (a[0][3], a[1][3], a[2][3]);
        // -inv3x3 * t
        let nx = -(i00 * tx + i01 * ty + i02 * tz);
        let ny = -(i10 * tx + i11 * ty + i12 * tz);
        let nz = -(i20 * tx + i21 * ty + i22 * tz);
        Self {
            m: [
                [i00, i01, i02, nx],
                [i10, i11, i12, ny],
                [i20, i21, i22, nz],
                [0.0, 0.0, 0.0, 1.0],
            ],
        }
    }

    pub fn decompose(&self) -> (Vector3, Quaternion, f32) {
        let a = &self.m;
        let t = Vector3 {
            x: a[0][3],
            y: a[1][3],
            z: a[2][3],
        };
        // Column lengths = per-axis scale.
        let sx = (a[0][0] * a[0][0] + a[1][0] * a[1][0] + a[2][0] * a[2][0]).sqrt();
        let sy = (a[0][1] * a[0][1] + a[1][1] * a[1][1] + a[2][1] * a[2][1]).sqrt();
        let sz = (a[0][2] * a[0][2] + a[1][2] * a[1][2] + a[2][2] * a[2][2]).sqrt();
        let scale = (sx + sy + sz) / 3.0;
        // Normalized rotation matrix columns.
        let (ix, iy, iz) = (safe_div(sx), safe_div(sy), safe_div(sz));
        let r00 = a[0][0] * ix;
        let r01 = a[0][1] * iy;
        let r02 = a[0][2] * iz;
        let r10 = a[1][0] * ix;
        let r11 = a[1][1] * iy;
        let r12 = a[1][2] * iz;
        let r20 = a[2][0] * ix;
        let r21 = a[2][1] * iy;
        let r22 = a[2][2] * iz;
        let q = quat_from_mat3([[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]]);
        (t, q, scale)
    }
}

fn quat_from_mat3(r: [[f32; 3]; 3]) -> Quaternion {
    let trace = r[0][0] + r[1][1] + r[2][2];
    let q = if trace > 0.0 {
        let s = (trace + 1.0).sqrt() * 2.0;
        Quaternion {
            w: 0.25 * s,
            x: (r[2][1] - r[1][2]) / s,
            y: (r[0][2] - r[2][0]) / s,
            z: (r[1][0] - r[0][1]) / s,
        }
    } else if r[0][0] > r[1][1] && r[0][0] > r[2][2] {
        let s = (1.0 + r[0][0] - r[1][1] - r[2][2]).sqrt() * 2.0;
        Quaternion {
            w: (r[2][1] - r[1][2]) / s,
            x: 0.25 * s,
            y: (r[0][1] + r[1][0]) / s,
            z: (r[0][2] + r[2][0]) / s,
        }
    } else if r[1][1] > r[2][2] {
        let s = (1.0 + r[1][1] - r[0][0] - r[2][2]).sqrt() * 2.0;
        Quaternion {
            w: (r[0][2] - r[2][0]) / s,
            x: (r[0][1] + r[1][0]) / s,
            y: 0.25 * s,
            z: (r[1][2] + r[2][1]) / s,
        }
    } else {
        let s = (1.0 + r[2][2] - r[0][0] - r[1][1]).sqrt() * 2.0;
        Quaternion {
            w: (r[1][0] - r[0][1]) / s,
            x: (r[0][2] + r[2][0]) / s,
            y: (r[1][2] + r[2][1]) / s,
            z: 0.25 * s,
        }
    };
    q.normalized()
}

fn safe_div(s: f32) -> f32 {
    if s.abs() < 1e-12 { 0.0 } else { 1.0 / s }
}

impl Mul for Matrix4 {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        let mut out = [[0.0f32; 4]; 4];
        for (r, out_row) in out.iter_mut().enumerate() {
            for (c, out_cell) in out_row.iter_mut().enumerate() {
                *out_cell = self.m[r][0] * rhs.m[0][c]
                    + self.m[r][1] * rhs.m[1][c]
                    + self.m[r][2] * rhs.m[2][c]
                    + self.m[r][3] * rhs.m[3][c];
            }
        }
        Self { m: out }
    }
}
