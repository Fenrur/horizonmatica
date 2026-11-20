fn horizonmatica_render_needs(needs: &mut RenderNeeds) {
    if mod_horizonmatica::draw_callback::<for<'a> fn(&mut WorldDrawn<'a>)>().is_some() {
        needs.world_depth = true;
    }
}
