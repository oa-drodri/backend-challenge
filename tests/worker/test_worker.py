import pytest
from worker import count_zero_passes
from models.ecg import ExecutionData, Lead


def process_lead_data(data):
    leads_data = data.get("leads", [])
    leads = []

    for lead_data in leads_data:
        name = lead_data.get("name")
        signal = lead_data.get("signal", [])

        lead = Lead(name=name, signal=signal)
        leads.append(lead)

    return leads


@pytest.mark.parametrize(
    "leads, expected_count",
    [
        ({"leads": [
            {"name": "Lead1", "signal": [-1, -2, -3, 1, 2, 3]},
            {"name": "Lead2", "signal": [4, -5, -6, 7, -8, 9]},
        ]}, 5),
        ({"leads": [
            {"name": "Lead1", "signal": [1, 2, -3, -4, 5, -6]},
            {"name": "Lead2", "signal": [-7, 8, -9, -10, 11, 12]},
        ]}, 6),
        ({"leads": [
            {"name": "Lead1", "signal": [0, 0, 0]},
            {"name": "Lead2", "signal": [0, 0, 0]},
        ]}, 0),
        ({"leads": [
            {"name": "Lead1", "signal": [-1, -2, -3]},
            {"name": "Lead2", "signal": [-4, -5, -6]},
        ]}, 0),
        ({"leads": [
            {"name": "Lead1", "signal": [1, 2, 3]},
            {"name": "Lead2", "signal": [4, 5, 6]},
        ]}, 0),
    ]
)
def test_count_zero_passes(leads, expected_count, mock_collection):
    execution_data = ExecutionData(
        date="2000/01/01",
        leads=process_lead_data(leads)
    )
    assert count_zero_passes(execution_data) == expected_count
