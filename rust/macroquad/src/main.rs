extern crate macroquad;
extern crate bitvec;

use macroquad::prelude::*;
use macroquad::prelude::load_ttf_font;

use bitvec::prelude::*;
use bitvec::vec::BitVec;

struct Laby {
    size_x: usize,
    size_y: usize,
    real_x: usize,
    real_y: usize,
    real_z: usize,
    arr: BitVec<usize, Lsb0>
}

impl Laby {
    pub fn new(size_x: usize, size_y: usize) -> Self {
        let real_x = size_x + 2;
        let real_y = size_y + 2;
        Self {
            size_x,
            size_y,
            real_x,
            real_y,
            real_z: 2_usize,
            arr: BitVec::repeat(true, real_x * real_y)
        }
    }
}

#[macroquad::main("Laby")]
async fn main() {
    // from: https://www.dafont.com/computerfont.font
    let _font = load_ttf_font("res/Computerfont.ttf")
        .await
        .expect("Font loaded");
    let mut li = Laby::new(5_usize, 5_usize);
    li.arr.set(0, false);

    loop {
        if is_key_down(KeyCode::Escape) {
            break;
        }
        let border = 30_f32;
        let pad = 3_f32;
        let border_h: f32;
        let border_w: f32;
        let block_size_w = (screen_width() - border) / (li.real_x as f32);
        let block_size_h = (screen_height() - border) / (li.real_y as f32);
        let block_size: f32;
        if block_size_w < block_size_h {
            block_size = block_size_w;
            border_w = border * 0.5;
            border_h = (screen_height() - block_size * (li.real_y as f32)) * 0.5;
        } else {
            block_size = block_size_h;
            border_w = (screen_width() - block_size * (li.real_x as f32)) * 0.5;
            border_h = border * 0.5;
        }

        clear_background(WHITE);

        for x in 0..li.real_x {
            for y in 0..li.real_y {
                if li.arr[x + y * li.real_x] == true {
                    draw_rectangle(
                        border_w + (x as f32) * block_size + pad,
                        border_h + (y as f32) * block_size + pad,
                        block_size - pad,
                        block_size - pad,
                        BLACK,
                    );
                }
            }
        }

        // let score_text = &format!("Hello world!");
        // let score_text_dim = measure_text(&score_text, Some(font), 60, 1.0);
        // draw_text_ex(
        //     &score_text,
        //     (screen_width() - score_text_dim.width) * 0.5,
        //     40.0,
        //     TextParams {
        //         font,
        //         font_size: 60,
        //         color: BLACK,
        //         ..Default::default()
        //     },
        // );
        next_frame().await
    }
}
