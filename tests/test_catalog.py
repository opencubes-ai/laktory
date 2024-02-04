from laktory.models import Catalog
from laktory._testing.stackvalidator import StackValidator


def test_model():
    cat = Catalog(
        name="lakehouse",
    )

    assert cat.name == "lakehouse"
    assert cat.full_name == "lakehouse"


def test_deploy():
    cat = Catalog(
        name="dev",
        grants=[
            {"principal": "account users", "privileges": ["USE_CATALOG", "USE_SCHEMA"]}
        ],
        schemas=[
            {
                "name": "engineering",
                "grants": [
                    {"principal": "domain-engineering", "privileges": ["SELECT"]}
                ],
            },
            {
                "name": "sources",
                "volumes": [
                    {
                        "name": "landing",
                        "volume_type": "EXTERNAL",
                        "grants": [
                            {
                                "principal": "account users",
                                "privileges": ["READ_VOLUME"],
                            },
                            {
                                "principal": "role-metastore-admins",
                                "privileges": ["WRITE_VOLUME"],
                            },
                        ],
                    },
                ],
            },
        ],
    )
    validator = StackValidator({"catalogs": [cat]})
    validator.validate()


if __name__ == "__main__":
    test_model()
    test_deploy()
