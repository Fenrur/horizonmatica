// Preserve the pinned Nightly's command tree, then add Horizonmatica's completions.
fn horizonmatica_chat_tree(
    game: &mut crate::game::Game<'_>,
    base: Option<&horizon_client::command::Dispatcher>,
) -> horizon_client::command::Dispatcher {
    let base = match base {
        Some(tree) => tree,
        None => horizon_client::command::vanilla::game_dispatcher(),
    };
    let mut commands = Vec::new();
    game.native_register_client_commands(&mut commands);
    commands.retain(|command| {
        let keep = command.level == 0;
        if !keep {
            log::warn!(
                "Horizon: a client command was left out: `{}` has an operator level",
                command.usage
            );
        }
        keep
    });
    let arguments = super::native_server::command_arguments();
    let (tree, _, problems) = super::native_server::command_tree(
        &commands,
        |name| base.find(name).is_some(),
        &arguments,
    );
    for problem in problems {
        log::warn!("Horizon: a client command was left out: {problem}");
    }
    let mut tree_with_mods = base.clone();
    super::native_server::register_dispatcher(
        &mut tree_with_mods,
        &tree,
        horizon_client::command::MOD_COMMAND,
        &arguments,
    );
    if game.on(crate::game::horizonmatica::ID) {
        crate::game::horizonmatica::chat_tree(&mut tree_with_mods);
    }
    with_studio_commands(&with_native_commands(&tree_with_mods, &["studio"])).with_profiler()
}
