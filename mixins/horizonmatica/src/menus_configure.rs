fn horizonmatica_configure(game: &mut crate::game::Game<'_>, index: usize) {
    crate::game::horizonmatica_menus::open_from_mods(game, index);
}
