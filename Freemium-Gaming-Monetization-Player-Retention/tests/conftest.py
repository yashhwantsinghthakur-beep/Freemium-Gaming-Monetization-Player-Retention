import pytest
import pandas as pd

@pytest.fixture
def sample_player_data():
    return pd.DataFrame({
        "UserID": ["u1", "u2", "u3", "u4"],
        "Age": [24.0, 31.0, None, 19.0],
        "Gender": ["Male", "Female", None, "Male"],
        "Country": ["USA", "India", "UK", "Canada"],
        "Device": ["Android", "iOS", "Android", "iOS"],
        "GameGenre": ["Adventure", "Casual", "MOBA", "Adventure"],
        "SessionCount": [10, 5, 12, 8],
        "AverageSessionLength": [22.5, 14.2, 30.1, 18.0],
        "SpendingSegment": ["Whale", "Minnow", "Dolphin", "Minnow"],
        "InAppPurchaseAmount": [4500.0, 10.0, 250.0, None],
        "FirstPurchaseDaysAfterInstall": [5.0, 20.0, 8.0, None],
        "PaymentMethod": ["Credit Card", "Paypal", "Google Pay", None],
        "LastPurchaseDate": ["2025-05-01", "2025-04-10", "2025-06-11", None]
    })