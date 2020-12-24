import score

def test_snake_hits():
    assert score.score == 0
    score.score += 2
    assert score.score == 2
    score.score -= 1
    assert score.score == 1

