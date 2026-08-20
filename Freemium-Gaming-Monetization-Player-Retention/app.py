import io
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify, Response
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_raw_data, clean_game_data, filter_gaming_dataset
from src.monetization import segment_revenue_contribution, genre_monetization_depth
from src.player_analysis import calculate_correlation_matrix
from src.llm_insights import generate_llm_insights

app = Flask(__name__)

try:
    RAW_DF = load_raw_data()
    PAYING_DF, F2P_DF = clean_game_data(RAW_DF)
    BASE_DF = pd.concat([PAYING_DF, F2P_DF], ignore_index=True)
except Exception as e:
    print(f"Dataset load error: {e}")
    BASE_DF = pd.DataFrame(columns=[
        "UserID", "Age", "Gender", "Country", "Device", "GameGenre",
        "SessionCount", "AverageSessionLength", "SpendingSegment",
        "InAppPurchaseAmount", "FirstPurchaseDaysAfterInstall",
        "PaymentMethod", "LastPurchaseDate"
    ])

def style_plotly_chart(fig, height=390):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB", family="Inter, system-ui, sans-serif", size=12),
        margin=dict(l=45, r=25, t=50, b=45),
        height=height,
        hoverlabel=dict(bgcolor="#111827", font_color="#F9FAFB"),
        legend=dict(
            font=dict(color="#E5E7EB"),
            bgcolor="rgba(17,24,39,.65)",
            bordercolor="rgba(255,255,255,.10)",
            borderwidth=1
        )
    )
    fig.update_xaxes(
        tickfont=dict(color="#A7B0C0"),
        title_font=dict(color="#DDE3EE"),
        showgrid=True,
        gridcolor="rgba(255,255,255,.07)",
        zeroline=False
    )
    fig.update_yaxes(
        tickfont=dict(color="#A7B0C0"),
        title_font=dict(color="#DDE3EE"),
        showgrid=True,
        gridcolor="rgba(255,255,255,.07)",
        zeroline=False
    )
    return fig

def fig_json(fig):
    return json.loads(style_plotly_chart(fig).to_json())

def safe_num(v):
    return float(v) if pd.notna(v) else 0.0

def generate_insights(df: pd.DataFrame, paying: pd.DataFrame) -> list:
    if df.empty:
        return ["No player data matches the current filter criteria."]

    insights = []
    total_users = df["UserID"].nunique()
    paying_users = paying["UserID"].nunique() if not paying.empty else 0
    total_rev = safe_num(paying["InAppPurchaseAmount"].sum()) if not paying.empty else 0.0

    if not paying.empty and total_rev > 0:
        # Whale Concentration Insight
        whales = paying[paying["SpendingSegment"] == "Whale"]
        if not whales.empty:
            whale_rev = whales["InAppPurchaseAmount"].sum()
            whale_rev_pct = (whale_rev / total_rev) * 100
            whale_user_pct = (whales["UserID"].nunique() / paying_users) * 100
            insights.append(
                f"<strong>Whale Concentration:</strong> Whales make up <strong>{whale_user_pct:.1f}%</strong> of paying users but contribute <strong>{whale_rev_pct:.1f}%</strong> (${whale_rev:,.2f}) of gross revenue."
            )

        # Top Performing Genre
        genre_summary = paying.groupby("GameGenre")["InAppPurchaseAmount"].sum()
        if not genre_summary.empty:
            top_genre = genre_summary.idxmax()
            top_genre_rev = genre_summary.max()
            top_genre_pct = (top_genre_rev / total_rev) * 100
            insights.append(
                f"<strong>Top Monetizing Genre:</strong> <strong>{top_genre}</strong> is the highest revenue driver, generating <strong>{top_genre_pct:.1f}%</strong> (${top_genre_rev:,.2f}) of total revenue."
            )

        # Top Monetizing Device (ARPPU)
        device_rev = paying.groupby("Device").agg(Revenue=("InAppPurchaseAmount", "sum"), Users=("UserID", "nunique"))
        device_rev["ARPPU"] = device_rev["Revenue"] / device_rev["Users"]
        if not device_rev.empty:
            top_device = device_rev["ARPPU"].idxmax()
            insights.append(
                f"<strong>Platform Value Leader:</strong> <strong>{top_device}</strong> leads monetization depth with an ARPPU of <strong>${device_rev.loc[top_device, 'ARPPU']:,.2f}</strong>."
            )

        # Time to Conversion Latency
        if "FirstPurchaseDaysAfterInstall" in paying.columns:
            median_latency = paying["FirstPurchaseDaysAfterInstall"].dropna()
            median_latency = median_latency[median_latency >= 0].median()
            if pd.notna(median_latency):
                insights.append(
                    f"<strong>Conversion Window:</strong> The median time from install to first purchase is <strong>{median_latency:.1f} days</strong>."
                )
    else:
        insights.append("<strong>Zero Paying Users:</strong> The selected player cohort consists exclusively of non-paying players (0% conversion).")

    return insights

