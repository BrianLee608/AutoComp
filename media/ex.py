from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("a.mp4")
clip2 = VideoFileClip("b.mp4")
final_clip = concatenate_videoclips([clip1,clip2])
print(final_clip.fps)
final_clip.write_videofile("my_concatenation.mp4")
