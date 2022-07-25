extern crate macroquad;

use macroquad::prelude::*;
use macroquad::prelude::load_ttf_font;
use macroquad::prelude::rand::gen_range;

use std::time::Instant;

struct Laby {
    size_x: usize,
    size_y: usize,
    real_x: usize,
    real_y: usize,
    real_z: usize,
    arr: Vec<usize>,
    dirs: Vec<isize>
}

impl Laby {
    pub fn new(size_x: usize, size_y: usize) -> Self {
        let real_x = size_x + 2;
        let real_y = size_y + 2;
        let dirs:Vec<isize> = vec![real_x as isize, 1, - (real_x as isize), -1];
        let mut li = Self {
            size_x,
            size_y,
            real_x,
            real_y,
            real_z: 2_usize,
            arr: vec![0; real_x * real_y],
            dirs
        };
        for x in 1..li.size_x + 1 {
            for y in 1..li.size_y + 1 {
                li.arr[x + y * li.real_x] = 1;
            }
        }
        return li;
    }
}

#[macroquad::main("Laby")]
async fn main() {
    // from: https://www.dafont.com/computerfont.font
    let font = load_ttf_font("res/Computerfont.ttf")
        .await
        .expect("Font loaded");
    rand::srand(macroquad::miniquad::date::now() as _);
    println!("Start");
    let start = Instant::now();
    // let mut li = Laby::new(9_usize, 9_usize);
    // let mut li = Laby::new(51_usize, 31_usize);
    // let mut li = Laby::new(77_usize, 31_usize);
    let mut li = Laby::new(331_usize, 201_usize);
    // let mut li = Laby::new(77711_usize, 711_usize);
    let mut jump_pos = Vec::<usize>::new();
    let mut pos: usize = 2 * li.real_x + 2;
    li.arr[pos] = 0;

    loop {
        loop {
            let mut avai_dir = Vec::<isize>::new();
            for d in &li.dirs {
                let test_pos: usize = ((pos as isize) + d * 2) as usize;
                if li.arr[test_pos] == 1 {
                    avai_dir.push(*d);
                }
            }
            if avai_dir.len() > 0 {
                let r = gen_range::<usize>(0, avai_dir.len());
                let dir = avai_dir[r];
                if avai_dir.len() > 1 {
                    jump_pos.push(pos);
                }
                for _ in 0..2 {
                    pos = ((pos as isize) + dir) as usize;
                    li.arr[pos] = 0;
                }
            } else {
                break;
            }
        }
        if jump_pos.len() == 0 {
            break
        }
        let r:usize = gen_range::<usize>(0, jump_pos.len());
        pos = jump_pos.swap_remove(r);
    }
    li.arr[li.real_x + 2] = 0;
    li.arr[li.real_x * li.size_y + (li.real_x -3)] = 0;
    let duration = start.elapsed();
    println!("Time elapsed to generate labrinth is: {:?}", duration);

    loop {
        if is_key_down(KeyCode::Escape) {
            break;
        }
        let border = 30_f32;
        // let pad = 3_f32;
        let pad = 0_f32;
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
        if li.size_x * li.size_y <= 331 * 201 {
            for x in 0..li.real_x {
                for y in 0..li.real_y {
                    if li.arr[x + y * li.real_x] == 1 {
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
        } else {
            let score_text = &format!("Labyrinth {} * {} is too big to display", li.size_x, li.size_y);
            let score_text_dim = measure_text(&score_text, Some(font), 60, 1.0);
            draw_text_ex(
                &score_text,
                (screen_width() - score_text_dim.width) * 0.5,
                40.0,
                TextParams {
                    font,
                    font_size: 60,
                    color: BLACK,
                    ..Default::default()
                },
            );
        }

        next_frame().await
    }
}
