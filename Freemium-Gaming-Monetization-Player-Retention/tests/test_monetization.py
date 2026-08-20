from src.data_loader import clean_game_data
from src.monetization import calculate_arpu, segment_revenue_contribution

def test_arpu_and_segmentation(sample_player_data):
    paying_df, _ = clean_game_data(sample_player_data)
    arpu = calculate_arpu(paying_df)
    assert arpu == (4500.0 + 10.0 + 250.0) / 3
    
    seg_contrib = segment_revenue_contribution(paying_df)
    assert "RevenueSharePct" in seg_contrib.columns
    assert round(seg_contrib["RevenueSharePct"].sum(), 2) == 100.0