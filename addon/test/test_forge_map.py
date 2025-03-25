from ..src.madeleine.forge_level_reader import get_forge_map

maps: list[tuple[str, str]] = [
    ("cd87b6a4-3283-4187-a5b3-b3d4cd8446d6", "a306f8e7-cb92-4907-a80e-3fe72b76df63"),
    ("3dde0705-5b09-4a6f-a7d9-36e0cd1ebf0f", "8c1536df-b8b2-4872-b81c-a557b9041bba"),
    ("48c924c8-d471-4fd7-9121-163f511fcb29", "0928f751-0df7-4cee-93d5-a9c4ff338d0c"),
    ("b535e5fd-ca99-4252-9946-18067be43ed3", "66514427-a281-4d46-a928-cf1d2793b83b"),
    ("2182e9f8-7555-4955-874d-1afa6053ea62", "db8399b3-27b6-452e-b969-10ed26e7e99f"),
    ("89f3b8ad-6bbf-4652-8d67-8e5330294de4", "ee7540aa-e504-4372-8e04-3e583a3359aa"),
    ("d035fc3e-f298-4c14-9487-465be2e1dc1f", "8d5eb886-a41d-4093-827e-2cbdc75c651e"),
    ("f1cc3b4e-471c-4ec5-b855-1db7d9e6ce42", "cc6dfb16-7782-4995-a74a-98e86051fcdf"),
    ("e4bb06db-065f-4902-b93b-d8dac315eac4", "e23fe351-1729-4dd6-ba3b-b42d30e48244"),
    ("e8268e75-6583-42ad-9e0c-2d2f043f5f0f", "470ca4cf-b6f2-4d1e-ba3d-dc4d136f7764"),
]


def test_forge_map() -> None:
    for asset, version in maps:
        objects, categories = get_forge_map(asset, version, "")
        assert objects != []
        assert categories != []
        for object in objects:
            assert object.global_id != -1
