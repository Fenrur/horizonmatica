fn horizonmatica_screen_close(game: &mut crate::game::Game<'_>) -> std::ops::ControlFlow<()> {
    crate::game::horizonmatica_menus::hook_close(game)
}
