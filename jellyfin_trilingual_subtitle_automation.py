#!/usr/bin/env python3
"""
Jellyfin Trilingual Subtitle Automation
Watches for Chinese and English subtitle pairs in Jellyfin media folders
and automatically generates trilingual subtitles (Chinese, Pinyin, English)
"""

import os
import time
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Tuple
from pypinyin import pinyin, Style
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_time(time_str: str) -> float:
    """
    Convert SRT timestamp to seconds for comparison.
    Format: 00:01:23,456 -> seconds as float
    """
    time_str = time_str.strip()
    hours, minutes, rest = time_str.split(':')
    seconds, milliseconds = rest.split(',')
    
    total_seconds = (
        int(hours) * 3600 +
        int(minutes) * 60 +
        int(seconds) +
        int(milliseconds) / 1000.0
    )
    return total_seconds


def parse_srt(filename: str) -> List[Dict]:
    """
    Parse an SRT file and return a list of subtitle entries.
    Each entry is a dict with: index, start_time, end_time, start_sec, end_sec, text
    """
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newlines to get individual subtitle blocks
    blocks = re.split(r'\n\n+', content.strip())
    
    subtitles = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        
        # Parse the subtitle block
        index = lines[0].strip()
        timestamp = lines[1].strip()
        text = '\n'.join(lines[2:])
        
        # Extract start and end times
        times = timestamp.split(' --> ')
        if len(times) == 2:
            start_time = times[0].strip()
            end_time = times[1].strip()
            
            subtitles.append({
                'index': index,
                'start_time': start_time,
                'end_time': end_time,
                'start_sec': parse_time(start_time),
                'end_sec': parse_time(end_time),
                'text': text
            })
    
    return subtitles


def chinese_to_pinyin(text: str) -> str:
    """
    Convert Chinese text to pinyin with tone marks.
    """
    # Generate pinyin with tone marks
    pinyin_list = pinyin(text, style=Style.TONE)
    
    # Join the pinyin syllables with spaces
    result = ' '.join([p[0] for p in pinyin_list])
    
    return result


def find_matching_english(chinese_sub: Dict, english_subs: List[Dict], last_match_index: int = 0) -> Tuple[Dict, int]:
    """
    Find the English subtitle that best matches the Chinese subtitle timing.
    Uses timestamp overlap to match.
    """
    best_match = None
    best_overlap = 0
    best_index = last_match_index
    
    # Start searching from the last matched index to improve performance
    for i in range(last_match_index, len(english_subs)):
        eng = english_subs[i]
        
        # Calculate overlap between Chinese and English subtitle times
        overlap_start = max(chinese_sub['start_sec'], eng['start_sec'])
        overlap_end = min(chinese_sub['end_sec'], eng['end_sec'])
        overlap = overlap_end - overlap_start
        
        if overlap > 0 and overlap > best_overlap:
            best_overlap = overlap
            best_match = eng
            best_index = i
        
        # If we've passed the Chinese subtitle's end time, stop searching
        if eng['start_sec'] > chinese_sub['end_sec']:
            break
    
    return best_match, best_index


def merge_subtitles_by_time(chinese_subs: List[Dict], english_subs: List[Dict]) -> List[Dict]:
    """
    Merge Chinese and English subtitles by matching timestamps.
    """
    merged = []
    last_match_index = 0
    
    for chinese in chinese_subs:
        # Find the best matching English subtitle
        english, last_match_index = find_matching_english(
            chinese, english_subs, last_match_index
        )
        
        if english:
            # Generate pinyin from Chinese text
            pinyin_text = chinese_to_pinyin(chinese['text'])
            
            # Create merged entry using Chinese timestamps
            merged.append({
                'index': str(len(merged) + 1),
                'start_time': chinese['start_time'],
                'end_time': chinese['end_time'],
                'chinese': chinese['text'],
                'pinyin': pinyin_text,
                'english': english['text']
            })
        else:
            # No English match found - Chinese only with pinyin
            pinyin_text = chinese_to_pinyin(chinese['text'])
            merged.append({
                'index': str(len(merged) + 1),
                'start_time': chinese['start_time'],
                'end_time': chinese['end_time'],
                'chinese': chinese['text'],
                'pinyin': pinyin_text,
                'english': '[No English subtitle]'
            })
    
    return merged


