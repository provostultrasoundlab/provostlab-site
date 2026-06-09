import os
import subprocess
import glob

def convert_gifs():
    research_dir = "/Users/jeanprovost/provostlab-site/public/research"
    gif_files = glob.glob(os.path.join(research_dir, "*.gif"))
    
    print(f"Found {len(gif_files)} GIF files to convert in {research_dir}.")
    
    for gif_path in gif_files:
        base_name = os.path.splitext(os.path.basename(gif_path))[0]
        
        poster_path = os.path.join(research_dir, f"{base_name}.webp")
        mp4_path = os.path.join(research_dir, f"{base_name}.mp4")
        webm_path = os.path.join(research_dir, f"{base_name}.webm")
        
        print(f"\nProcessing: {os.path.basename(gif_path)}...")
        
        # 1. Generate WebP Poster image (first frame)
        if not os.path.exists(poster_path):
            print(f"  Generating poster: {os.path.basename(poster_path)}")
            # -vframes 1 extracts the first frame
            cmd = ["ffmpeg", "-y", "-i", gif_path, "-vframes", "1", "-f", "image2", "-c:v", "libwebp", poster_path]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"  Poster already exists: {os.path.basename(poster_path)}")
            
        # 2. Convert to MP4 (H.264, even dimensions required for yuv420p)
        if not os.path.exists(mp4_path):
            print(f"  Converting to MP4: {os.path.basename(mp4_path)}")
            cmd = [
                "ffmpeg", "-y", "-i", gif_path, 
                "-movflags", "faststart", 
                "-pix_fmt", "yuv420p", 
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", 
                mp4_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"  MP4 already exists: {os.path.basename(mp4_path)}")
            
        # 3. Convert to WebM (VP9, lightweight)
        if not os.path.exists(webm_path):
            print(f"  Converting to WebM: {os.path.basename(webm_path)}")
            cmd = [
                "ffmpeg", "-y", "-i", gif_path, 
                "-c:v", "libvpx-vp9", 
                "-b:v", "0", 
                "-crf", "30", 
                "-an", 
                webm_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"  WebM already exists: {os.path.basename(webm_path)}")

if __name__ == "__main__":
    convert_gifs()
