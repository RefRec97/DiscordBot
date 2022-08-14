import interactions

phalanx_map_options = [
    interactions.Option(
        name="galaxy",
        description="Galaxie die betrachtet werden soll",
        type=interactions.OptionType.INTEGER,
        required=True,
    ),
    interactions.Option(
        name="start_system",
        description="Startsystem der Map",
        type=interactions.OptionType.INTEGER,
        required=True,
    ),
    interactions.Option(
        name="end_system",
        description="Endsystem der Map",
        type=interactions.OptionType.INTEGER,
        required=True,
    ),
]