def generate_analytics_payload(df: pd.DataFrame):
    paying = df[df["InAppPurchaseAmount"].fillna(0) > 0].copy()
    f2p = df[df["InAppPurchaseAmount"].fillna(0) <= 0].copy()

    total_rev = safe_num(paying["InAppPurchaseAmount"].sum()) if not paying.empty else 0
    paying_users = paying["UserID"].nunique() if not paying.empty else 0
    f2p_users = f2p["UserID"].nunique() if not f2p.empty else 0
    total_users = df["UserID"].nunique() if not df.empty else 0
    arppu = total_rev / paying_users if paying_users else 0
    conversion_rate = paying_users / total_users * 100 if total_users else 0
    avg_sessions = safe_num(paying["SessionCount"].mean()) if not paying.empty else 0
    avg_session_length = safe_num(paying["AverageSessionLength"].mean()) if not paying.empty else 0

    kpis = {
        "total_revenue": f"${total_rev:,.2f}",
        "paying_users": f"{paying_users:,}",
        "f2p_users": f"{f2p_users:,}",
        "arppu": f"${arppu:,.2f}",
        "total_users": f"{total_users:,}",
        "conversion_rate": f"{conversion_rate:.1f}%",
        "avg_sessions": f"{avg_sessions:.1f}",
        "avg_session_length": f"{avg_session_length:.1f}"
    }

    charts = {}

    # 1. Revenue concentration
    if not paying.empty:
        seg_summary = segment_revenue_contribution(paying)
        if not seg_summary.empty:
            charts["fig_pareto"] = fig_json(px.pie(
                seg_summary, values="TotalRevenue", names="SpendingSegment",
                hole=.50, title="Revenue concentration by spending segment"
            ))

        # 2. Revenue by genre
        genre_rev = (
            paying.groupby("GameGenre", as_index=False)["InAppPurchaseAmount"]
            .sum().sort_values("InAppPurchaseAmount", ascending=True)
        )
        if not genre_rev.empty:
            charts["fig_genre_rev"] = fig_json(px.bar(
                genre_rev, x="InAppPurchaseAmount", y="GameGenre", orientation="h",
                title="Gross revenue by game genre"
            ))

        # 3. Genre × segment monetization depth
        depth = genre_monetization_depth(paying)
        if not depth.empty:
            cols = [c for c in ["Whale", "Dolphin", "Minnow"] if c in depth.columns]
            if cols:
                charts["fig_depth"] = fig_json(px.bar(
                    depth, x="GameGenre", y=cols, barmode="group",
                    title="Average spend by genre and spending segment"
                ))

        # 4. Correlation heatmap
        corr = calculate_correlation_matrix(paying)
        if not corr.empty:
            charts["fig_corr"] = fig_json(px.imshow(
                corr, text_auto=".2f", aspect="auto",
                title="Numerical feature correlation"
            ))

        # 5. Session count vs purchase amount
        charts["fig_scatter"] = fig_json(px.scatter(
            paying, x="SessionCount", y="InAppPurchaseAmount",
            color="SpendingSegment",
            hover_data=[c for c in ["Age", "GameGenre", "Device"] if c in paying.columns],
            title="Session count vs in-app purchase amount"
        ))

        # 6. Session length by segment
        charts["fig_session_box"] = fig_json(px.box(
            paying, x="SpendingSegment", y="AverageSessionLength",
            color="SpendingSegment", points=False,
            title="Average session length across spending tiers"
        ))

        # 7. Device ARPU
        device_df = paying.groupby("Device").agg(
            Revenue=("InAppPurchaseAmount", "sum"),
            Users=("UserID", "nunique")
        ).reset_index()
        device_df["ARPU"] = device_df["Revenue"] / device_df["Users"].replace(0, pd.NA)
        charts["fig_device"] = fig_json(px.bar(
            device_df.sort_values("ARPU", ascending=False),
            x="Device", y="ARPU", text_auto=".2f",
            title="ARPU by device platform"
        ))

        # 8. Country player volume
        country_df = df["Country"].value_counts().head(10).reset_index()
        country_df.columns = ["Country", "Players"]
        charts["fig_country"] = fig_json(px.bar(
            country_df.sort_values("Players"),
            x="Players", y="Country", orientation="h",
            title="Top countries by player volume"
        ))

        # 9. Conversion latency
        if "FirstPurchaseDaysAfterInstall" in paying.columns:
            latency = paying["FirstPurchaseDaysAfterInstall"].dropna()
            latency = latency[latency >= 0]
            if not latency.empty:
                charts["fig_latency"] = fig_json(px.histogram(
                    latency, nbins=30,
                    title="Time to first purchase"
                ))

        # 10. Revenue by spending segment
        seg_rev = paying.groupby("SpendingSegment", as_index=False)["InAppPurchaseAmount"].sum()
        charts["fig_segment_revenue"] = fig_json(px.bar(
            seg_rev.sort_values("InAppPurchaseAmount", ascending=False),
            x="SpendingSegment", y="InAppPurchaseAmount", text_auto=".2f",
            title="Total revenue by spending segment"
        ))

        # 11. Average revenue by country
        country_arpu = (
            paying.groupby("Country", as_index=False)["InAppPurchaseAmount"]
            .mean().rename(columns={"InAppPurchaseAmount": "AverageRevenue"})
            .sort_values("AverageRevenue", ascending=False).head(10)
        )
        if not country_arpu.empty:
            charts["fig_country_arpu"] = fig_json(px.bar(
                country_arpu.sort_values("AverageRevenue"),
                x="AverageRevenue", y="Country", orientation="h",
                title="Top countries by average revenue per paying player"
            ))

        # 12. Genre × gender average spend
        if "Gender" in paying.columns:
            gg = (
                paying.groupby(["GameGenre", "Gender"], as_index=False)["InAppPurchaseAmount"]
                .mean().rename(columns={"InAppPurchaseAmount": "AverageSpend"})
            )
            if not gg.empty:
                charts["fig_gender_genre"] = fig_json(px.bar(
                    gg, x="AverageSpend", y="GameGenre", color="Gender",
                    barmode="group", orientation="h",
                    title="Average spend by genre and gender"
                ))

        # 13. Device total revenue
        device_rev = (
            paying.groupby("Device", as_index=False)["InAppPurchaseAmount"]
            .sum().rename(columns={"InAppPurchaseAmount": "Revenue"})
        )
        charts["fig_device_revenue"] = fig_json(px.bar(
            device_rev.sort_values("Revenue", ascending=False),
            x="Device", y="Revenue", text_auto=".2f",
            title="Total in-app purchase revenue by device"
        ))

        # 14. Age distribution of paying users
        if "Age" in paying.columns:
            charts["fig_age"] = fig_json(px.histogram(
                paying, x="Age", nbins=20,
                title="Age distribution of paying players"
            ))

        # 15. Engagement profile by segment
        engagement = paying.groupby("SpendingSegment", as_index=False).agg(
            AvgSessions=("SessionCount", "mean"),
            AvgSessionLength=("AverageSessionLength", "mean")
        )
        charts["fig_engagement"] = fig_json(px.bar(
            engagement, x="SpendingSegment",
            y=["AvgSessions", "AvgSessionLength"], barmode="group",
            title="Engagement profile by spending segment"
        ))

    cols = [c for c in [
        "UserID", "Age", "Gender", "Country", "Device", "GameGenre",
        "SessionCount", "AverageSessionLength", "SpendingSegment",
        "InAppPurchaseAmount", "FirstPurchaseDaysAfterInstall", "PaymentMethod"
    ] if c in df.columns]

    table_data = df[cols].head(100).to_dict(orient="records")

    return {
        "kpis": kpis,
        "charts": charts,
        "insights": generate_insights(df, paying),
        "table_cols": cols,
        "table_data": table_data,
        "row_count": len(df),
        "empty": df.empty
    }

