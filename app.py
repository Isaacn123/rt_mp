import streamlit as st
import json
from pathlib import Path

# st.title("🎥 RTMP URL Generator for OBS")
# st.write("Generate RTMP URLs for streaming TV stations from OBS")

# # Platform selection
# platform = st.selectbox(
#     "Select Streaming Platform",
#     ["twitch", "youtube", "facebook", "custom"]
# )

# # Platform-specific instructions
# instructions = {
#     "twitch": "Get stream key from: Twitch Dashboard → Settings → Stream",
#     "youtube": "Get stream key from: YouTube Studio → Go Live → Create Stream", 
#     "facebook": "Get stream key from Facebook Live API",
#     "custom": "Enter your custom RTMP server details"
# }

# st.info(instructions[platform])

# # Input fields
# stream_key = st.text_input("Stream Key", type="password")

# server_url = ""
# app_name = ""

# if platform == "custom":
#     col1, col2 = st.columns(2)
#     with col1:
#         server_url = st.text_input("RTMP Server URL (e.g., live.example.com)")
#     with col2:
#         app_name = st.text_input("Application Name (e.g., live)")

# # Generate RTMP URL
# if st.button("Generate RTMP URL"):
#     if not stream_key:
#         st.error("Please enter a stream key")
#     elif platform == "custom" and (not server_url or not app_name):
#         st.error("Please enter server URL and application name for custom RTMP")
#     else:
#         # Generate RTMP URL based on platform
#         rtmp_templates = {
#             "twitch": f"rtmp://live.twitch.tv/app/{stream_key}",
#             "youtube": f"rtmp://a.rtmp.youtube.com/live2/{stream_key}",
#             "facebook": f"rtmp://live-api-s.facebook.com:80/rtmp/{stream_key}",
#             "custom": f"rtmp://{server_url}/{app_name}/{stream_key}"
#         }
        
#         rtmp_url = rtmp_templates[platform]
        
#         st.success("RTMP URL Generated Successfully!")
#         st.code(rtmp_url, language="bash")
        
#         # OBS Setup Instructions
#         st.subheader("OBS Setup Instructions")
#         st.write("1. Open OBS Studio")
#         st.write("2. Go to **Settings → Stream**")
#         st.write("3. Select **Service: Custom**")
#         st.write(f"4. **Server:** `{rtmp_url.rsplit('/', 1)[0]}`")
#         st.write(f"5. **Stream Key:** `{stream_key}`")
#         st.write("6. Click **OK** and start streaming!")
        
#         # Copy to clipboard
#         if st.button("Copy RTMP URL to Clipboard"):
#             st.code(rtmp_url)
#             st.success("URL copied! (Manual copy required in Streamlit Cloud)")

# # Save configurations
# st.sidebar.header("💾 Save Configurations")
# config_name = st.sidebar.text_input("Configuration Name")
# stream_key_save = st.sidebar.text_input("Stream Key (for saving)", type="password")

# if st.sidebar.button("Save Configuration"):
#     if config_name and stream_key_save:
#         config = {
#             "platform": platform,
#             "stream_key": stream_key_save,
#             "server_url": server_url,
#             "app_name": app_name
#         }
        
#         # Save to file (in real app, use proper database)
#         try:
#             with open("stream_configs.json", "a") as f:
#                 f.write(json.dumps(config) + "\n")
#             st.sidebar.success("Configuration saved!")
#         except Exception as e:
#             st.sidebar.error(f"Error saving: {e}")


class RTMPGenerator:
    def __init__(self):
        self.platforms = {
            "twitch": {
                "template": "rtmp://live.twitch.tv/app/{stream_key}",
                "help": "Get stream key from Twitch Dashboard -> Settings -> Stream",
                "server": "rtmp://live.twitch.tv/app"
            },
            "youtube": {
                "template": "rtmp://a.rtmp.youtube.com/live2/{stream_key}",
                "help": "Get stream key from YouTube Studio -> Go Live -> Create Stream", 
                "server": "rtmp://a.rtmp.youtube.com/live2"
            },
            "facebook": {
                "template": "rtmp://live-api-s.facebook.com:80/rtmp/{stream_key}",
                "help": "Get stream key from Facebook Live API",
                "server": "rtmp://live-api-s.facebook.com:80/rtmp"
            },
            "custom": {
                "template": "rtmp://{server_url}/{app_name}/{stream_key}",
                "help": "Enter custom RTMP server details",
                "server": "rtmp://your-server.com/app"
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

# Streamlit App
def main():
    st.set_page_config(
        page_title="RTMP URL Generator",
        page_icon="🎥",
        layout="wide"
    )
    
    st.title("🎥 RTMP URL Generator for OBS")
    st.write("Generate RTMP URLs for streaming from OBS to various platforms")
    
    generator = RTMPGenerator()
    
    # Sidebar for saved configs
    st.sidebar.title("💾 Saved Configurations")
    configs = generator.load_configs()
    
    if configs:
        for config in configs:
            with st.sidebar.expander(config['name']):
                st.write(f"Platform: {config['platform']}")
                st.code(config['rtmp_url'])
                if st.button(f"Load {config['name']}", key=config['name']):
                    st.session_state.loaded_config = config
    else:
        st.sidebar.info("No saved configurations")
    
    # Main form
    with st.form("rtmp_generator"):
        col1, col2 = st.columns(2)
        
        with col1:
            platform = st.selectbox(
                "Streaming Platform",
                list(generator.platforms.keys()),
                format_func=lambda x: x.capitalize()
            )
            
            st.info(generator.platforms[platform]['help'])
            
            stream_key = st.text_input(
                "Stream Key",
                type="password",
                placeholder="Enter your stream key here"
            )
        
        with col2:
            if platform == "custom":
                server_url = st.text_input(
                    "RTMP Server URL",
                    placeholder="live.example.com"
                )
                app_name = st.text_input(
                    "Application Name", 
                    placeholder="live"
                )
            else:
                server_url = ""
                app_name = ""
                st.write("### Platform Defaults")
                st.code(f"Server: {generator.platforms[platform]['server']}")
        
        config_name = st.text_input(
            "Configuration Name (optional)",
            placeholder="My Twitch Stream"
        )
        
        submitted = st.form_submit_button("Generate RTMP URL")
    
    # Generate RTMP URL
    if submitted:
        if not stream_key:
            st.error("❌ Please enter a stream key")
        elif platform == "custom" and (not server_url or not app_name):
            st.error("❌ Please enter server URL and application name")
        else:
            rtmp_url = generator.generate_rtmp(platform, stream_key, server_url, app_name)
            
            st.success("✅ RTMP URL Generated!")
            st.code(rtmp_url, language="bash")
            
            # OBS Instructions
            st.subheader("📹 OBS Setup Instructions")
            server_part = rtmp_url.rsplit('/', 1)[0] if platform != "custom" else f"rtmp://{server_url}/{app_name}"
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**OBS Settings:**")
                st.write("1. Settings → Stream")
                st.write("2. Service: **Custom**")
                st.write(f"3. Server: `{server_part}`")
                st.write(f"4. Stream Key: `{stream_key}`")
            with col2:
                st.write("**Quick Copy:**")
                st.code(f"Server: {server_part}")
                st.code(f"Stream Key: {stream_key}")
            
            # Save configuration
            if config_name:
                try:
                    config_file = generator.save_config(config_name, platform, stream_key, server_url, app_name)
                    st.success(f"✅ Configuration saved as '{config_name}'")
                except Exception as e:
                    st.error(f"Error saving configuration: {e}")

if __name__ == "__main__":
    main()