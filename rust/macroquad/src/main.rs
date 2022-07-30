extern crate macroquad;

// use macroquad::prelude::load_ttf_font;
use macroquad::prelude::rand::gen_range;
use macroquad::prelude::*;

use std::time::Instant;

struct Laby {
    size_x: usize,
    size_y: usize,
    real_x: usize,
    real_y: usize,
    real_z: usize,
    arr: Vec<usize>,
    dirs: Vec<isize>,
}

impl Laby {
    pub fn new(size_x: usize, size_y: usize) -> Self {
        let real_x = size_x + 2;
        let real_y = size_y + 2;
        let dirs: Vec<isize> = vec![real_x as isize, 1, -(real_x as isize), -1];
        let mut li = Self {
            size_x,
            size_y,
            real_x,
            real_y,
            real_z: 2_usize,
            arr: vec![0; real_x * real_y],
            dirs,
        };
        for x in 1..li.size_x + 1 {
            for y in 1..li.size_y + 1 {
                li.arr[x + y * li.real_x] = 1;
            }
        }
        return li;
    }
}

struct PaintLabyLine<'a> {
    li: &'a Laby,
    block_size: f32,
    half_line_width: f32,
    border_h: f32,
    border_w: f32
}

impl<'a> PaintLabyLine<'a>{
    fn new(border: f32, line_rel_size: f32, li: &'a Laby) -> Self {
        let size_x: f32 = ((li.size_x as f32) - 1.0) * 0.5;
        let size_y: f32 = ((li.size_y as f32) - 1.0) * 0.5;
        let block_size_w = ((screen_width() - 2.0 * border) / size_x).floor();
        let block_size_h = ((screen_height() - 2.0 * border) / size_y).floor();
        let block_size: f32;
        if block_size_w < block_size_h {
            block_size = block_size_w;
        } else {
            block_size = block_size_h;
        }
        let border_h = (screen_height() - block_size * (size_y as f32)) * 0.5;
        let border_w = (screen_width() - block_size * (size_x as f32)) * 0.5;
        let mut half_line_width: f32 = (block_size * line_rel_size * 0.5).round();
        if half_line_width == 0.0 {
            half_line_width = 0.5;
        }
        Self {
            li,
            block_size,
            half_line_width,
            border_h,
            border_w
        }
    }

    fn x_pos(&self, x: usize) -> f32 {
        (x - 1) as f32 * 0.5 * self.block_size + self.border_w
    }

    fn y_pos(&self, y: usize) -> f32 {
        (y - 1) as f32 * 0.5 * self.block_size + self.border_h
    }

    pub fn paint_line_li(&self) {
        clear_background(WHITE);
        if self.li.size_x * self.li.size_y <= 331 * 201 {
            self.paint_bridge_shadow();
            self.paint_base();
        } else {
            let score_text = &format!(
                "Labyrinth {} * {} is too big to display",
                self.li.size_x, self.li.size_y
            );
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
        }
    }

    fn paint_bridge_shadow(&self) {
        let rel_width = 0.6;
        let width = self.block_size * rel_width;
        let rel_lo = (1.0 - rel_width) * 0.5;
        let rel_high = 1.0 - rel_lo;
        let lo = self.block_size * rel_lo;
        let high = self.block_size * rel_high;
        for x in (1..self.li.size_x).step_by(2) {
            for y in (1..self.li.size_y).step_by(2) {
                let cur_pos = (x + 1) + (y + 1) * self.li.real_x + self.li.real_x * self.li.real_y;
                if self.li.arr[cur_pos] == 0 {
                    if self.li.arr[cur_pos + self.li.real_x] == 0 && self.li.arr[cur_pos - self.li.real_x] == 0 {
                        draw_rectangle(
                            self.x_pos(x) + lo,
                            self.y_pos(y) - lo,
                            width,
                            2.0 * lo + self.block_size,
                            LIGHTGRAY,
                        );
                    } else {
                        draw_rectangle(
                            self.x_pos(x) - lo,
                            self.y_pos(y) + lo,
                            2.0 * lo + self.block_size,
                            width,
                            LIGHTGRAY,
                        );
                    }
                }
            }
        }
    }

    fn paint_base(&self) {
        for x in (1..self.li.size_x + 1).step_by(2) {
            for y in (1..self.li.size_y + 1).step_by(2) {
                let cur_pos = x + y * self.li.real_x;
                let x_pos = self.x_pos(x) - self.half_line_width;
                let y_pos = self.y_pos(y) - self.half_line_width;
                if self.li.arr[cur_pos + 1] == 1 {
                    draw_rectangle(
                        x_pos,
                        y_pos,
                        2.0 * self.half_line_width + self.block_size,
                        2.0 * self.half_line_width,
                        BLACK,
                    );
                }
                if self.li.arr[cur_pos + self.li.real_x] == 1 {
                    draw_rectangle(
                        x_pos,
                        y_pos,
                        2.0 * self.half_line_width,
                        2.0 * self.half_line_width + self.block_size,
                        BLACK,
                    );
                }
            }
        }
    }
}

