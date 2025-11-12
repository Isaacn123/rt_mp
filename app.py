import streamlit as st
import json
from pathlib import Path

class RTMPGenerator:
    def __init__(self):
        self.platforms = {
            "twitch": {
                "template": "rtmp://live.twitch.tv/app/{stream_key}",
                "help": "Get stream key from Twitch Dashboard -> Settings -> Stream",
                "server": "live.twitch.tv",
                "app_name": "app"
            },
            "youtube": {
                "template": "rtmp://a.rtmp.youtube.com/live2/{stream_key}",
                "help": "Get stream key from YouTube Studio -> Go Live -> Create Stream",
                "server": "a.rtmp.youtube.com", 
                "app_name": "live2"
            },
            "facebook": {
                "template": "rtmp://live-api-s.facebook.com:80/rtmp/{stream_key}",
                "help": "Get stream key from Facebook Live API",
                "server": "live-api-s.facebook.com:80",
                "app_name": "rtmp"
            },
            "custom": {
                "template": "rtmp://{server_url}/{app_name}/{stream_key}",
                "help": "Enter custom RTMP server details for vMix",
                "server": "",
                "app_name": ""
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
    
    def get_server_info(self, platform):
        """Get server and app name for vMix configuration"""
        if platform in self.platforms:
            return {
                "server": self.platforms[platform]["server"],
                "app_name": self.platforms[platform]["app_name"]
            }
        return {"server": "", "app_name": ""}

# Streamlit App
def main():
    st.set_page_config(
        page_title="vMix RTMP URL Generator",
        page_icon="🎥",
        layout="wide"
    )
    
    st.title("🎥 vMix RTMP URL Generator")
    st.write("Generate RTMP URLs and configuration for vMix Streaming")
    
    generator = RTMPGenerator()
    
    # Platform selection
    platform = st.selectbox(
        "Select Streaming Platform",
        list(generator.platforms.keys()),
        format_func=lambda x: x.capitalize()
    )
    
    st.info(generator.platforms[platform]['help'])
    
    # Show platform defaults for non-custom platforms
    if platform != "custom":
        server_info = generator.get_server_info(platform)
        st.write("**Platform Defaults:**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Server", value=server_info["server"], disabled=True)
        with col2:
            st.text_input("Application", value=server_info["app_name"], disabled=True)
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        stream_key = st.text_input(
            "Stream Key",
            type="password",
            placeholder="Enter your stream key here",
            help="Get this from your streaming platform dashboard"
        )
    
    with col2:
        if platform == "custom":
            server_url = st.text_input(
                "RTMP Server URL",
                placeholder="live.example.com or 192.168.1.100"
            )
            app_name = st.text_input(
                "Application Name", 
                placeholder="live, stream, or app"
            )
        else:
            server_url = ""
            app_name = ""
    
    # Configuration name for saving
    config_name = st.text_input(
        "Configuration Name (optional)",
        placeholder="My vMix YouTube Stream"
    )
    
    # Generate button
    if st.button("Generate vMix Configuration", type="primary"):
        if not stream_key:
            st.error("❌ Please enter a stream key")
        elif platform == "custom" and (not server_url or not app_name):
            st.error("❌ Please enter server URL and application name")
        else:
            # Generate RTMP URL
            rtmp_url = generator.generate_rtmp(platform, stream_key, server_url, app_name)
            
            # Get server info for vMix
            if platform == "custom":
                server_info = {"server": server_url, "app_name": app_name}
            else:
                server_info = generator.get_server_info(platform)
            
            st.success("✅ vMix Configuration Generated!")
            
            # Display configuration in tabs
            tab1, tab2, tab3 = st.tabs(["📋 vMix Setup", "🔗 RTMP URL", "💾 Save Configuration"])
            
            with tab1:
                st.subheader("vMix Streaming Configuration")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Method 1: Full URL (Recommended)**")
                    st.code(f"URL: {rtmp_url}", language="bash")
                    st.write("**Steps:**")
                    st.write("1. vMix → Settings → Streaming")
                    st.write("2. Add Destination → Custom")
                    st.write(f"3. URL: `{rtmp_url}`")
                    st.write("4. Click OK")
                
                with col2:
                    st.write("**Method 2: Separate Fields**")
                    st.code(f"URL: rtmp://{server_info['server']}/{server_info['app_name']}", language="bash")
                    st.code(f"Stream Key: {stream_key}", language="bash")
                    st.write("**Steps:**")
                    st.write("1. vMix → Settings → Streaming")
                    st.write("2. Add Destination → Custom")
                    st.write(f"3. URL: `rtmp://{server_info['server']}/{server_info['app_name']}`")
                    st.write(f"4. Stream Key: `{stream_key}`")
                    st.write("5. Click OK")
            
            with tab2:
                st.subheader("Complete RTMP URL")
                st.code(rtmp_url, language="bash")
                
                # Copy to clipboard
                if st.button("Copy RTMP URL to Clipboard"):
                    st.code(rtmp_url)
                    st.success("URL ready to copy! (Select and copy manually)")
            
            with tab3:
                if config_name:
                    # Save configuration
                    config_dir = Path("/app/configs")
                    config_dir.mkdir(exist_ok=True)
                    
                    config = {
                        "name": config_name,
                        "platform": platform,
                        "stream_key": stream_key,
                        "server_url": server_url if platform == "custom" else server_info["server"],
                        "app_name": app_name if platform == "custom" else server_info["app_name"],
                        "rtmp_url": rtmp_url,
                        "for_vmix": True
                    }
                    
                    try:
                        config_file = config_dir / f"{config_name}.json"
                        with open(config_file, 'w') as f:
                            json.dump(config, f, indent=2)
                        st.success(f"✅ Configuration saved as '{config_name}'")
                        
                        st.write("**Saved Configuration:**")
                        st.json(config)
                    except Exception as e:
                        st.error(f"Error saving configuration: {e}")
                else:
                    st.info("💡 Enter a configuration name above to save these settings")
    
    # Sidebar with saved configurations and instructions
    st.sidebar.title("vMix Instructions")
    st.sidebar.write("""
    **Quick Guide:**
    1. Get stream key from your platform
    2. Generate configuration here
    3. In vMix: Settings → Streaming
    4. Add Destination → Custom
    5. Use the generated URL or separate fields
    6. Start Streaming!
    """)
    
    # Show saved configurations
    st.sidebar.title("💾 Saved Configs")
    config_dir = Path("/app/configs")
    if config_dir.exists():
        config_files = list(config_dir.glob("*.json"))
        if config_files:
            for config_file in config_files:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                if st.sidebar.button(f"📁 {config['name']}"):
                    st.session_state.loaded_config = config
                    # Auto-fill form with loaded config
                    st.experimental_rerun()
        else:
            st.sidebar.info("No saved configurations")
    
    # Load configuration if selected
    if 'loaded_config' in st.session_state:
        config = st.session_state.loaded_config
        st.sidebar.success(f"Loaded: {config['name']}")
        
        # Pre-fill form with loaded config
        st.write("---")
        st.subheader(f"📂 Loaded Configuration: {config['name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Platform:** {config['platform']}")
            st.write(f"**Server:** {config['server_url']}")
            st.write(f"**App Name:** {config['app_name']}")
        with col2:
            st.write(f"**Stream Key:** {'*' * len(config['stream_key'])}")
            st.code(f"RTMP URL: {config['rtmp_url']}")
        
        if st.button("Use This Configuration"):
            # Set form values (you'd need to use session state to pre-fill the form)
            st.info("To use this config, manually copy the values above")

if __name__ == "__main__":
    main()