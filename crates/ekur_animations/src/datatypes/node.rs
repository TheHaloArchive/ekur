#[derive(Default, Debug)]
pub struct Node {
    pub name: String,
    pub parent_node: i16,
    pub first_child_node: i16,
    pub next_subling_node: i16,
    pub translation: (f32, f32, f32),
    pub rotation: (f32, f32, f32, f32),
    pub scale: f32,
}
