use std::any::Any;
use std::sync::OnceLock;

pub use horizonmatica_core as core;
pub use horizonmatica_menus as menus;
use mod_api::Hooks;

static DRAW: OnceLock<Box<dyn Any + Send + Sync>> = OnceLock::new();

// Both patch libraries use the same SDK types. Keep the callback type-checked
// without depending on the engine's unstable rendering crate in the mod crate.
pub fn register_draw<T: Any + Send + Sync>(draw: T) {
    let _ = DRAW.set(Box::new(draw));
}

pub fn draw_callback<T: Any>() -> Option<&'static T> {
    DRAW.get()?.downcast_ref()
}

#[derive(Default)]
struct Horizonmatica;

#[mod_api::horizon_mod]
impl Hooks for Horizonmatica {}
