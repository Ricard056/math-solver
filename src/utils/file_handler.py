#!/usr/bin/env python3
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class FileHandler:
    """Handles JSON file operations with proper error handling"""
    
    @staticmethod
    def create_directories():
        """Create necessary directory structure"""
        dirs = ['data/input', 'data/output', 'data/temp']
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Load JSON file with error handling"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filepath}: {e}")
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str) -> None:
        """Save JSON file with pretty formatting"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def generate_filename(metadata: Dict[str, Any], extension: str = 'json') -> str:
        """Generate filename from metadata"""
        course = metadata['course']
        assignment = metadata['assignment']
        
        # C3_2025_T18_integrales_v1
        filename = f"C{course['level']}_{assignment['year']}_"
        filename += f"{assignment['type'][0]}{assignment['number']}_"
        filename += f"integrales_v{assignment['iteration']}"
        
        return f"{filename}.{extension}"
    
    @staticmethod
    def is_intermediate_json(data: Dict[str, Any]) -> bool:
        """Detect if JSON is intermediate (has file_info)"""
        return 'file_info' in data.get('metadata', {})
    
    @staticmethod
    def copy_display_settings(global_settings: Dict[str, Any], exercise: Dict[str, Any]) -> Dict[str, Any]:
        """Copy global display settings to individual exercise"""
        display_settings = {
            'units': global_settings.get('units', 'u'),
            'decimal_precision': global_settings.get('decimal_precision', 4),
            'show_steps': global_settings.get('show_steps', False)
        }
        
        if 'equation_format' in global_settings:
            display_settings.update(global_settings['equation_format'])
        
        return display_settings