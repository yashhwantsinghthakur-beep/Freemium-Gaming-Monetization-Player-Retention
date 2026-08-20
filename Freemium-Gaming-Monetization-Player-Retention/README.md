# Freemium Gaming Monetization & Player Retention Analytics

A comprehensive Python data analytics pipeline for evaluating player retention, behavioral drop-offs, and monetization health in Free-to-Play (F2P) games.

## 📊 Project Overview

This project provides data-driven insights into player engagement and revenue optimization for F2P game studios. By analyzing player behavior, retention patterns, and in-app purchase trends, this pipeline enables actionable recommendations for improving both player experience and monetization strategy.

### Key Features

- **Player Retention Analysis**: Track cohort retention rates, churn prediction, and lifetime value (LTV)
- **Monetization Metrics**: Analyze ARPU, ARPPU, conversion funnels, and revenue distribution
- **Behavioral Analysis**: Identify drop-off points, engagement patterns, and player segmentation
- **Data Pipeline**: End-to-end data processing from raw CSVs to actionable insights
- **Reproducible Results**: Modular, well-documented code for consistent analysis

## 🎯 Use Cases

- **Player Retention Optimization**: Identify at-risk player segments before churn
- **Monetization Strategy**: Evaluate pricing, in-app purchase effectiveness, and pricing tiers
- **User Segmentation**: Classify players by behavior and spending patterns
- **Churn Prediction**: Proactive identification of players likely to leave
- **A/B Testing**: Data foundation for game design experiments

## 📁 Project Structure

```
Freemium-Gaming-Monetization-Player-Retention/
├── notebooks/                    # Jupyter Notebooks (analysis workflows)
│   ├── 01_data_exploration.ipynb
│   ├── 02_retention_analysis.ipynb
│   ├── 03_monetization_metrics.ipynb
│   ├── 04_player_segmentation.ipynb
│   └── 05_churn_prediction.ipynb
├── src/                          # Reusable Python modules
│   ├── __init__.py
│   ├── data_loader.py
│   ├── retention.py
│   ├── monetization.py
│   ├── player_analysis.py
│   └── utils.py
├── data/                         # Data files
│   ├── raw/                      # Original data
│   ├── processed/                # Cleaned data
│   └── external/                 # Reference data
├── outputs/                      # Generated results
│   ├── visualizations/           # Charts & plots
│   ├── reports/                  # Analysis reports
│   └── models/                   # Saved models
├── tests/                        # Unit & integration tests
├── docs/                         # Documentation
├── .gitignore
├── requirements.txt              # Python dependencies
├── README.md
└── LICENSE
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/razesoni/Freemium-Gaming-Monetization-Player-Retention.git
   cd Freemium-Gaming-Monetization-Player-Retention
   ```

2. **Create a virtual environment**:
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n f2p-analytics python=3.10
   conda activate f2p-analytics
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   jupyter notebook
   ```

## 📊 Dataset

### Input Data: `mobile_game_inapp_purchases.csv`

Expected columns:
- `player_id`: Unique player identifier
- `purchase_date`: Date of in-app purchase
- `purchase_amount`: Revenue amount (USD)
- `item_type`: Type of item purchased
- `install_date`: Player installation date
- `platform`: Android/iOS
- `country`: Player location
- `session_count`: Number of game sessions
- `session_length`: Average session duration (minutes)
- `genre`: Game genre/category

### Data Size
- Format: CSV
- Rows: Thousands to millions of player transactions
- Size: Scalable pipeline supporting large datasets
- Version: Updated August 2026

## 🔍 Analysis Workflows

### 1. Data Exploration (`01_data_exploration.ipynb`)
- Load and inspect raw data
- Identify missing values and outliers
- Generate descriptive statistics
- Visualize data distributions
- Detect anomalies and data quality issues

### 2. Retention Analysis (`02_retention_analysis.ipynb`)
- Calculate day-1, day-7, day-30 retention rates
- Build cohort retention tables
- Analyze retention trends over time
- Segment players by retention behavior
- Churn rate analysis

### 3. Monetization Metrics (`03_monetization_metrics.ipynb`)
- ARPU (Average Revenue Per User)
- ARPPU (Average Revenue Per Paying User)
- Conversion funnel analysis
- Revenue distribution by player segment
- LTV (Lifetime Value) estimation
- Platform & regional ARPU comparisons

### 4. Player Segmentation (`04_player_segmentation.ipynb`)
- Cluster players by spending/engagement (Whales, Dolphins, Minnows)
- Identify segment-specific behaviors
- Analyze segment demographics
- Develop targeting strategies
- Lifetime value predictions per segment

### 5. Churn Prediction (`05_churn_prediction.ipynb`)
- Build predictive models (Logistic Regression, Random Forest)
- Feature engineering for churn indicators
- Model evaluation and validation
- Identify high-risk player segments
- Generate churn risk scores

## 💻 Core Modules

### `src/data_loader.py`
Load and preprocess game data, handle missing values, and prepare datasets.

```python
from src.data_loader import load_game_data

