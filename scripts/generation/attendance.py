import pandas as pd
import random
from datetime import datetime, timedelta

def generate_attendance(learners_df, num_weeks, days_per_week, start_date, tracks, base_path):
    """Generate attendance data for all weeks"""
    print("Generating attendance data...")
    
    all_attendance = []
    
    for week in range(1, num_weeks + 1):
        for day in range(1, days_per_week + 1):
            session_date = start_date + timedelta(days=(week-1)*7 + (day-1))
            
            daily_attendance = []
            
            for _, learner in learners_df.iterrows():
                # Skip if learner dropped out before this date
                if learner['ProgramStatus'] == 'Dropped Out':
                    if learner['CompletionDate'] and \
                       datetime.strptime(learner['CompletionDate'], '%Y-%m-%d') < session_date:
                        continue
                
                # Determine if learner attends (varies by learner performance)
                base_attendance_rate = 0.85  # 85% base rate
                
                # High performers attend more (90-95%)
                # Average performers: 80-90%
                # Low performers: 60-80%
                learner_factor = random.gauss(1.0, 0.15)  # Normal distribution
                attendance_probability = min(0.98, base_attendance_rate * learner_factor)
                
                if random.random() < attendance_probability:
                    # Generate realistic duration
                    # Most sessions are 2-3 hours (120-180 minutes)
                    # Some leave early (60-120 minutes)
                    duration_choice = random.random()
                    
                    if duration_choice < 0.70:  # 70% attend full session
                        duration = random.randint(140, 180)
                    elif duration_choice < 0.90:  # 20% leave a bit early
                        duration = random.randint(90, 139)
                    else:  # 10% leave very early or have issues
                        duration = random.randint(35, 89)
                    
                    join_time = session_date.replace(hour=9, minute=random.randint(0, 10))
                    leave_time = join_time + timedelta(minutes=duration)
                    
                    daily_attendance.append({
                        'LearnerID': learner['LearnerID'],
                        'LearnerName': learner['LearnerName'],
                        'Cohort': learner['Cohort'],
                        'JoinTime': join_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'LeaveTime': leave_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'Duration_Minutes': duration
                    })
                else:
                    # Small chance they join briefly then leave (technical issues, etc.)
                    if random.random() < 0.30:
                        duration = random.randint(5, 29)  # Under 30 minutes
                        join_time = session_date.replace(hour=9, minute=random.randint(0, 30))
                        leave_time = join_time + timedelta(minutes=duration)
                        
                        daily_attendance.append({
                            'LearnerID': learner['LearnerID'],
                            'LearnerName': learner['LearnerName'],
                            'Cohort': learner['Cohort'],
                            'JoinTime': join_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'LeaveTime': leave_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'Duration_Minutes': duration
                        })
            
            # Save daily attendance file
            if daily_attendance:
                df = pd.DataFrame(daily_attendance)
                
                # Group by track and save
                for track in tracks:
                    track_learners = learners_df[learners_df['Track'] == track]['LearnerID'].values
                    track_attendance = df[df['LearnerID'].isin(track_learners)]
                    
                    if not track_attendance.empty:
                        filepath = f"{base_path}/Zoom Attendance/{track}/Week {week}/Day{day}_Attendance.csv"
                        track_attendance.to_csv(filepath, index=False)
            
            all_attendance.extend(daily_attendance)
    
    print(f"Generated {len(all_attendance)} attendance records")
    print(f"Average attendance per session: {len(all_attendance) / (num_weeks * days_per_week):.1f}")
    
    return pd.DataFrame(all_attendance)
