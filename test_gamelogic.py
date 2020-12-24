import elements

def test_snake_hits():
    assert elements.score == 0
    elements.score += 2
    assert elements.score == 2
    elements.score -= 1
    assert elements.score == 1

