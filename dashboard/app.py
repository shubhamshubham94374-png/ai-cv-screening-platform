import streamlit as st
import plotly.express as px
import pandas as pd
from db import run_query

st.set_page_config(page_title="AI CV Screening Dashboard", layout="wide")

st.title("📋 AI-Powered CV Screening Platform")
st.caption("Recruiter Dashboard")

# --- Top metrics ---
candidate_count_df = run_query("SELECT COUNT(*) as count FROM candidates")
job_count_df = run_query("SELECT COUNT(*) as count FROM jobs")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Candidates", int(candidate_count_df["count"][0]))
with col2:
    st.metric("Total Jobs", int(job_count_df["count"][0]))

st.divider()

# --- Job selector ---
jobs_df = run_query("SELECT id, title, company FROM jobs ORDER BY id")

if jobs_df.empty:
    st.warning("No jobs found. Create a job posting via the API first.")
else:
    job_options = {f"{row['title']} ({row['company'] or 'N/A'}) - ID {row['id']}": row['id'] for _, row in jobs_df.iterrows()}
    selected_job_label = st.selectbox("Select a Job to view candidate rankings:", options=list(job_options.keys()))
    selected_job_id = job_options[selected_job_label]

    st.subheader("Candidate Rankings")

    ranking_query = f"""
    SELECT
        c.id AS candidate_id,
        c.name,
        c.email,
        ms.total_score,
        ms.required_skills_score,
        ms.preferred_skills_score,
        ms.experience_score,
        ms.education_score,
        ai.recommendation
    FROM match_scores ms
    JOIN candidates c ON c.id = ms.candidate_id
    LEFT JOIN ai_insights ai ON ai.candidate_id = ms.candidate_id AND ai.job_id = ms.job_id
    WHERE ms.job_id = {selected_job_id}
    ORDER BY ms.total_score DESC
    """
    rankings_df = run_query(ranking_query)

    if rankings_df.empty:
        st.info("No scored candidates yet for this job. Run scoring via the API first.")
    else:
        st.dataframe(
            rankings_df,
            use_container_width=True,
            column_config={
                "total_score": st.column_config.ProgressColumn(
                    "Total Score", min_value=0, max_value=100, format="%.1f"
                ),
            },
        )

    st.divider()
    st.subheader("Skill Gap Analysis")

    skill_gap_query = f"""
    SELECT missing_required_skills
    FROM match_scores
    WHERE job_id = {selected_job_id}
    """
    skill_gap_df = run_query(skill_gap_query)

    if not skill_gap_df.empty:
        all_missing_skills = []
        for skills_list in skill_gap_df["missing_required_skills"].dropna():
            all_missing_skills.extend(skills_list)

        if all_missing_skills:
            missing_counts = pd.Series(all_missing_skills).value_counts().reset_index()
            missing_counts.columns = ["Skill", "Number of Candidates Missing It"]

            fig = px.bar(
                missing_counts,
                x="Skill",
                y="Number of Candidates Missing It",
                title="Most Commonly Missing Required Skills",
                color="Number of Candidates Missing It",
                color_continuous_scale="Reds",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing required skills across all scored candidates!")

    st.divider()
    st.subheader("Match Score Distribution")

    distribution_query = f"""
    SELECT total_score
    FROM match_scores
    WHERE job_id = {selected_job_id}
    """
    distribution_df = run_query(distribution_query)

    if not distribution_df.empty:
        fig_hist = px.histogram(
            distribution_df,
            x="total_score",
            nbins=10,
            title="Distribution of Candidate Match Scores",
            labels={"total_score": "Total Match Score"},
        )
        fig_hist.update_layout(yaxis_title="Number of Candidates")
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("No scores available yet to display a distribution.")

    st.divider()
    st.subheader("Candidate Detail View")

    if not rankings_df.empty:
        candidate_options = {
            f"{row['name']} (ID {row['candidate_id']})": row['candidate_id']
            for _, row in rankings_df.iterrows()
        }
        selected_candidate_label = st.selectbox(
            "Select a candidate to view full AI insights:",
            options=list(candidate_options.keys()),
        )
        selected_candidate_id = candidate_options[selected_candidate_label]

        insight_query = f"""
        SELECT summary, strengths, weaknesses, interview_questions, recommendation, recommendation_justification
        FROM ai_insights
        WHERE candidate_id = {selected_candidate_id} AND job_id = {selected_job_id}
        """
        insight_df = run_query(insight_query)

        if insight_df.empty:
            st.info("No AI insights generated yet for this candidate. Run the insights endpoint first.")
        else:
            insight = insight_df.iloc[0]

            st.markdown(f"**Recommendation:** {insight['recommendation']}")
            st.markdown(f"**Summary:** {insight['summary']}")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Strengths**")
                for s in insight["strengths"]:
                    st.markdown(f"- {s}")
            with col_b:
                st.markdown("**Weaknesses**")
                for w in insight["weaknesses"]:
                    st.markdown(f"- {w}")

            st.markdown("**Suggested Interview Questions**")
            for q in insight["interview_questions"]:
                st.markdown(f"- {q}")

            st.markdown(f"**Justification:** {insight['recommendation_justification']}")
    else:
        st.info("No candidates available for detail view.")