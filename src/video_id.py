video_id = "VIDEO_ID_HERE"  # your YouTube video ID
comments = get_video_comments(video_id)
len(comments)
🔹 STEP 6: Create DataFrame
python
Copy code
df = pd.DataFrame(comments, columns=["comment"])