#[rustfmt::skip]
fn test_laby_v() -> Laby {
    let mut li = Laby::new(7_usize, 7_usize);
    li.arr = vec![
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 1, 1, 1, 1, 1, 0,
        0, 1, 0, 1, 0, 0, 0, 1, 0,
        0, 1, 0, 1, 1, 1, 0, 1, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0,
        0, 1, 1, 1, 1, 1, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ];
    li
}

#[rustfmt::skip]
fn test_laby_h() -> Laby {
    let mut li = Laby::new(7_usize, 7_usize);
    li.arr = vec![
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 1, 1, 1, 1, 1, 0,
        0, 1, 0, 0, 0, 1, 0, 1, 0,
        0, 1, 1, 1, 0, 1, 0, 1, 0,
        0, 1, 0, 1, 0, 1, 0, 1, 0,
        0, 1, 0, 1, 0, 1, 0, 1, 0,
        0, 1, 0, 0, 0, 1, 0, 1, 0,
        0, 1, 1, 1, 1, 1, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 0, 0, 0, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ];
    li
}

fn generate(size_x: usize, size_y: usize) -> Laby {
    let mut li: Laby = Laby::new(size_x, size_y);
    rand::srand(macroquad::miniquad::date::now() as _);
    let mut jump_pos = Vec::<usize>::new();
    let mut pos: usize = 2 * li.real_x + 2;
    li.arr[pos] = 0;
    let mut avai_dir = Vec::<isize>::new();

    loop {
        loop {
            avai_dir.clear();
            for d in &li.dirs {
                let test_pos: usize = ((pos as isize) + d * 2) as usize;
                if li.arr[test_pos] == 1 {
                    avai_dir.push(*d);
                }
            }

            if avai_dir.len() == 0 {
                break;
            } else if avai_dir.len() > 1 {
                jump_pos.push(pos);
            }
            let r = gen_range::<usize>(0, avai_dir.len());
            let dir = avai_dir[r];
            for _ in 0..2 {
                pos = ((pos as isize) + dir) as usize;
                li.arr[pos] = 0;
            }
        }
        if jump_pos.len() == 0 {
            break;
        }
        let r: usize = gen_range::<usize>(0, jump_pos.len());
        pos = jump_pos.swap_remove(r);
    }
    li.arr[li.real_x + 2] = 0;
    li.arr[li.real_x * li.size_y + (li.real_x - 3)] = 0;
    li
}

fn paint_block_li(li: &Laby) {
    let border = 10_f32;
    // let pad = 3_f32;
    let pad = 0_f32;
    let border_h: f32;
    let border_w: f32;
    let block_size_w = ((screen_width() - border) / (li.real_x as f32)).floor();
    let block_size_h = ((screen_height() - border) / (li.real_y as f32)).floor();
    let block_size: f32;
    if block_size_w < block_size_h {
        block_size = block_size_w;
    } else {
        block_size = block_size_h;
    }
    border_h = (screen_height() - block_size * (li.real_y as f32)) * 0.5;
    border_w = (screen_width() - block_size * (li.real_x as f32)) * 0.5;

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
        let score_text = &format!(
            "Labyrinth {} * {} is too big to display",
            li.size_x, li.size_y
        );
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
    }
}

#[macroquad::main("Laby")]
async fn main() {
    // from: https://www.dafont.com/computerfont.font
    // let font = load_ttf_font("res/Computerfont.ttf")
    //     .await
    //     .expect("Font loaded");
    let start = Instant::now();
    println!("Start");
    // let li = generate(9_usize, 9_usize);
    // let li = generate(51_usize, 31_usize);
    // let li = generate(77_usize, 31_usize);
    // let li = generate(331_usize, 201_usize);
    // let li = generate(77711_usize, 711_usize);
    let li = test_laby_v();
    // let li = test_laby_h();
    let duration = start.elapsed();
    println!("Time elapsed to generate labrinth is: {:?}", duration);

    loop {
        let pll = PaintLabyLine::new(30.0, 0.1, &li);
        if is_key_down(KeyCode::Escape) {
            break;
        }
        // paint_block_li(&li);
        pll.paint_line_li();
        next_frame().await
    }
}
