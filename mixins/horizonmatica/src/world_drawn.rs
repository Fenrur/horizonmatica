fn horizonmatica_world_drawn(world: &mut WorldDrawn<'_>) {
    if let Some(draw) = mod_horizonmatica::draw_callback::<for<'a> fn(&mut WorldDrawn<'a>)>() {
        draw(world);
    }
}
