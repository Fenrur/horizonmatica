fn horizonmatica_key(game: &mut crate::game::Game<'_>, key: &str, action: mod_api::KeyAction) {
    crate::game::horizonmatica::key(game, key, action == mod_api::KeyAction::Press);
}
