from runner import make_file_name, source_hash

all_competitors = [
    "David_AI_v9",
    "David_AI_v8",
    "David_AI_v7",
    "David_AI_v6",
    "David_AI_v5",
    "David_AI_v4",
    "David_AI_v3",
    "David_AI_v2",
    "David_AI_v1",
    "Iain_AI_v2",
    "Iain_AI_v1",
    "Michael_AI_v1_3",
    "Michael_AI_v1_2",
    "Michael_AI_v1_1",
    "Michael_AI_v1_0",
    "Robert_AI",
    "no_search",
    "random_AI",
    "no_move_AI",
    # 'Human_player'
]

bad_competitors = [
    "Robert_AI",
    "no_search",
    "random_AI",
]

competitorNames = bad_competitors
competitorNames = all_competitors

for name in competitorNames:
    exec("import " + name)

competitors = [eval(name) for name in competitorNames]
for player in competitors:
    player.matchesPlayed_ = 0
    player.tournamentScore_ = 0
    player.totalMoves_ = 0
    player.totalTime_ = 0

tournamentResults = [("white", "black", "result", "moves", "time", "explanation")]
white_wins = 0
black_wins = 0
draws = 0
for repeat in range(1, 50):
    for white in competitors:
        for black in competitors:
            if white == black:
                continue
            file_name = (
                rf"results/{white.__name__} vs {black.__name__} repeat {repeat}.txt"
            )
            try:
                file = open(make_file_name(white, black, repeat))
                previous_versions = file.readline()
                current_versions = (
                    f"{source_hash(white)} vs {source_hash(black)} repeat {repeat}\n"
                )
                if current_versions != previous_versions:
                    continue
            except (FileNotFoundError, SyntaxError):
                continue
            result = eval(file.readline())
            score = result["score"]
            if score == 1:
                white_wins += 1
            elif score == 0:
                black_wins += 1
            else:
                draws += 1
            white.matchesPlayed_ += 1
            white.tournamentScore_ += score
            white.totalMoves_ += result["white_moves"]
            white.totalTime_ += result["white_time_taken"]
            black.matchesPlayed_ += 1
            black.tournamentScore_ += 1 - score
            black.totalMoves_ += result["black_moves"]
            black.totalTime_ += result["black_time_taken"]
            tournamentResults.append(
                (
                    white.__name__,
                    black.__name__,
                    score,
                    result["black_moves"] + result["white_moves"],
                    "{:.3f}".format(
                        result["black_time_taken"] + result["white_time_taken"]
                    ),
                    result["cause"],
                )
            )


print("\n------------------------ tournament results ------------------------")
print(
    f"The tournament has taken {sum(c.totalTime_ for c in competitors):.1f} seconds so far"
)
print("All the matches played in the tournament so far are shown below")
for result in tournamentResults:
    print("".join("{:<16}".format(r) for r in result), sep="\t")
print("\nThe total scores are:")
for player in competitors:
    if player.matchesPlayed_:
        player.percentage_score_ = 100 * player.tournamentScore_ / player.matchesPlayed_
    else:
        player.percentage_score_ = 0
competitors.sort(key=lambda c: c.percentage_score_, reverse=True)
for player in competitors:
    if player.matchesPlayed_ == 0:
        continue
    print(
        f"{player.__name__: <16}"
        f"scored {player.percentage_score_:.1f}% "
        f"{player.tournamentScore_}/{player.matchesPlayed_} "
        # f'with {player.totalMoves_} moves, '
        f"taking on average {player.totalTime_ / player.totalMoves_:.3f} seconds"
    )

print(
    f"\nThere were {white_wins} white wins, {black_wins} black wins and {draws} draws"
)
