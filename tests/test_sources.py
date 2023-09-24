from laktory.models.datasources import EventDataSource


def test_source_event():
    reader = EventDataSource(
        name="stock_price",
        producer={"name": "yahoo_finance"},
    )
    assert reader.dirpath == "/mnt/landing/events/yahoo_finance/stock_price/"


if __name__ == "__main__":
    test_source_event()
