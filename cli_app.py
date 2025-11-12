#!/usr/bin/env python3
import json
import os
from pathlib import Path

class RTMPGenerator:
    def __init__(self):
        self.platforms = {
            "twitch": {
                "template": "rtmp://live.twitch.tv/app/{stream_key}",
                "help": "Get stream key from Twitch Dashboard -> Settings -> Stream",
                "server": "rtmp://live.twitch.tv/app",
                "example_key": "live_123456789_abcdefghij"
            },
            "youtube": {
                "template": "rtmp://a.rtmp.youtube.com/live2/{stream_key}",
                "help": "Get stream key from YouTube Studio -> Go Live -> Create Stream",
                "server": "rtmp://a.rtmp.youtube.com/live2",
                "example_key": "xxxx-xxxx-xxxx-xxxx"
            },
            "facebook": {
                "template": "rtmp://live-api-s.facebook.com:80/rtmp/{stream_key}",
                "help": "Get stream key from Facebook Live API",
                "server": "rtmp://live-api-s.facebook.com:80/rtmp",
                "example_key": "123456789012345?ds=1"
            },
            "custom": {
                "template": "rtmp://{server_url}/{app_name}/{stream_key}",
                "help": "Enter custom RTMP server details",
                "server": "rtmp://your-server.com/app",
                "example_key": "your_stream_key"
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
    
    def save_config(self, config_name, platform, stream_key, server_url="", app_name=""):
        config_dir = Path("/app/configs")
        config_dir.mkdir(exist_ok=True)
        
        config = {
            "name": config_name,
            "platform": platform,
            "stream_key": stream_key,
            "server_url": server_url,
            "app_name": app_name,
            "rtmp_url": self.generate_rtmp(platform, stream_key, server_url, app_name)
        }
        
        config_file = config_dir / f"{config_name}.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config_file
    
    def load_configs(self):
        config_dir = Path("/app/configs")
        configs = []
        if config_dir.exists():
            for config_file in config_dir.glob("*.json"):
                with open(config_file, 'r') as f:
                    configs.append(json.load(f))
        return configs

def main():
    generator = RTMPGenerator()
    
    print("🎥 RTMP URL Generator for OBS")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Generate new RTMP URL")
        print("2. View saved configurations")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            generate_rtmp_url(generator)
        elif choice == "2":
            view_saved_configs(generator)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def generate_rtmp_url(generator):
    print("\nAvailable platforms:")
    for i, platform in enumerate(generator.platforms.keys(), 1):
        print(f"{i}. {platform.capitalize()}")
    
    while True:
        try:
            choice = input("\nSelect platform (number): ")
            platform = list(generator.platforms.keys())[int(choice)-1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
    
    print(f"\n{generator.platforms[platform]['help']}")
    print(f"Example: {generator.platforms[platform]['example_key']}")
    
    stream_key = input("\nEnter your stream key: ").strip()
    
    server_url = ""
    app_name = ""
    if platform == "custom":
        server_url = input("Enter RTMP server URL (e.g., live.example.com): ").strip()
        app_name = input("Enter application name (e.g., live): ").strip()
    
    # Generate RTMP URL
    rtmp_url = generator.generate_rtmp(platform, stream_key, server_url, app_name)
    
    print(f"\n✅ RTMP URL Generated!")
    print(f"Platform: {platform.upper()}")
    print(f"Full RTMP URL: {rtmp_url}")
    
    # Show OBS setup
    server_part = rtmp_url.rsplit('/', 1)[0] if platform != "custom" else f"rtmp://{server_url}/{app_name}"
    print(f"\n📹 OBS Setup:")
    print(f"Server: {server_part}")
    print(f"Stream Key: {stream_key}")
    
    # Save configuration
    save = input("\nSave this configuration? (y/n): ").lower().strip()
    if save == 'y':
        config_name = input("Enter configuration name: ").strip()
        config_file = generator.save_config(config_name, platform, stream_key, server_url, app_name)
        print(f"✅ Configuration saved to: {config_file}")

def view_saved_configs(generator):
    configs = generator.load_configs()
    if not configs:
        print("\nNo saved configurations found.")
        return
    
    print("\n📁 Saved Configurations:")
    for i, config in enumerate(configs, 1):
        print(f"\n{i}. {config['name']} ({config['platform']})")
        print(f"   RTMP URL: {config['rtmp_url']}")

if __name__ == "__main__":
    main()