def write_trilingual_srt(subtitles: List[Dict], output_filename: str):
    """
    Write the trilingual subtitles to an SRT file.
    Format: Chinese (single line), Pinyin (single line), English (can be multi-line)
    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        for sub in subtitles:
            # Write subtitle block
            f.write(f"{sub['index']}\n")
            f.write(f"{sub['start_time']} --> {sub['end_time']}\n")
            
            # Chinese - replace line breaks with spaces to keep on one line
            chinese_single_line = sub['chinese'].replace('\n', ' ')
            f.write(f"{chinese_single_line}\n")
            
            # Pinyin - already single line
            f.write(f"{sub['pinyin']}\n")
            
            # English - keep as-is (may have multiple lines)
            f.write(f"{sub['english']}\n")
            f.write("\n")  # Blank line between blocks


def find_subtitle_pairs(directory: str) -> List[Tuple[str, str, str]]:
    """
    Find matching Chinese and English subtitle pairs in a directory.
    Returns list of tuples: (video_basename, chinese_srt_path, english_srt_path)
    """
    pairs = []
    path = Path(directory)
    
    # Find all subtitle files
    chinese_subs = list(path.glob("*.chs.srt")) + list(path.glob("*.chi.srt")) + list(path.glob("*.zh.srt")) + list(path.glob("*.zho.srt"))
    english_subs = list(path.glob("*.eng.srt")) + list(path.glob("*.en.srt"))
    
    # Match pairs
    for chinese_file in chinese_subs:
        # Extract base filename
        base_name = chinese_file.stem
        for suffix in ['.chs', '.chi', '.zh', '.zho']:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
                break
        
        # Look for matching English subtitle
        for english_file in english_subs:
            eng_base = english_file.stem
            for suffix in ['.eng', '.en']:
                if eng_base.endswith(suffix):
                    eng_base = eng_base[:-len(suffix)]
                    break
            
            if base_name == eng_base:
                pairs.append((base_name, str(chinese_file), str(english_file)))
                break
    
    return pairs


def process_subtitle_pair(chinese_file: str, english_file: str, output_file: str):
    """
    Process a Chinese-English subtitle pair and create trilingual output.
    """
    logger.info(f"Processing: {Path(chinese_file).name} + {Path(english_file).name}")
    
    try:
        chinese_subs = parse_srt(chinese_file)
        logger.info(f"  Found {len(chinese_subs)} Chinese entries")
        
        english_subs = parse_srt(english_file)
        logger.info(f"  Found {len(english_subs)} English entries")
        
        merged = merge_subtitles_by_time(chinese_subs, english_subs)
        logger.info(f"  Merged {len(merged)} subtitle entries")
        
        write_trilingual_srt(merged, output_file)
        logger.info(f"  ✓ Created: {Path(output_file).name}")
        
        return True
    except Exception as e:
        logger.error(f"  ✗ Error processing {Path(chinese_file).name}: {e}")
        return False


def watch_directory(directory: str, interval: int = 60):
    """
    Watch a directory for new subtitle pairs and process them automatically.
    """
    logger.info(f"Watching directory: {directory}")
    logger.info(f"Check interval: {interval} seconds")
    logger.info("Press Ctrl+C to stop")
    
    processed_pairs = set()
    
    try:
        while True:
            pairs = find_subtitle_pairs(directory)
            
            for base_name, chinese_file, english_file in pairs:
                # Create output filename
                output_file = str(Path(directory) / f"{base_name}.srt")
                
                # Check if already processed
                pair_key = (chinese_file, english_file)
                if pair_key in processed_pairs or Path(output_file).exists():
                    continue
                
                # Process the pair
                if process_subtitle_pair(chinese_file, english_file, output_file):
                    processed_pairs.add(pair_key)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("\nStopping watcher...")


def main():
    parser = argparse.ArgumentParser(
        description='Jellyfin Trilingual Subtitle Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single subtitle pair
  %(prog)s /path/to/movie/folder

  # Watch a directory for new subtitle pairs
  %(prog)s /path/to/movies --watch

  # Watch with custom check interval
  %(prog)s /path/to/movies --watch --interval 30
        """
    )
    
    parser.add_argument(
        'directory',
        help='Directory containing subtitle files'
    )
    
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch directory for new subtitle pairs'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Check interval in seconds (default: 60)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Validate directory
    if not Path(args.directory).is_dir():
        logger.error(f"Error: {args.directory} is not a valid directory")
        return 1
    
    if args.watch:
        watch_directory(args.directory, args.interval)
    else:
        # Process once
        pairs = find_subtitle_pairs(args.directory)
        
        if not pairs:
            logger.info("No subtitle pairs found")
            return 0
        
        logger.info(f"Found {len(pairs)} subtitle pair(s)")
        
        success_count = 0
        for base_name, chinese_file, english_file in pairs:
            output_file = str(Path(args.directory) / f"{base_name}.srt")
            if process_subtitle_pair(chinese_file, english_file, output_file):
                success_count += 1
        
        logger.info(f"\nProcessed {success_count}/{len(pairs)} pairs successfully")
    
    return 0


if __name__ == "__main__":
    exit(main())