@app.route("/")
def index():
    genres = sorted(BASE_DF["GameGenre"].dropna().unique())
    segments = ["Whale", "Dolphin", "Minnow"]
    devices = sorted(BASE_DF["Device"].dropna().unique())
    countries = sorted(BASE_DF["Country"].dropna().unique())
    return render_template("index.html", genres=genres, segments=segments,
                           devices=devices, countries=countries)

@app.route("/api/filter", methods=["POST"])
def api_filter():
    data = request.get_json() or {}
    filtered_df = filter_gaming_dataset(
        BASE_DF,
        genres=data.get("genres"),
        segments=data.get("segments"),
        devices=data.get("devices"),
        countries=data.get("countries")
    )
    return jsonify(generate_analytics_payload(filtered_df))

@app.route("/api/download-csv", methods=["POST"])
def download_csv():
    data = request.get_json() or {}
    filtered_df = filter_gaming_dataset(
        BASE_DF,
        genres=data.get("genres"),
        segments=data.get("segments"),
        devices=data.get("devices"),
        countries=data.get("countries")
    )
    output = io.StringIO()
    filtered_df.to_csv(output, index=False)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=freemium_game_analytics.csv"}
    )

@app.route("/api/ai-insights", methods=["POST"])
def api_ai_insights():
    data = request.get_json() or {}
    
    # Filter dataset based on current sidebar selections
    filtered_df = filter_gaming_dataset(
        BASE_DF,
        genres=data.get("genres"),
        segments=data.get("segments"),
        devices=data.get("devices"),
        countries=data.get("countries")
    )
    
    analytics = generate_analytics_payload(filtered_df)
    
    llm_summary = generate_llm_insights(
        kpis=analytics["kpis"],
        filter_summary=data
    )
    
    return jsonify({"ai_summary": llm_summary})

if __name__ == "__main__":
    app.run(debug=True, port=5000)