extern crate macroquad;

// use macroquad::prelude::load_ttf_font;
use macroquad::prelude::*;
use macroquad::rand::gen_range;

use std::f32::consts::PI;
use std::time::Instant;

#[derive(Debug)]
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
        let real_z = 2;
        let dirs: Vec<isize> = vec![real_x as isize, 1, -(real_x as isize), -1];
        let mut li = Self {
            size_x,
            size_y,
            real_x,
            real_y,
            real_z: 2_usize,
            arr: vec![0; real_x * real_y * real_z],
            dirs,
        };
        for x in 1..li.size_x + 1 {
            for y in 1..li.size_y + 1 {
                for z in 0..li.real_z {
                    li.arr[x + y * li.real_x + z * real_x * real_y] = 1;
                }
            }
        }
        return li;
    }
}

#[derive(Debug, Clone, Copy)]
struct PaintLabyLine<'a> {
    li: &'a Laby,
    block_size: f32,
    half_line_width: f32,
    border_h: f32,
    border_w: f32,
    bridge_width: f32,
    bridge_length: f32,
    bridge_top: f32,
    lo: f32,
    texture_bridge_v: Texture2D,
    texture_bridge_h: Texture2D,
}

impl<'a> PaintLabyLine<'a> {
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
        let border_h = ((screen_height() - block_size * (size_y as f32)) * 0.5).round();
        let border_w = ((screen_width() - block_size * (size_x as f32)) * 0.5).round();
        let mut half_line_width: f32 = (block_size * line_rel_size * 0.5).round();
        if half_line_width == 0.0 {
            half_line_width = 0.5;
        }
        let rel_bridge_width = 0.6;
        let rel_bridge_top = 0.25;
        let rel_bridge_line_width = 0.5;
        let mut line_width = (half_line_width * 2.0 * rel_bridge_line_width).round();
        if line_width <= 0.0 {
            line_width = 1.0;
        }
        let bridge_width = (block_size * rel_bridge_width).round();
        let image_breath_top = (bridge_width * (1.0 + rel_bridge_top)).ceil();
        let rel_lo = (1.0 - rel_bridge_width) * 0.5;
        let lo = (block_size * rel_lo).round();
        let bridge_length = 2.0 * lo + block_size;
        let bridge_top = image_breath_top - bridge_width;

        let mut transparant = WHITE;
        transparant.a = 0.0;
        let mut image_bridge_v =
            Image::gen_image_color(image_breath_top as u16, bridge_length as u16, transparant);
        let mut image_bridge_h =
            Image::gen_image_color(bridge_length as u16, image_breath_top as u16, transparant);
        let texture_bridge_v = Texture2D::from_image(&image_bridge_v);
        let texture_bridge_h = Texture2D::from_image(&image_bridge_h);
        for i in 0..(bridge_length as u32) {
            let i_over_pi = (PI / (bridge_length as f32)) * (i as f32);
            let begin_bridge = ((i_over_pi).sin() * bridge_width * rel_bridge_top).floor();
            for n in 0..(image_breath_top as u32) {
                let n_f32 = n as f32;
                let n_h = (image_breath_top as u32) - n - 1;
                if n_f32 < begin_bridge {
                } else if n_f32 >= begin_bridge && n_f32 < (begin_bridge + line_width) {
                    image_bridge_v.set_pixel(n, i, BLACK);
                    image_bridge_h.set_pixel(i, n_h, BLACK);
                } else if n_f32 <= begin_bridge + bridge_width - line_width {
                    image_bridge_v.set_pixel(n, i, WHITE);
                    image_bridge_h.set_pixel(i, n_h, WHITE);
                } else if n_f32 <= begin_bridge + bridge_width {
                    image_bridge_v.set_pixel(n, i, BLACK);
                    image_bridge_h.set_pixel(i, n_h, BLACK);
                }
            }
        }
        texture_bridge_v.update(&image_bridge_v);
        texture_bridge_h.update(&image_bridge_h);
        Self {
            li,
            block_size,
            half_line_width,
            border_h,
            border_w,
            bridge_width,
            bridge_length,
            bridge_top,
            lo,
            texture_bridge_v,
            texture_bridge_h,
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
            self.paint_bridge();
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
        for x in (1..self.li.size_x).step_by(2) {
            for y in (1..self.li.size_y).step_by(2) {
                let cur_pos = (x + 1) + (y + 1) * self.li.real_x + self.li.real_x * self.li.real_y;
                if self.li.arr[cur_pos] == 0 {
                    if self.li.arr[cur_pos + self.li.real_x] == 0
                        && self.li.arr[cur_pos - self.li.real_x] == 0
                    {
                        draw_rectangle(
                            self.x_pos(x) + self.lo,
                            self.y_pos(y) - self.lo,
                            self.bridge_width,
                            self.bridge_length,
                            LIGHTGRAY,
                        );
                    } else {
                        draw_rectangle(
                            self.x_pos(x) - self.lo,
                            self.y_pos(y) + self.lo,
                            self.bridge_length,
                            self.bridge_width,
                            LIGHTGRAY,
                        );
                    }
                }
            }
        }
    }

