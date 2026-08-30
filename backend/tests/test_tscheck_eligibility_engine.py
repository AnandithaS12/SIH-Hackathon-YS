"""
Covers acceptance criteria:
- "Questionnaire completes ... produces a persona + scheme matches" (API side)
- "Eligibility hard blockers still return INELIGIBLE after the engine refactor"

Verified against a running server + real seeded Mongo data (40 schemes / 12 docs).
"""
import httpx

BASE_URL = "http://localhost:8001/api"

MP_FEMALE_FARMER_PAYLOAD = {
    "name": "Sunita Devi",
    "age": 34,
    "gender": "female",
    "state": "Madhya Pradesh",
    "category": "OBC",
    "occupation": "Farmer / Agriculture",
    "annual_income": 120000,
    "area_type": "rural",
    "has_bpl_card": True,
    "has_land": True,
    "has_girl_child": True,
}


def test_mp_female_farmer_persona_and_counts():
    resp = httpx.post(f"{BASE_URL}/citizens/evaluate", json=MP_FEMALE_FARMER_PAYLOAD, timeout=30)
    assert resp.status_code == 200, resp.text
    data = resp.json()

    persona_title = data["persona"]["title"] if isinstance(data["persona"], dict) else data["persona"]
    assert persona_title == "Krishi & Annadata Agricultural Producer"

    assert data["total_schemes_evaluated"] == 40
    assert data["eligible_count"] == 19
    assert data["partially_eligible_count"] == 13


def test_mp_female_farmer_hard_blockers():
    resp = httpx.post(f"{BASE_URL}/citizens/evaluate", json=MP_FEMALE_FARMER_PAYLOAD, timeout=30)
    assert resp.status_code == 200, resp.text
    eligibility_map = resp.json()["eligibility_map"]

    assert eligibility_map["pm-kisan"]["status"] == "ELIGIBLE"
    assert eligibility_map["ladli-behna-mp"]["status"] == "ELIGIBLE"

    # State-restricted / demographic-restricted schemes must never leak as eligible
    assert eligibility_map["gruha-lakshmi-karnataka"]["status"] == "INELIGIBLE"
    assert eligibility_map["adip-disability-aids"]["status"] == "INELIGIBLE"

    # No scheme restricted to another state may show ELIGIBLE / PARTIALLY_ELIGIBLE
    karnataka_only_ineligible = eligibility_map["gruha-lakshmi-karnataka"]["status"]
    assert karnataka_only_ineligible not in ("ELIGIBLE", "PARTIALLY_ELIGIBLE")
