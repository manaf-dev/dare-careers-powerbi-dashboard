import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_assessments(learners_df, num_weeks, start_date, tracks, base_path):
    """Generate lab and quiz data"""
    print("Generating assessment data...")

    labs = []
    quizzes = []

    for week in range(1, num_weeks + 1):
        assessment_date = start_date + timedelta(days=week * 7 - 2)

        for _, learner in learners_df.iterrows():
            # Skip if dropped out before this week
            if learner["ProgramStatus"] == "Dropped Out":
                if learner["CompletionDate"]:
                    dropout_date = datetime.strptime(
                        learner["CompletionDate"], "%Y-%m-%d"
                    )
                    if dropout_date < assessment_date:
                        continue

            # Determine learner performance tier
            if learner["Certified"] == "Yes":
                # High performers: 80-100
                lab_mean, lab_std = 88, 8
                quiz_mean, quiz_std = 90, 7
                completion_rate = 0.98
            elif learner["Graduated"] == "Yes":
                # Medium performers: 70-90
                lab_mean, lab_std = 78, 10
                quiz_mean, quiz_std = 80, 10
                completion_rate = 0.92
            else:
                # Lower performers: 60-80
                lab_mean, lab_std = 68, 12
                quiz_mean, quiz_std = 70, 12
                completion_rate = 0.75

            # Lab submission
            if random.random() < completion_rate:
                lab_score = int(np.clip(np.random.normal(lab_mean, lab_std), 0, 100))
                labs.append(
                    {
                        "LearnerID": learner["LearnerID"],
                        "LearnerName": learner["LearnerName"],
                        "Cohort": learner["Cohort"],
                        "LabName": f"Week {week} Lab",
                        "Score": lab_score,
                        "MaxScore": 100,
                        "SubmissionDate": (
                            assessment_date + timedelta(days=random.randint(0, 2))
                        ).strftime("%Y-%m-%d"),
                    }
                )

            # Quiz submission (higher completion rate)
            if random.random() < min(0.98, completion_rate + 0.10):
                quiz_score = int(np.clip(np.random.normal(quiz_mean, quiz_std), 0, 100))
                quizzes.append(
                    {
                        "LearnerID": learner["LearnerID"],
                        "LearnerName": learner["LearnerName"],
                        "Cohort": learner["Cohort"],
                        "QuizName": f"Week {week} Quiz",
                        "Score": quiz_score,
                        "MaxScore": 100,
                        "CompletionDate": (
                            assessment_date - timedelta(days=random.randint(0, 1))
                        ).strftime("%Y-%m-%d"),
                    }
                )

    labs_df = pd.DataFrame(labs)
    quizzes_df = pd.DataFrame(quizzes)

    # Save by track
    for track in tracks:
        track_learners = learners_df[learners_df["Track"] == track]["LearnerID"].values

        for week in range(1, num_weeks + 1):
            # Labs
            week_labs = labs_df[
                (labs_df["LearnerID"].isin(track_learners))
                & (labs_df["LabName"] == f"Week {week} Lab")
            ]
            if not week_labs.empty:
                filepath = (
                    f"{base_path}/Lab and Quizzes/{track}/Week{week}_Lab_Grades.csv"
                )
                week_labs.to_csv(filepath, index=False)

            # Quizzes
            week_quizzes = quizzes_df[
                (quizzes_df["LearnerID"].isin(track_learners))
                & (quizzes_df["QuizName"] == f"Week {week} Quiz")
            ]
            if not week_quizzes.empty:
                filepath = (
                    f"{base_path}/Lab and Quizzes/{track}/Week{week}_Quiz_Grades.csv"
                )
                week_quizzes.to_csv(filepath, index=False)

    print(f"Generated {len(labs)} lab submissions")
    print(f"Generated {len(quizzes)} quiz submissions")

    return labs_df, quizzes_df

    return labs_df, quizzes_df

    return labs_df, quizzes_df
