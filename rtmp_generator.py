import json
import pyperclip  # For copying to clipboard
import os

class RTMPGenerator:
    def __init__(self):
        self.platforms = {
            "twitch": {
                "template": "rtmp://live.twitch.tv/app/{stream_key}",
                "help": "Get stream key from Twitch Dashboard -> Settings -> Stream"
            },
            "youtube": {
                "template": "rtmp://a.rtmp.youtube.com/live2/{stream_key}",
                "help": "Get stream key from YouTube Studio -> Go Live -> Create Stream"
            },
            "facebook": {
                "template": "rtmp://live-api-s.facebook.com:80/rtmp/{stream_key}",
                "help": "Get stream key from Facebook Live API"
            },
            "custom": {
                "template": "rtmp://{server_url}/{app_name}/{stream_key}",
                "help": "Enter custom RTMP server details"
            }
        }
    
    def generate_rtmp(self, platform, stream_key, server_url="", app_name=""):
        if platform not in self.platforms:
            return "Invalid platform selected"
        
        template = self.platforms[platform]["template"]
        
        if platform == "custom":
            rtmp_url = template.format(
                server_url=server_url,
                app_name=app_name,
                stream_key=stream_key
            )
        else:
            rtmp_url = template.format(stream_key=stream_key)
        
        return rtmp_url
    
    def display_platforms(self):
        print("Available platforms:")
        for i, platform in enumerate(self.platforms.keys(), 1):
            print(f"{i}. {platform.capitalize()}")
        print()

def main():
    generator = RTMPGenerator()
    
    print("=== RTMP URL Generator for OBS ===")
    generator.display_platforms()
    
    # Get platform choice
    while True:
        try:
            choice = input("Select platform (number): ")
            platform = list(generator.platforms.keys())[int(choice)-1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
    
    # Get stream key
    stream_key = input("Enter your stream key: ")
    
    # Additional info for custom RTMP
    server_url = ""
    app_name = ""
    if platform == "custom":
        server_url = input("Enter RTMP server URL: ")
        app_name = input("Enter application name: ")
    
    # Generate RTMP URL
    rtmp_url = generator.generate_rtmp(platform, stream_key, server_url, app_name)
    
    print(f"\n=== Your RTMP URL ===")
    print(f"Platform: {platform.upper()}")
    print(f"RTMP URL: {rtmp_url}")
    print(f"\nHelp: {generator.platforms[platform]['help']}")
    
    # Try to copy to clipboard
    try:
        pyperclip.copy(rtmp_url)
        print("✓ RTMP URL copied to clipboard!")
    except:
        print("Note: Install 'pyperclip' for automatic clipboard copy")
    
    print("\nUse this URL in OBS: Settings -> Stream -> Service: Custom")
    print("Server: ", rtmp_url.split('/{stream_key}')[0] if '{stream_key}' in rtmp_url else rtmp_url.rsplit('/', 1)[0])
    print("Stream Key: ", stream_key)

if __name__ == "__main__":
    main()