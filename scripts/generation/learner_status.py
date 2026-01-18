
def save_learner_status(learners_df, tracks, base_path):
    """Save learner status files"""
    print("Saving learner status data...")
    
    for track in tracks:
        track_learners = learners_df[learners_df['Track'] == track]
        filepath = f"{base_path}/Status Records/{track}/Learner_Status.csv"
        track_learners.to_csv(filepath, index=False)
        print(f"Saved {len(track_learners)} learners for {track}")

