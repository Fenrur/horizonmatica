// The info box and the material list.
fn horizonmatica_hud(
    game: &crate::game::Game<'_>,
    batch: &mut horizon_client::hud::HudBatch,
    corners: &mut mod_api::Corners,
) {
    crate::game::horizonmatica::hud(game, batch, corners);
}
