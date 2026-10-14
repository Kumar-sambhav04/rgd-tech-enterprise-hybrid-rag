from app.authorization.access_control import(apply_ac,UserRole)


test_results = [
    {
        "id": "chunk-1",
        "rank": 1,
        "metadata": {
            "access_level": "support"
        }
    },
    {
        "id": "chunk-2",
        "rank": 2,
        "metadata": {
            "access_level": "admin"
        }
    },
    {
        "id": "chunk-3",
        "rank": 3,
        "metadata": {
            "access_level": "support"
        }
    }
]


support_results = apply_ac(
    test_results,
    UserRole.SUPPORT
)

print(support_results)