from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SUPPORT = "support"


def apply_ac(results: list[dict],role:UserRole)->list[dict]:
    if role == UserRole.ADMIN:
        filtered_results = results

    elif role == UserRole.SUPPORT:
        filtered_results = [result for result in results
                 if result["metadata"].get("access_level") == "support"]

    else:
       raise ValueError(f"Unsupported user role : {role}")

    for rank, result in enumerate(filtered_results,start=1):
        result["rank"] = rank

    return filtered_results
    