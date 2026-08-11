use ekur_definitions::animations::MovementDataType;

use crate::datatypes::quaternion::Quaternion;

#[derive(Debug, Clone, Copy)]
pub struct MovementFrame {
    pub dx: f32,
    pub dy: f32,
    pub dz: f32,
    pub rotation: Quaternion,
}

impl Default for MovementFrame {
    fn default() -> Self {
        Self {
            dx: 0.0,
            dy: 0.0,
            dz: 0.0,
            rotation: Quaternion::IDENTITY,
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct MovementData {
    pub kind: MovementDataType,
    pub frames: Vec<MovementFrame>,
}

/// Bytes-per-frame for each movement kind, on disk.
fn movement_bytes_per_frame(kind: MovementDataType) -> usize {
    match kind {
        MovementDataType::None => 0,
        MovementDataType::DxDy => 8,
        MovementDataType::DxDyDyaw => 12,
        MovementDataType::DxDyDzDyaw => 16,
        MovementDataType::DxDyDzDangleAxis => 24,
        MovementDataType::XYZAbsolute => 12,
        MovementDataType::Auto => 0,
    }
}

fn f32_at(data: &[u8], off: usize) -> f32 {
    f32::from_le_bytes(data[off..off + 4].try_into().unwrap())
}

pub fn read_movement_at(
    data: &[u8],
    offset: usize,
    size: usize,
    kind: MovementDataType,
    frame_count: usize,
) -> MovementData {
    if kind == MovementDataType::None || size == 0 {
        return MovementData::default();
    }
    let bpf = movement_bytes_per_frame(kind);
    if bpf == 0 || !size.is_multiple_of(bpf) {
        return MovementData::default();
    }
    if offset.checked_add(size).is_none_or(|end| end > data.len()) {
        return MovementData::default();
    }
    let read_count = (size / bpf).min(frame_count.max(1));
    let mut frames = Vec::with_capacity(read_count);
    for i in 0..read_count {
        let off = offset + i * bpf;
        let frame = match kind {
            MovementDataType::DxDy => MovementFrame {
                dx: f32_at(data, off),
                dy: f32_at(data, off + 4),
                ..Default::default()
            },
            MovementDataType::DxDyDyaw => MovementFrame {
                dx: f32_at(data, off),
                dy: f32_at(data, off + 4),
                dz: 0.0,
                rotation: Quaternion::from_yaw(f32_at(data, off + 8)),
            },
            MovementDataType::DxDyDzDyaw => MovementFrame {
                dx: f32_at(data, off),
                dy: f32_at(data, off + 4),
                dz: f32_at(data, off + 8),
                rotation: Quaternion::from_yaw(f32_at(data, off + 12)),
            },
            MovementDataType::DxDyDzDangleAxis => MovementFrame {
                dx: f32_at(data, off),
                dy: f32_at(data, off + 4),
                dz: f32_at(data, off + 8),
                rotation: Quaternion::from_angle_axis(
                    f32_at(data, off + 12),
                    f32_at(data, off + 16),
                    f32_at(data, off + 20),
                ),
            },
            MovementDataType::XYZAbsolute => MovementFrame {
                dx: f32_at(data, off),
                dy: f32_at(data, off + 4),
                dz: f32_at(data, off + 8),
                ..Default::default()
            },
            MovementDataType::None | MovementDataType::Auto => MovementFrame::default(),
        };
        frames.push(frame);
    }
    MovementData { kind, frames }
}
