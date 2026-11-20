fn horizonmatica_wheel(game: &mut crate::game::Game<'_>, scroll: [f64; 2], canceled: &mut bool) {
    if !*canceled {
        crate::game::horizonmatica::wheel(game, scroll[1] as f32, canceled);
    }
}
