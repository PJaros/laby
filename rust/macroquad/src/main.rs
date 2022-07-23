use macroquad::prelude::*;

#[macroquad::main("Laby")]
async fn main() {
    // from: https://www.dafont.com/computerfont.font
    let font = load_ttf_font("res/Computerfont.ttf")
        .await
        .expect("Font loaded");
    let (size_x, size_y) = (5_i32, 5_i32);

    loop {
        if is_key_down(KeyCode::Escape) {
            break;
        }
        let border = 30_f32;
        let pad = 3_f32;
        let border_h: f32;
        let border_w: f32;
        let block_size_w = (screen_width() - border) / (size_x as f32);
        let block_size_h = (screen_height() - border) / (size_y as f32);
        let block_size: f32;
        if block_size_w < block_size_h {
            block_size = block_size_w;
            border_w = border * 0.5;
            border_h = (screen_height() - block_size * (size_y as f32)) * 0.5;
        } else {
            block_size = block_size_h;
            border_w = (screen_width() - block_size * (size_x as f32)) * 0.5;
            border_h = border * 0.5;
        }

        clear_background(WHITE);

        for x in 0..size_x {
            for y in 0..size_y {
                draw_rectangle(
                    border_w + (x as f32) * block_size + pad,
                    border_h + (y as f32) * block_size + pad,
                    block_size - pad,
                    block_size - pad,
                    BLACK,
                );
            }
        }

        let score_text = &format!("Hello world!");
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
        next_frame().await
    }
}
