import structures.Timber.timber as timber


class TestTimberCompression:

    def test_comp(self):
        col = timber.Column(
            length=3700,
            breadth=90,
            depth=90,
            grade="F17",
            category=2,
            seasoned=True,
            latitude=False,
        )
        col._compression(moisture_content=15, g13=1, la=3700)
