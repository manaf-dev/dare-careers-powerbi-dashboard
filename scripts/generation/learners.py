import pandas as pd
import random
from datetime import timedelta

def generate_learners(num_learners, first_names, last_names, cohorts, tracks, start_date):
    """Generate learner status data"""
    print("Generating learner data...")
    
    learners = []
    used_names = set()
    
    for i in range(num_learners):
        # Generate unique name
        while True:
            first = random.choice(first_names)
            last = random.choice(last_names)
            full_name = f"{first} {last}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        learner_id = f"L{str(i+1).zfill(4)}"
        cohort = random.choice(cohorts)
        track = random.choice(tracks)
        
        # Determine program status (realistic distribution)
        status_rand = random.random()
        if status_rand < 0.75:  # 75% complete
            program_status = "Completed"
            graduated = "Yes"
            completion_date = start_date + timedelta(days=70)
            # 80% of graduates get certified
            certified = "Yes" if random.random() < 0.80 else "No"
            if track == 'Power BI':
                cert_type = 'Microsoft PL-300' if certified == "Yes" else "N/A"
            else:
                cert_type = 'AWS Solutions Architect' if certified == "Yes" else "N/A"
        elif status_rand < 0.90:  # 15% ongoing
            program_status = "Ongoing"
            graduated = "No"
            completion_date = None
            certified = "No"
            cert_type = "N/A"
        else:  # 10% dropped out
            program_status = "Dropped Out"
            graduated = "No"
            dropout_week = random.randint(2, 6)
            completion_date = start_date + timedelta(days=dropout_week * 7)
            certified = "No"
            cert_type = "N/A"
        
        learners.append({
            'LearnerID': learner_id,
            'LearnerName': full_name,
            'Cohort': cohort,
            'Track': track,
            'ProgramStatus': program_status,
            'Graduated': graduated,
            'Certified': certified,
            'CertificationType': cert_type,
            'EnrollmentDate': start_date.strftime('%Y-%m-%d'),
            'CompletionDate': completion_date.strftime('%Y-%m-%d') if completion_date else ''
        })
    
    learners_df = pd.DataFrame(learners)
    print(f"Generated {len(learners)} learners")
    print(f"Completed: {sum(learners_df['ProgramStatus'] == 'Completed')}")
    print(f"Ongoing: {sum(learners_df['ProgramStatus'] == 'Ongoing')}")
    print(f"Dropped Out: {sum(learners_df['ProgramStatus'] == 'Dropped Out')}")
    print(f"Certified: {sum(learners_df['Certified'] == 'Yes')}")
    
    return learners_df
