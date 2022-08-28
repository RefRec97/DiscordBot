import interactions

compare_options = [
    interactions.Option(
        name="comparator",
        description="1 = Gesamtpunkte, 2 = Flotte, 3 = Forschung, Gebaeude = 4, Verteidigung = 5",
        type=interactions.OptionType.INTEGER,
        required=True,
        choices=[
            interactions.Choice(name="Gesamtpunkte", value=1), 
            interactions.Choice(name="Flotte", value=2),
            interactions.Choice(name="Forschung", value=3), 
            interactions.Choice(name="Gebaeude", value=4),
            interactions.Choice(name="Verteidigung", value=5),
        ],
    ),
    interactions.Option(
        name="player_1",
        description="Name des ersten Spielers",
        type=interactions.OptionType.STRING,
        required=True,
    ),
    interactions.Option(
        name="player_2",
        description="Name des zweiten Spielers",
        type=interactions.OptionType.STRING,
        required=True,
    ),
    interactions.Option(
        name="player_3",
        description="Name des dritten Spielers",
        type=interactions.OptionType.STRING,
        required=False,
    ),
    interactions.Option(
        name="player_4",
        description="Name des vierten Spielers",
        type=interactions.OptionType.STRING,
        required=False,
    ),
    interactions.Option(
        name="player_5",
        description="Name des fuenften Spielers",
        type=interactions.OptionType.STRING,
        required=False,
    ),
    interactions.Option(
        name="size",
        description="size of chart, default m",
        type=interactions.OptionType.STRING,
        required=False,
        choices=[
            interactions.Choice(name="s", value="s"), 
            interactions.Choice(name="m", value="m"),
            interactions.Choice(name="l", value="l"), 
            interactions.Choice(name="xl", value="xl"),
        ],
    ),
]