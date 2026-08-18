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
    if s.len() < 48 || s[0] != CodecType::SharedStatic as u8 {
        return None;
    }
    let (n_rot, n_scl, n_trn) = (s[2] as usize, s[4] as usize, s[6] as usize);
    let trn_off = 48 + n_rot * 2;
    let scl_off = trn_off + n_trn * 2;
    let index =
        |o: usize| -> Option<u16> { s.get(o..o + 2).map(|b| u16::from_le_bytes([b[0], b[1]])) };
    let mut rotations = Vec::with_capacity(n_rot);
    for k in 0..n_rot {
        let idx = index(48 + 2 * k)?;
        let q = (idx != u16::MAX)
            .then(|| pool.rotations.get(idx as usize).copied())
            .flatten();
        rotations.push(q.map(|v| vec![v]).unwrap_or_default());
    }
    let mut translations = Vec::with_capacity(n_trn);
    for k in 0..n_trn {
        let idx = index(trn_off + 2 * k)?;
        let t = (idx != u16::MAX)
            .then(|| pool.translations.get(idx as usize).copied())
            .flatten();
        translations.push(t.map(|v| vec![v]).unwrap_or_default());
    }
    let mut scales = Vec::with_capacity(n_scl);
    for k in 0..n_scl {
        let idx = index(scl_off + 2 * k)?;
        let v = (idx != u16::MAX)
            .then(|| pool.scales.get(idx as usize).copied())
            .flatten();
        scales.push(v.map(|x| vec![x]).unwrap_or_default());
    }
    Some(Codec {
        rotations,
        translations,
        scales,
    })
}
