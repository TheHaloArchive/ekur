use ekur_definitions::animations::{AnimationType, MovementDataType};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum JmaKind {
    Jmm,
    Jma,
    Jmt,
    Jmz,
    Jmo,
    Jmr,
}

impl JmaKind {
    pub fn from_metadata(animation_type: AnimationType, frame_info_type: MovementDataType) -> Self {
        match animation_type {
            AnimationType::Overlay => return Self::Jmo,
            AnimationType::Replacement => return Self::Jmr,
            _ => {}
        }
        match frame_info_type {
            MovementDataType::DxDy => Self::Jma,
            MovementDataType::DxDyDyaw => Self::Jmt,
            MovementDataType::DxDyDzDyaw
            | MovementDataType::DxDyDzDangleAxis
            | MovementDataType::XYZAbsolute => Self::Jmz,
            MovementDataType::None | MovementDataType::Auto => Self::Jmm,
        }
    }

    pub fn folds_movement(self) -> bool {
        matches!(self, Self::Jma | Self::Jmt | Self::Jmz)
    }

    pub fn prepends_rest_pose(self) -> bool {
        matches!(self, Self::Jmo | Self::Jmr)
    }

    pub fn appends_held_frame(self) -> bool {
        matches!(self, Self::Jmm | Self::Jma | Self::Jmt | Self::Jmz)
    }
}