df = load_game_data('data/raw/mobile_game_inapp_purchases.csv')
```

### `src/retention.py`
Calculate retention metrics and build cohort analyses.

```python
from src.retention import calculate_retention_cohort

retention_table = calculate_retention_cohort(df)
print(retention_table)
```

### `src/monetization.py`
Compute revenue metrics and analyze monetization health.

```python
from src.monetization import calculate_arpu, calculate_arppu

arpu = calculate_arpu(df)
arppu = calculate_arppu(df)
print(f"ARPU: ${arpu:.2f}, ARPPU: ${arppu:.2f}")
```

### `src/player_analysis.py`
Analyze player behavior and segment user bases.

```python
from src.player_analysis import segment_players

segments = segment_players(df)
print(segments.value_counts())
```

### `src/utils.py`
Helper functions for data processing and visualization.

## 🧪 Testing

Run the test suite to ensure code quality:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_retention.py

# Run with coverage
pytest --cov=src
```

## 📈 Example Usage

```python
import pandas as pd
from src.data_loader import load_game_data
from src.retention import calculate_retention_cohort
from src.monetization import calculate_arpu

# Load data
df = load_game_data('data/raw/mobile_game_inapp_purchases.csv')

# Calculate retention
retention_cohort = calculate_retention_cohort(df)
print("Retention Cohort Analysis:")
print(retention_cohort)

# Calculate ARPU
arpu = calculate_arpu(df)
print(f"\nAverage Revenue Per User: ${arpu:.2f}")

# Calculate ARPPU
arppu = calculate_arppu(df)
print(f"Average Revenue Per Paying User: ${arppu:.2f}")
```

## 📚 Documentation

- **[Methodology](docs/methodology.md)**: Detailed explanation of analysis approaches
- **[Data Dictionary](docs/data_dictionary.md)**: Column definitions and data specifications
- **[Contributing Guide](docs/contributing.md)**: Guidelines for contributing to the project

## 🔄 Workflow

1. **Data Preparation**: Run `01_data_exploration.ipynb` to load and inspect data
2. **Analysis**: Execute notebooks 02-05 for specific analyses
3. **Generate Reports**: Export visualizations and findings to `outputs/`
4. **Export Results**: Save processed data and models for production use
5. **Iteration**: Use insights to refine game mechanics and monetization

## 🛠️ Tech Stack

| Component | Tools |
|-----------|-------|
| **Data Processing** | pandas, NumPy |
| **Analysis** | scikit-learn, SciPy |
| **Visualization** | Matplotlib, Seaborn |
| **Notebooks** | Jupyter, JupyterLab |
| **Testing** | pytest |
| **Version Control** | Git/GitHub |
| **Environment** | Python 3.8+ |

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature description'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

See [CONTRIBUTING.md](docs/contributing.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Razesh Soni**  
📧 GitHub: [@razesoni](https://github.com/razesoni)

## 💬 Contact & Support

For questions, issues, or suggestions:
- Open an [Issue](https://github.com/razesoni/Freemium-Gaming-Monetization-Player-Retention/issues)
- Submit a [Pull Request](https://github.com/razesoni/Freemium-Gaming-Monetization-Player-Retention/pulls)
- Check existing documentation in `/docs`

## ⚠️ Known Limitations

- Requires CSV format input data
- Assumes transaction-level data granularity
- Scalability dependent on available memory
- Churn prediction requires historical data with 30+ days minimum
- Platform-specific features require standardized column names

## 🎮 Roadmap & Future Enhancements

- [ ] Add automated CI/CD pipeline (GitHub Actions)
- [ ] Dockerization for reproducible environments
- [ ] Interactive dashboard (Streamlit/Dash)
- [ ] Real-time data processing capabilities
- [ ] Machine learning model persistence (joblib/pickle)
- [ ] Expanded documentation with case studies
- [ ] API endpoint for model predictions
- [ ] Automated report generation

## 📈 Key Metrics Tracked

- **DAU/MAU**: Daily/Monthly Active Users
- **Retention Rates**: D1, D7, D30 cohort retention
- **ARPU**: Average Revenue Per User
- **ARPPU**: Average Revenue Per Paying User
- **LTV**: Lifetime Value
- **Conversion Rate**: F2P to Paying conversion
- **Churn Rate**: Player attrition metrics

---

**Last Updated**: August 2026  
**Status**: Active Development 🚀  
**Maintenance**: Actively maintained
