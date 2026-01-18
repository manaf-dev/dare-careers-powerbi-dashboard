
import numpy as np
import random

import config
from generation.directory_setup import create_directory_structure
from generation.learners import generate_learners
from generation.learner_status import save_learner_status
from generation.attendance import generate_attendance
from generation.assessments import generate_assessments
from generation.participation import generate_participation

def main():
    """Main execution function"""
    # Set random seed for reproducibility
    np.random.seed(config.RANDOM_SEED)
    random.seed(config.RANDOM_SEED)


    # Create directory structure
    create_directory_structure(config.BASE_PATH, config.TRACKS, config.NUM_WEEKS)
    
    # Generate learner data
    learners_df = generate_learners(
        num_learners=config.NUM_LEARNERS,
        first_names=config.FIRST_NAMES,
        last_names=config.LAST_NAMES,
        cohorts=config.COHORTS,
        tracks=config.TRACKS,
        start_date=config.START_DATE
    )
    
    # Save learner status files
    save_learner_status(learners_df, config.TRACKS, config.BASE_PATH)
    
    # Generate attendance data
    attendance_df = generate_attendance(
        learners_df=learners_df,
        num_weeks=config.NUM_WEEKS,
        days_per_week=config.DAYS_PER_WEEK,
        start_date=config.START_DATE,
        tracks=config.TRACKS,
        base_path=config.BASE_PATH
    )

    # Generate lab and quiz data
    labs_df, quizzes_df = generate_assessments(
        learners_df=learners_df,
        num_weeks=config.NUM_WEEKS,
        start_date=config.START_DATE,
        tracks=config.TRACKS,
        base_path=config.BASE_PATH
    )

    # Generate participation data
    participation_df = generate_participation(
        learners_df=learners_df,
        num_weeks=config.NUM_WEEKS,
        days_per_week=config.DAYS_PER_WEEK,
        start_date=config.START_DATE,
        tracks=config.TRACKS,
        base_path=config.BASE_PATH
    )
    



if __name__ == "__main__":
    main()