    fn paint_bridge(&self) {
        for x in (1..self.li.size_x).step_by(2) {
            for y in (1..self.li.size_y).step_by(2) {
                let cur_pos = (x + 1) + (y + 1) * self.li.real_x + self.li.real_x * self.li.real_y;
                if self.li.arr[cur_pos] == 0 {
                    if self.li.arr[cur_pos + self.li.real_x] == 0
                        && self.li.arr[cur_pos - self.li.real_x] == 0
                    {
                        draw_texture(
                            self.texture_bridge_v,
                            self.x_pos(x) + self.lo,
                            self.y_pos(y) - self.lo,
                            WHITE,
                        );
                    } else {
                        draw_texture(
                            self.texture_bridge_h,
                            self.x_pos(x) - self.lo,
                            self.y_pos(y) + self.lo - self.bridge_top,
                            WHITE,
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
fn _test_laby_v() -> Laby {
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
fn _test_laby_h() -> Laby {
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
    let mut avai_dir = Vec::<isize>::with_capacity(4);
    let mut avai_bridge_dir = Vec::<isize>::with_capacity(4);

    loop {
        loop {
            avai_dir.clear();
            avai_bridge_dir.clear();
            // let test_pos = pos;
            // println!("cur pos: {}, x: {}, y: {}", test_pos, test_pos % li.real_x, test_pos / li.real_x);
            for d in &li.dirs {
                if li.arr[(((pos as isize) + d * 2) as usize)] == 1 {
                    avai_dir.push(*d);
                }
            }
            for d in &li.dirs {
                let test_pos =
                    (((pos as isize) + d * 2 + (li.real_x * li.real_y) as isize) as usize);
                // println!("test_pos: {}, x: {}, y: {}", test_pos, test_pos % li.real_x, test_pos / li.real_x);
                if li.arr[test_pos] == 1
                    && li.arr[((pos as isize) + d * 4) as usize] == 1
                    && li.arr[((pos as isize) + d) as usize] == 1
                    && li.arr[((pos as isize) + d * 2) as usize] == 0
                {
                    avai_bridge_dir.push(*d);
                }
            }

            if avai_dir.len() > 0 {
                if avai_dir.len() > 1 {
                    jump_pos.push(pos);
                }
                let r = gen_range::<usize>(0, avai_dir.len());
                let dir = avai_dir[r];
                for _ in 0..2 {
                    pos = ((pos as isize) + dir) as usize;
                    li.arr[pos] = 0;
                }
                // let test_pos = pos;
                // println!("pos after dig: {}, x: {}, y: {}", test_pos, test_pos % li.real_x, test_pos / li.real_x);
            // } else if avai_bridge_dir.len() > 0 && gen_range::<usize>(0, 2) == 0 {
            } else if avai_bridge_dir.len() > 0 {
                let r = gen_range::<usize>(0, avai_bridge_dir.len());
                let dir = avai_bridge_dir[r];
                let mut b_pos: usize = pos + li.real_x * li.real_y;
                pos = ((pos as isize) + 4 * dir) as usize;
                for _ in 0..3 {
                    b_pos = ((b_pos as isize) + dir) as usize;
                    li.arr[b_pos] = 0;
                }
                li.arr[pos] = 0;
                // _print_li(&li);
                // let test_pos = pos;
                // println!("pos after bridge dig: {}, x: {}, y: {}", test_pos, test_pos % li.real_x, test_pos / li.real_x);
            } else {
                break;
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

fn _print_li(li: &Laby) {
    for i in 0..li.arr.len() / li.real_x {
        let mut line_output = String::new();
        for n in 0..li.real_x {
            line_output.push(match li.arr[i * li.real_x + n] {
                0 => '.',
                _ => '#',
            });
        }
        println!("{}", line_output);
    }
}

fn paint_block_li(li: &Laby) {
    let border = 2_f32;
    let pad = 3_f32;
    // let pad = 0_f32;
    let border_h: f32;
    let border_w: f32;
    let block_size_w = ((screen_width() - border) / (li.real_x as f32)).floor();
    let block_size_h = ((screen_height() - border) / ((li.real_y * li.real_z) as f32)).floor();
    let block_size: f32;
    if block_size_w < block_size_h {
        block_size = block_size_w;
    } else {
        block_size = block_size_h;
    }
    border_h = (screen_height() - block_size * ((li.real_y * li.real_z) as f32)) * 0.5;
    border_w = (screen_width() - block_size * (li.real_x as f32)) * 0.5;

    clear_background(WHITE);
    if li.size_x * li.size_y <= 331 * 201 {
        for x in (0..li.real_x).rev() {
            for y in 0..(li.real_y * li.real_z) {
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
    let mut show_line = true;
    println!("Start");
    // let li = generate(9_usize, 9_usize);
    // let li = generate(51_usize, 31_usize);
    let li = generate(77_usize, 31_usize);
    // let li = generate(331_usize, 201_usize);
    // let li = generate(77711_usize, 711_usize);
    // let li = _test_laby_v();
    // let li = _test_laby_h();
    let duration = start.elapsed();
    println!("Time elapsed to generate labrinth is: {:?}", duration);
    // let mut once: bool = false;
    loop {
        let pll = PaintLabyLine::new(30.0, 0.1, &li);
        // if !once {
        //     let mut pll_dbg = pll.clone();
        //     let dummy_li = Laby::new(1, 1);
        //     pll_dbg.li = &dummy_li;
        //     dbg!(pll_dbg);
        //     once = true;
        // }
        if is_key_down(KeyCode::Escape) {
            break;
        }
        if is_key_pressed(KeyCode::Space) {
            show_line = ! show_line;
        }

        if show_line {
            pll.paint_line_li();
        } else {
            paint_block_li(&li);
        }
        next_frame().await
    }
}
