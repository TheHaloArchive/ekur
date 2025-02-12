/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
pub(super) fn get_resource_data(
    offset: usize,
    length: usize,
    resource_buffers: &[Vec<u8>],
) -> Vec<u8> {
    let mut output = vec![0u8; length];
    let mut resource_index = 0;
    let mut resource_position = 0;
    let mut output_position = 0;

    while output_position < length && resource_index < resource_buffers.len() {
        let resource_buffer = &resource_buffers[resource_index];

        if offset >= resource_position + resource_buffer.len() {
            resource_position += resource_buffer.len();
            resource_index += 1;
            continue;
        }

        let mut offset_in_block = 0;
        if offset > resource_position {
            offset_in_block += offset - resource_position;
            resource_position += offset_in_block;
        }

        let bytes_to_copy = (length - output_position).min(resource_buffer.len() - offset_in_block);
        output[output_position..output_position + bytes_to_copy]
            .copy_from_slice(&resource_buffer[offset_in_block..offset_in_block + bytes_to_copy]);

        output_position += bytes_to_copy;
        resource_position += bytes_to_copy;
        resource_index += 1;
    }

    output
}
