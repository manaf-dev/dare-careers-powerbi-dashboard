import pandas as pd
import random
from datetime import datetime, timedelta

def generate_participation(learners_df, num_weeks, days_per_week, start_date, tracks, base_path):
    """Generate participation data"""
    print("Generating participation data...")
    
    participation = []
    
    comments_by_score = {
        5: ["Outstanding contributions", "Excellent engagement", "Exceptional participation", 
            "Very active and insightful", "Consistently excellent contributions"],
        4: ["Good participation", "Actively engaged", "Strong contributions", 
            "Good questions and comments", "Well engaged in discussions"],
        3: ["Moderate participation", "Average engagement", "Participated when asked", 
            "Satisfactory involvement", "Standard participation level"],
        2: ["Limited participation", "Minimal engagement", "Quiet in discussions", 
            "Needs more involvement", "Could participate more"],
        1: ["Very limited participation", "No engagement", "Silent throughout", 
            "Did not participate", "Absent from discussions"]
    }
    
    for week in range(1, num_weeks + 1):
        for day in range(1, days_per_week + 1):
            session_date = start_date + timedelta(days=(week-1)*7 + (day-1))
            
            for _, learner in learners_df.iterrows():
                # Skip if dropped out
                if learner['ProgramStatus'] == 'Dropped Out':
                    if learner['CompletionDate']:
                        dropout_date = datetime.strptime(learner['CompletionDate'], '%Y-%m-%d')
                        if dropout_date < session_date:
                            continue
                
                # Only record participation if they likely attended
                if random.random() < 0.85:
                    # Performance tier affects participation
                    if learner['Certified'] == 'Yes':
                        score_weights = [0.05, 0.10, 0.20, 0.35, 0.30]  # Skewed toward 4-5
                    elif learner['Graduated'] == 'Yes':
                        score_weights = [0.10, 0.15, 0.35, 0.30, 0.10]  # Centered on 3-4
                    else:
                        score_weights = [0.20, 0.30, 0.30, 0.15, 0.05]  # Skewed toward 1-3
                    
                    score = random.choices([1, 2, 3, 4, 5], weights=score_weights)[0]
                    
                    participation.append({
                        'LearnerID': learner['LearnerID'],
                        'LearnerName': learner['LearnerName'],
                        'Cohort': learner['Cohort'],
                        'Date': session_date.strftime('%Y-%m-%d'),
                        'ParticipationScore': score,
                        'Comments': random.choice(comments_by_score[score])
                    })
    
    participation_df = pd.DataFrame(participation)
    
    # Save by track
    for track in tracks:
        track_learners = learners_df[learners_df['Track'] == track]['LearnerID'].values
        track_participation = participation_df[participation_df['LearnerID'].isin(track_learners)]
        
        if not track_participation.empty:
            filepath = f"{base_path}/Participation Records/{track}/Daily_Participation.csv"
            track_participation.to_csv(filepath, index=False)
    
    print(f"Generated {len(participation)} participation records")
    
    return participation_df
