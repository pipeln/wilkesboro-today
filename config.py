#!/usr/bin/env python3
"""
Centralized Configuration Module
All secrets and configuration in one secure place
"""

import os
import sys
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Centralized configuration management for Wilkesboro Today."""
    
    # Supabase Configuration
    SUPABASE_URL: str = ''
    SUPABASE_KEY: str = ''
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = ''
    TELEGRAM_CHAT_ID: str = ''
    
    # GitHub Configuration
    GITHUB_TOKEN: str = ''
    
    # WordPress Configuration (optional)
    WP_API_URL: str = ''
    WP_USERNAME: str = ''
    WP_APP_PASSWORD: str = ''
    
    # Gemini AI Configuration (optional)
    GEMINI_API_KEY: str = ''
    
    # Application Settings
    ASTRO_BUILD_DIR: str = '/root/.openclaw/workspace/website-design'
    LOG_DIR: str = '/root/.openclaw/workspace/logs'
    
    def __post_init__(self):
        """Load from environment variables."""
        self.SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
        self.SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
        self.TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        self.TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
        self.GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
        self.WP_API_URL = os.environ.get('WP_API_URL', '')
        self.WP_USERNAME = os.environ.get('WP_USERNAME', '')
        self.WP_APP_PASSWORD = os.environ.get('WP_APP_PASSWORD', '')
        self.GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
        self.ASTRO_BUILD_DIR = os.environ.get('ASTRO_BUILD_DIR', '/root/.openclaw/workspace/website-design')
        self.LOG_DIR = os.environ.get('LOG_DIR', '/root/.openclaw/workspace/logs')
    
    def validate(self, required: Optional[List[str]] = None) -> List[str]:
        """
        Validate that required configuration is set.
        
        Args:
            required: List of required config keys. If None, uses default set.
            
        Returns:
            List of missing configuration keys
        """
        if required is None:
            required = ['SUPABASE_URL', 'SUPABASE_KEY', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
        
        missing = []
        for key in required:
            value = getattr(self, key, '')
            if not value or value.strip() == '':
                missing.append(key)
        
        return missing
    
    def validate_or_exit(self, required: Optional[List[str]] = None) -> None:
        """
        Validate configuration and exit if missing required values.
        
        Args:
            required: List of required config keys
        """
        missing = self.validate(required)
        if missing:
            print("❌ Configuration Error: Missing required environment variables:")
            for key in missing:
                print(f"   - {key}")
            print("\nPlease set these in your .env file and try again.")
            sys.exit(1)
    
    def is_configured(self, key: str) -> bool:
        """Check if a specific configuration value is set."""
        value = getattr(self, key, '')
        return bool(value and value.strip())
    
    def get(self, key: str, default: str = '') -> str:
        """Get a configuration value with a default."""
        return getattr(self, key, default)
    
    def mask_secret(self, value: str, visible_chars: int = 4) -> str:
        """Mask a secret value for safe logging."""
        if not value:
            return '[NOT SET]'
        if len(value) <= visible_chars * 2:
            return '*' * len(value)
        return value[:visible_chars] + '*' * (len(value) - visible_chars * 2) + value[-visible_chars:]
    
    def print_status(self) -> None:
        """Print configuration status (with secrets masked)."""
        print("="*60)
        print("CONFIGURATION STATUS")
        print("="*60)
        
        configs = [
            ('Supabase URL', self.SUPABASE_URL),
            ('Supabase Key', self.mask_secret(self.SUPABASE_KEY)),
            ('Telegram Token', self.mask_secret(self.TELEGRAM_BOT_TOKEN)),
            ('Telegram Chat ID', self.TELEGRAM_CHAT_ID),
            ('GitHub Token', self.mask_secret(self.GITHUB_TOKEN)),
            ('WordPress URL', self.WP_API_URL or '[NOT SET]'),
            ('Gemini API Key', self.mask_secret(self.GEMINI_API_KEY)),
        ]
        
        for name, value in configs:
            status = '✅' if value and value != '[NOT SET]' else '❌'
            print(f"{status} {name}: {value}")
        
        print("="*60)


# Global config instance
config = Config()


if __name__ == "__main__":
    # When run directly, show configuration status
    config.print_status()
    
    # Validate required config
    missing = config.validate()
    if missing:
        print(f"\n⚠️  Missing required configuration: {', '.join(missing)}")
    else:
        print("\n✅ All required configuration is set!")
