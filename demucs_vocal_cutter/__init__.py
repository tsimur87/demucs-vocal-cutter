import yaml
import os

def load_config(config_path="demucs_vocal_cutter/config.yaml"):
    """Load configuration from config.yaml"""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {
            'temp_dir': 'temp_demucs',
            'output_dir': 'Outputs',
            'input_dir': 'Inputs',
            'default_model': 'htdemucs_ft',
            'default_quality': 'best',
            'supported_platforms': {
                'youtube': ['youtube.com', 'youtu.be'],
                'tiktok': ['tiktok.com'],
                'instagram': ['instagram.com'],
                'facebook': ['facebook.com', 'fb.com', 'fb.watch'],
                'twitter': ['twitter.com', 'x.com'],
                'vimeo': ['vimeo.com'],
                'reddit': ['reddit.com'],
                'soundcloud': ['soundcloud.com']
            }
        }

# Load config and make it available as a module-level variable
config = load_config()