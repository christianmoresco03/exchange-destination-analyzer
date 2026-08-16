import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Exchange Destination Analyzer",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv(
    "destinations.csv",
    sep=";",
    skiprows=4
)

df = df[
    [
        "University",
        "City",
        "Country",
        "Academic_Ranking",
        "Employer_Reputation_Raw",
        "Cost_of_Living_Raw",
        "Safety_Raw",
        "City_Attractiveness_Raw"
    ]
].copy()

# Make sure numeric columns are numeric
numeric_columns = [
    "Academic_Ranking",
    "Employer_Reputation_Raw",
    "Cost_of_Living_Raw",
    "Safety_Raw",
    "City_Attractiveness_Raw"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# ---------------------------------------------------
# NORMALIZATION
# ---------------------------------------------------

def normalize_positive(series):
    """
    Higher raw values are better.
    Best observation in the dataset = 100.
    Worst observation in the dataset = 0.
    """
    return (
        (series - series.min())
        / (series.max() - series.min())
        * 100
    )


def normalize_negative(series):
    """
    Lower raw values are better.
    Best observation in the dataset = 100.
    Worst observation in the dataset = 0.
    """
    return (
        (series.max() - series)
        / (series.max() - series.min())
        * 100
    )


# Lower academic ranking position = better
df["Academic_Score"] = normalize_negative(
    df["Academic_Ranking"]
)

# Higher Employer Reputation = better
df["Employer_Score"] = normalize_positive(
    df["Employer_Reputation_Raw"]
)

# Lower Cost of Living = better
df["Cost_Score"] = normalize_negative(
    df["Cost_of_Living_Raw"]
)

# Higher Safety = better
df["Safety_Score"] = normalize_positive(
    df["Safety_Raw"]
)

# Higher City Attractiveness = better
df["Attractiveness_Score"] = normalize_positive(
    df["City_Attractiveness_Raw"]
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🌍 Exchange Analyzer")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Build Your Ranking",
        "Compare Destinations",
        "Explore Data",
        "Methodology"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Data-driven decision support for "
    "international exchange selection."
)

# ---------------------------------------------------
# OVERVIEW
# ---------------------------------------------------

if page == "Overview":

    st.title("🌍 Exchange Destination Analyzer")

    st.subheader(
        "Data-driven decision support for "
        "international exchange selection"
    )

    st.write(
        """
        The Exchange Destination Analyzer was developed to support a real
        international exchange decision using academic, professional,
        financial and lifestyle data.

        The full exchange network includes a significantly larger number of
        partner universities. This project focuses on an initial curated sample
        of 28 destinations selected from that broader universe based on academic
        reputation, perceived quality, geographic preferences and personal
        interest.

        The objective of the tool is to move from this initial shortlist to a
        more structured and data-driven final decision. External datasets are
        combined with customizable user preferences to identify the destinations
        that best match the decision-maker's priorities.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Destinations", len(df))

    with col2:
        st.metric("Decision Criteria", 5)

    with col3:
        st.metric("Academic Data", "QS")

    with col4:
        st.metric("City Data", "QS + Numbeo")

    st.markdown("---")

    st.subheader("Decision Framework")

    framework = pd.DataFrame(
        {
            "Criterion": [
                "Academic Quality",
                "Employer Reputation",
                "Cost of Living",
                "Safety",
                "City Attractiveness"
            ],
            "Purpose": [
                "Measures the academic strength of the institution",
                "Captures employer perception of the university",
                "Measures relative affordability including rent",
                "Measures perceived safety of the destination",
                "Captures the attractiveness of the student city"
            ]
        }
    )

    st.dataframe(
        framework,
        hide_index=True,
        width="stretch"
    )

    st.info(
        "Use the navigation menu on the left to build your ranking, "
        "compare destinations or explore the underlying data."
    )

# ---------------------------------------------------
# BUILD YOUR RANKING
# ---------------------------------------------------

elif page == "Build Your Ranking":

    st.title("Build Your Ranking")

    st.info(
        f"Scores are relative to the {len(df)} destinations included in the dataset. "
        "A score of 100 represents the best-performing destination in this sample "
        "for that specific criterion, not an absolute maximum."
    )

    st.write(
        "Adjust the importance of each criterion. "
        "The five weights must add up to 100%."
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        academic_weight = st.slider(
            "Academic Quality",
            0,
            100,
            30
        )

    with col2:
        employer_weight = st.slider(
            "Employer Reputation",
            0,
            100,
            25
        )

    with col3:
        cost_weight = st.slider(
            "Cost of Living",
            0,
            100,
            15
        )

    with col4:
        safety_weight = st.slider(
            "Safety",
            0,
            100,
            10
        )

    with col5:
        attractiveness_weight = st.slider(
            "City Attractiveness",
            0,
            100,
            20
        )

    total_weight = (
        academic_weight
        + employer_weight
        + cost_weight
        + safety_weight
        + attractiveness_weight
    )

    if total_weight == 100:
        st.success("Total weight: 100%")
    else:
        st.warning(
            f"Total weight: {total_weight}%. "
            "Adjust the sliders until the total equals 100%."
        )

    if total_weight == 100:

        df["Final_Score"] = (
            df["Academic_Score"] * academic_weight
            + df["Employer_Score"] * employer_weight
            + df["Cost_Score"] * cost_weight
            + df["Safety_Score"] * safety_weight
            + df["Attractiveness_Score"] * attractiveness_weight
        ) / 100

        ranking = df.sort_values(
            "Final_Score",
            ascending=False
        ).copy()

        ranking["Rank"] = range(1, len(ranking) + 1)

        ranking["Final_Score"] = (
            ranking["Final_Score"].round(1)
        )

        # -------------------------------------------
        # TOP 3
        # -------------------------------------------

        st.subheader("Top Destinations")

        top1, top2, top3 = st.columns(3)

        first = ranking.iloc[0]
        second = ranking.iloc[1]
        third = ranking.iloc[2]

        with top1:
            with st.container(border=True):
                st.markdown("### 🥇 #1")
                st.markdown(
                    f"**{first['University']}**"
                )
                st.caption(
                    f"{first['City']}, {first['Country']}"
                )
                st.metric(
                    "Final Score",
                    f"{first['Final_Score']:.1f} / 100"
                )

        with top2:
            with st.container(border=True):
                st.markdown("### 🥈 #2")
                st.markdown(
                    f"**{second['University']}**"
                )
                st.caption(
                    f"{second['City']}, {second['Country']}"
                )
                st.metric(
                    "Final Score",
                    f"{second['Final_Score']:.1f} / 100"
                )

        with top3:
            with st.container(border=True):
                st.markdown("### 🥉 #3")
                st.markdown(
                    f"**{third['University']}**"
                )
                st.caption(
                    f"{third['City']}, {third['Country']}"
                )
                st.metric(
                    "Final Score",
                    f"{third['Final_Score']:.1f} / 100"
                )

        # -------------------------------------------
        # FULL RANKING
        # -------------------------------------------

        st.subheader("Full Ranking")

        ranking_table = ranking[
            [
                "Rank",
                "University",
                "City",
                "Country",
                "Final_Score"
            ]
        ].copy()

        ranking_table = ranking_table.rename(
            columns={
                "Final_Score": "Score"
            }
        )

        st.dataframe(
            ranking_table,
            hide_index=True,
            width="stretch",
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    format="%d"
                ),
                "Score": st.column_config.NumberColumn(
                    "Score",
                    format="%.1f"
                )
            }
        )

        # -------------------------------------------
        # DESTINATION DETAILS
        # -------------------------------------------

        st.subheader("Destination Details")

        selected_university = st.selectbox(
            "Select a destination",
            ranking["University"].tolist()
        )

        selected = ranking[
            ranking["University"] == selected_university
        ].iloc[0]

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(
                "Academic",
                f"{selected['Academic_Score']:.1f}"
            )

        with c2:
            st.metric(
                "Employer",
                f"{selected['Employer_Score']:.1f}"
            )

        with c3:
            st.metric(
                "Cost",
                f"{selected['Cost_Score']:.1f}"
            )

        with c4:
            st.metric(
                "Safety",
                f"{selected['Safety_Score']:.1f}"
            )

        with c5:
            st.metric(
                "Attractiveness",
                f"{selected['Attractiveness_Score']:.1f}"
            )

# ---------------------------------------------------
# COMPARE DESTINATIONS
# ---------------------------------------------------

elif page == "Compare Destinations":

    st.title("Compare Destinations")

    st.write(
        "Compare up to three exchange destinations across "
        "the five normalized decision criteria."
    )

    comparison_universities = st.multiselect(
        "Select up to 3 destinations",
        options=df["University"].tolist(),
        default=df["University"].head(3).tolist(),
        max_selections=3
    )

    if comparison_universities:

        categories = [
            "Academic",
            "Employer",
            "Cost",
            "Safety",
            "Attractiveness"
        ]

        fig = go.Figure()

        for university in comparison_universities:

            row = df[
                df["University"] == university
            ].iloc[0]

            values = [
                row["Academic_Score"],
                row["Employer_Score"],
                row["Cost_Score"],
                row["Safety_Score"],
                row["Attractiveness_Score"]
            ]

            values += values[:1]

            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories + categories[:1],
                    fill="toself",
                    name=university
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            height=650
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.subheader("Score Comparison")

        comparison_table = df[
            df["University"].isin(
                comparison_universities
            )
        ][
            [
                "University",
                "Academic_Score",
                "Employer_Score",
                "Cost_Score",
                "Safety_Score",
                "Attractiveness_Score"
            ]
        ].copy()

        comparison_table = comparison_table.rename(
            columns={
                "Academic_Score": "Academic",
                "Employer_Score": "Employer Reputation",
                "Cost_Score": "Cost",
                "Safety_Score": "Safety",
                "Attractiveness_Score": "Attractiveness"
            }
        )

        numeric_comparison_columns = [
            "Academic",
            "Employer Reputation",
            "Cost",
            "Safety",
            "Attractiveness"
        ]

        comparison_table[numeric_comparison_columns] = (
            comparison_table[numeric_comparison_columns]
            .round(1)
        )

        st.dataframe(
            comparison_table,
            hide_index=True,
            width="stretch"
        )

        st.caption(
            f"Normalized scores are relative to the {len(df)} "
            "destinations included in the dataset."
        )

# ---------------------------------------------------
# EXPLORE DATA
# ---------------------------------------------------

elif page == "Explore Data":

    st.title("Explore Data")

    st.write(
        "Explore the underlying raw data used by the model."
    )

    countries = sorted(
        df["Country"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_countries = st.multiselect(
        "Filter by country",
        countries
    )

    filtered_df = df.copy()

    if selected_countries:
        filtered_df = filtered_df[
            filtered_df["Country"].isin(
                selected_countries
            )
        ]

    raw_table = filtered_df[
        [
            "University",
            "City",
            "Country",
            "Academic_Ranking",
            "Employer_Reputation_Raw",
            "Cost_of_Living_Raw",
            "Safety_Raw",
            "City_Attractiveness_Raw"
        ]
    ].copy()

    raw_table = raw_table.rename(
        columns={
            "Academic_Ranking": "Academic Ranking",
            "Employer_Reputation_Raw": "Employer Reputation",
            "Cost_of_Living_Raw": "Cost of Living + Rent",
            "Safety_Raw": "Safety Index",
            "City_Attractiveness_Raw": "City Attractiveness"
        }
    )

    st.dataframe(
        raw_table,
        hide_index=True,
        width="stretch"
    )

    st.caption(
        "This table reports the raw source data before "
        "normalization and user-defined weighting."
    )

# ---------------------------------------------------
# METHODOLOGY
# ---------------------------------------------------

elif page == "Methodology":

    st.title("Methodology & Sources")

    st.write(
        """
        The model combines university-level and city-level indicators.
        Raw variables are transformed to a common 0–100 scale before
        applying user-defined weights.
        """
    )

    # -----------------------------------------------
    # ACADEMIC
    # -----------------------------------------------

    st.subheader("Academic Quality")

    st.markdown(
        """
        **Source:** QS World University Rankings by Subject –
        Business & Management Studies 2025.

        The original ranking position is used as the raw academic
        indicator. Since a lower ranking position represents stronger
        performance, the variable is inverted during normalization.
        """
    )

    # -----------------------------------------------
    # EMPLOYER
    # -----------------------------------------------

    st.subheader("Employer Reputation")

    st.markdown(
        """
        **Source:** QS Employer Reputation indicator –
        Business & Management Studies 2025.

        The original QS Employer Reputation score measures how
        institutions are perceived by employers. Higher raw scores
        correspond to stronger employer reputation.
        """
    )

    # -----------------------------------------------
    # COST
    # -----------------------------------------------

    st.subheader("Cost of Living")

    st.markdown(
        """
        **Source:** Numbeo Cost of Living Plus Rent Index 2025.

        The Cost of Living Plus Rent Index was selected instead of
        the standalone Cost of Living Index because accommodation
        represents a material component of expenditure for an
        international exchange student.

        Lower raw cost values receive higher normalized scores.
        """
    )

    st.markdown(
        "**Proxy observations used where direct 2025 city data were unavailable:**"
    )

    st.markdown(
        """
        - **Ithaca:** estimated using Pittsburgh × 95%
        - **Ann Arbor:** average of Pittsburgh and Columbus
        - **St. Gallen:** average of Bern and Basel × 95%
        - **Lille:** Lyon × 95%
        - **Vallendar:** Cologne × 90%
        """
    )

    # -----------------------------------------------
    # SAFETY
    # -----------------------------------------------

    st.subheader("Safety")

    st.markdown(
        """
        **Source:** Numbeo Safety Index by City 2025.

        Higher Safety Index values represent safer destinations and
        therefore receive higher normalized scores.
        """
    )

    st.markdown(
        """
        **Proxy treatment:** where a direct observation was unavailable
        for Vallendar, nearby Koblenz was used as the reference city.
        """
    )

    # -----------------------------------------------
    # CITY ATTRACTIVENESS
    # -----------------------------------------------

    st.subheader("City Attractiveness")

    st.markdown(
        """
        **Source:** QS Best Student Cities 2025.

        The indicator is used to capture the relative attractiveness
        of each destination from an international student perspective.
        Higher raw values correspond to higher attractiveness.
        """
    )

    # -----------------------------------------------
    # NORMALIZATION
    # -----------------------------------------------

    st.subheader("Normalization")

    st.write(
        """
        Since the underlying variables use different measurement
        scales, each criterion is transformed using min-max
        normalization.
        """
    )

    st.markdown(
        "**For criteria where higher values are better:**"
    )

    st.code(
        "Score = (x - min) / (max - min) × 100",
        language=None
    )

    st.markdown(
        "**For criteria where lower values are better "
        "(Academic Ranking and Cost of Living):**"
    )

    st.code(
        "Score = (max - x) / (max - min) × 100",
        language=None
    )

    st.caption(
        f"Normalized scores are relative to the {len(df)} "
        "destinations included in the dataset."
    )

    # -----------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------

    st.subheader("Final Score")

    st.write(
        """
        Users assign a weight to each of the five criteria.
        The weights must sum to 100%.
        """
    )

    st.code(
        "Final Score = Σ (Normalized Criterion Score × User Weight)",
        language=None
    )

    st.write(
        """
        The resulting composite score is used to rank destinations
        from highest to lowest according to the user's selected
        priorities.
        """
    )

    st.info(
        "The model is designed as a decision-support tool rather than "
        "an objective universal ranking. Results depend on both the "
        "underlying dataset and the preferences selected by the user."
    )