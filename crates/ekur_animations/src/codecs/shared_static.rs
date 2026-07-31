use ekur_definitions::animations::AnimationGraph;
use ekur_definitions::animations::AnimationTagResourceMember;
use ekur_definitions::animations::CodecType;

use crate::Codec;
use crate::Quaternion;
use crate::Vector3;

#[derive(Debug, Default)]
pub struct SharedStaticPool {
    pub rotations: Vec<Quaternion>,
    pub translations: Vec<Vector3>,
    pub scales: Vec<f32>,
}

pub fn build_shared_static_pool(animation_graph: &AnimationGraph) -> SharedStaticPool {
    let mut pool = SharedStaticPool::default();
    for q in &animation_graph.rotations.elements {
        pool.rotations
            .push(Quaternion::from_quantized_xyzw(q).normalized());
    }
    for p in &animation_graph.positions.elements {
        pool.translations.push(Vector3::from_shared(p));
    }
    for s in &animation_graph.scales.elements {
        pool.scales.push(s.scale.0);
    }
    pool
}

pub fn decode_shared_static(
    buffer: &[u8],
    tag_data: &AnimationTagResourceMember,
    pool: &SharedStaticPool,
) -> Option<Codec> {
    let cps = tag_data.animation_data_sizes.compressed_static_pose.0 as usize;
    if cps == 0 || cps > buffer.len() {
        return None;
    }

    let s = &buffer[buffer.len() - cps..];
    if s.len() < 32 || s[0] != CodecType::SharedStatic as u8 {
        return None;
    }
    let (n_rot, n_trn, n_scl) = (s[1] as usize, s[2] as usize, s[3] as usize);
    let trn_off = u32::from_le_bytes(s.get(12..16)?.try_into().ok()?) as usize;
    let scl_off = u32::from_le_bytes(s.get(16..20)?.try_into().ok()?) as usize;
    let index =
        |o: usize| -> Option<i16> { s.get(o..o + 2).map(|b| i16::from_le_bytes([b[0], b[1]])) };
    let mut rotations = Vec::with_capacity(n_rot);
    for k in 0..n_rot {
        let idx = index(32 + 2 * k)?;
        let q = (idx >= 0)
            .then(|| pool.rotations.get(idx as usize).copied())
            .flatten();
        rotations.push(vec![q.unwrap_or(Quaternion::IDENTITY)]);
    }
    let mut translations = Vec::with_capacity(n_trn);
    for k in 0..n_trn {
        let idx = index(trn_off + 2 * k)?;
        let t = (idx >= 0)
            .then(|| pool.translations.get(idx as usize).copied())
            .flatten();
        translations.push(vec![t.unwrap_or_default()]);
    }
    let mut scales = Vec::with_capacity(n_scl);
    for k in 0..n_scl {
        let idx = index(scl_off + 2 * k)?;
        let v = (idx >= 0)
            .then(|| pool.scales.get(idx as usize).copied())
            .flatten();
        scales.push(vec![v.unwrap_or(1.0)]);
    }
    Some(Codec {
        rotations,
        translations,
        scales,
    })
}
