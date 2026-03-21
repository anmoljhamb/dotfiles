#!/usr/bin/env python3
"""
Dotfiles Manager - A robust tool for managing dotfiles with symlinks.

Commands:
    link       Create symlinks from repo to home directory
    scan       Find untracked config files/directories
    import     Move selected configs to repo and create symlinks
    status     Verify all symlinks are intact
    uninstall  Remove symlinks and restore backups
"""

import os
import sys
import shutil
import argparse
import fnmatch
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set

# Try to import yaml, fall back to JSON if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    yaml = None

# Try to import rich for beautiful output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


# ============================================================================
# OUTPUT HELPERS
# ============================================================================

class Output:
    """Unified output interface - uses rich if available, falls back to plain text."""
    
    def __init__(self):
        self.console = Console() if HAS_RICH else None
        self.use_rich = HAS_RICH
    
    def print(self, message: str = "", style: str = ""):
        """Print a message with optional styling."""
        if self.use_rich and style:
            self.console.print(message, style=style)
        else:
            print(message)
    
    def success(self, message: str):
        """Print a success message."""
        if self.use_rich:
            self.console.print(f"✓ {message}", style="green")
        else:
            print(f"[OK] {message}")
    
    def error(self, message: str):
        """Print an error message."""
        if self.use_rich:
            self.console.print(f"✗ {message}", style="red")
        else:
            print(f"[ERROR] {message}", file=sys.stderr)
    
    def warning(self, message: str):
        """Print a warning message."""
        if self.use_rich:
            self.console.print(f"⚠ {message}", style="yellow")
        else:
            print(f"[WARN] {message}")
    
    def info(self, message: str):
        """Print an info message."""
        if self.use_rich:
            self.console.print(f"ℹ {message}", style="blue")
        else:
            print(f"[INFO] {message}")
    
    def header(self, message: str):
        """Print a header."""
        if self.use_rich:
            self.console.print(Panel(message, style="cyan bold"))
        else:
            print(f"\n{'=' * 60}")
            print(f"  {message}")
            print(f"{'=' * 60}\n")
    
    def table(self, headers: List[str], rows: List[List[str]], title: str = ""):
        """Print a table."""
        if self.use_rich:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            for header in headers:
                table.add_column(header)
            for row in rows:
                table.add_row(*row)
            self.console.print(table)
        else:
            if title:
                print(f"\n{title}")
                print("-" * len(title))
            # Print headers
            col_widths = [len(h) for h in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
            
            header_line = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
            print(header_line)
            print("-" * len(header_line))
            
            for row in rows:
                print("  ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)))
            print()


# Global output instance
out = Output()


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config:
    """Configuration for the dotfiles manager."""
    repo_root: Path
    backup_dir: Path
    os_patterns: List[str]
    os_mappings: dict
    scan_paths: List[Path]
    auto_import: List[str]
    exclusions_file: Path
    create_parents: bool
    follow_symlinks: bool
    verify_targets: bool
    mappings: dict  # Custom path mappings: repo_path -> home_path
    make_executable: List[str]  # Patterns for files to make executable
    
    @classmethod
    def load(cls, config_path: Path = None) -> "Config":
        """Load configuration from YAML or JSON file."""
        if config_path is None:
            config_path = Path(__file__).parent / "dotfiles.yaml"
        
        if not config_path.exists():
            # Try JSON fallback
            json_path = Path(__file__).parent / "dotfiles.json"
            if json_path.exists():
                config_path = json_path
            else:
                out.error(f"Configuration file not found: {config_path}")
                out.info("Using default configuration")
                return cls._defaults()
        
        try:
            with open(config_path) as f:
                if config_path.suffix == '.json' or not HAS_YAML:
                    data = json.load(f)
                else:
                    data = yaml.safe_load(f)  # type: ignore
        except Exception as e:
            out.error(f"Failed to load config: {e}")
            return cls._defaults()
        
        repo_root = Path(data.get("repo", {}).get("root", ".")).expanduser().resolve()
        
        # Load custom mappings
        mappings = data.get("mappings", {})
        # Convert string paths to Path objects
        mappings = {k: Path(v).expanduser() for k, v in mappings.items()}
        
        return cls(
            repo_root=repo_root,
            backup_dir=repo_root / data.get("repo", {}).get("backup_dir", ".backups"),
            os_patterns=data.get("os_specific", {}).get("patterns", []),
            os_mappings=data.get("os_specific", {}).get("mappings", {}),
            scan_paths=[Path(p).expanduser() for p in data.get("scan_paths", ["~/.config", "~/"])],
            auto_import=data.get("auto_import", []),
            exclusions_file=repo_root / data.get("exclusions_file", ".dotfiles_ignore"),
            create_parents=data.get("linking", {}).get("create_parents", True),
            follow_symlinks=data.get("linking", {}).get("follow_symlinks", True),
            verify_targets=data.get("linking", {}).get("verify_targets", True),
            mappings=mappings,
            make_executable=data.get("make_executable", ["scripts/*", "*.sh", "bin/*"]),
        )
    
    @classmethod
    def _defaults(cls) -> "Config":
        """Return default configuration."""
        repo_root = Path(__file__).parent.resolve()
        return cls(
            repo_root=repo_root,
            backup_dir=repo_root / ".backups",
            os_patterns=[".linux", ".macos", ".darwin"],
            os_mappings={"linux": ".linux", "darwin": ".macos"},
            scan_paths=[Path.home() / ".config", Path.home()],
            auto_import=[],
            exclusions_file=repo_root / ".dotfiles_ignore",
            create_parents=True,
            follow_symlinks=True,
            verify_targets=True,
            mappings={},
            make_executable=["scripts/*", "*.sh", "bin/*"],
        )


# ============================================================================
# EXCLUSIONS / GITIGNORE-STYLE MATCHING
# ============================================================================

class ExclusionMatcher:
    """Matches paths against gitignore-style exclusion patterns."""
    
    def __init__(self, patterns: List[str]):
        self.patterns = [p.strip() for p in patterns if p.strip() and not p.startswith("#")]
    
    @classmethod
    def from_file(cls, path: Path) -> "ExclusionMatcher":
        """Load patterns from a file."""
        if not path.exists():
            return cls([])
        with open(path) as f:
            return cls(f.readlines())
    
    def is_excluded(self, path: str) -> bool:
        """Check if a path matches any exclusion pattern."""
        # Normalize path
        path = path.lstrip("/")
        parts = path.split("/")
        
        for pattern in self.patterns:
            if self._matches(pattern, path, parts):
                return True
        return False
    
    def _matches(self, pattern: str, path: str, parts: List[str]) -> bool:
        """Check if a pattern matches a path."""
        # Handle directory patterns
        if pattern.endswith("/"):
            pattern = pattern[:-1]
            if not any(part == pattern for part in parts):
                return False
        
        # Handle patterns with slashes (anchored to specific level)
        if "/" in pattern:
            # Anchored pattern - must match from root
            if fnmatch.fnmatch(path, pattern):
                return True
            # Or match any component
            for part in parts:
                if fnmatch.fnmatch(part, pattern.split("/")[-1]):
                    return True
        else:
            # Unanchored pattern - matches any component
            for part in parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
            # Also match full path for convenience
            if fnmatch.fnmatch(path, pattern):
                return True
        
        return False


# ============================================================================
# OS DETECTION
# ============================================================================

class OSDetector:
    """Detects current operating system and provides OS-specific utilities."""
    
    @staticmethod
    def get_current_os() -> str:
        """Get current OS identifier."""
        import platform
        system = platform.system().lower()
        if system == "darwin":
            return "darwin"
        elif system == "linux":
            return "linux"
        elif system == "windows":
            return "windows"
        return system
    
    @staticmethod
    def get_os_suffix(config: Config) -> Optional[str]:
        """Get the file suffix for current OS."""
        current_os = OSDetector.get_current_os()
        return config.os_mappings.get(current_os)
    
    @staticmethod
    def select_os_specific(files: List[Path], config: Config) -> List[Path]:
        """Filter files to OS-specific versions where available."""
        os_suffix = OSDetector.get_os_suffix(config)
        if not os_suffix:
            return files
        
        # Group files by their base name (without OS suffix)
        groups = {}
        for f in files:
            base = str(f)
            for suffix in config.os_patterns:
                if base.endswith(suffix):
                    base = base[:-len(suffix)]
                    break
            groups.setdefault(base, []).append(f)
        
        # Select best match for each group
        selected = []
        for base, group in groups.items():
            # Look for exact OS match
            os_match = None
            for f in group:
                if str(f).endswith(os_suffix):
                    os_match = f
                    break
            
            if os_match:
                selected.append(os_match)
            else:
                # No OS-specific version, use generic (no OS suffix)
                generic = [f for f in group if not any(str(f).endswith(s) for s in config.os_patterns)]
                if generic:
                    selected.append(generic[0])
                else:
                    selected.extend(group)
        
        return selected


# ============================================================================
# FILE OPERATIONS
# ============================================================================

class FileManager:
    """Handles file operations with safety and backup support."""
    
    def __init__(self, config: Config):
        self.config = config
        self.backup_dir = config.backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def backup(self, path: Path) -> Optional[Path]:
        """Backup a file/directory before modification."""
        if not path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path.name}_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        # Handle collisions
        counter = 1
        while backup_path.exists():
            backup_path = self.backup_dir / f"{backup_name}_{counter}"
            counter += 1
        
        if path.is_dir():
            shutil.copytree(path, backup_path)
        else:
            shutil.copy2(path, backup_path)
        
        return backup_path
    
    def create_symlink(self, target: Path, link: Path, dry_run: bool = False) -> Tuple[bool, str]:
        """Create a symbolic link with safety checks."""
        target = target.resolve()
        
        # Check if already correctly linked
        if link.is_symlink():
            if link.resolve() == target:
                return True, "already linked"
            else:
                return False, f"wrong target (points to {link.resolve()})"
        
        # Check if file/directory exists
        if link.exists():
            if not dry_run:
                backup_path = self.backup(link)
                if link.is_dir():
                    shutil.rmtree(link)
                else:
                    link.unlink()
            else:
                backup_path = self.backup_dir / f"{link.name}_dryrun"
        else:
            backup_path = None
        
        if dry_run:
            return True, f"would link (backup: {backup_path.name if backup_path else 'none'})"
        
        # Create parent directories
        if self.config.create_parents:
            link.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            link.symlink_to(target)
            return True, f"linked (backup: {backup_path.name if backup_path else 'none'})"
        except OSError as e:
            return False, str(e)
    
    def remove_symlink(self, link: Path, restore_backup: bool = False) -> Tuple[bool, str]:
        """Remove a symlink and optionally restore backup."""
        if not link.is_symlink():
            return False, "not a symlink"
        
        if not restore_backup:
            link.unlink()
            return True, "removed"
        
        # Find most recent backup
        backups = sorted(
            [b for b in self.backup_dir.iterdir() if b.name.startswith(link.name)],
            key=lambda b: b.stat().st_mtime,
            reverse=True
        )
        
        link.unlink()
        
        if backups:
            backup = backups[0]
            if backup.is_dir():
                shutil.copytree(backup, link)
            else:
                shutil.copy2(backup, link)
            return True, f"removed and restored from {backup.name}"
        else:
            return True, "removed (no backup found)"
    
    def move_to_repo(self, source: Path, repo_path: Path, dry_run: bool = False) -> Tuple[bool, Path, str]:
        """Move a file/directory from home to repo."""
        source = source.expanduser().resolve()
        target = repo_path.expanduser().resolve()
        
        if dry_run:
            return True, target, "would move"
        
        # Create parent directories in repo
        target.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.move(str(source), str(target))
            return True, target, "moved"
        except OSError as e:
            return False, target, str(e)


# ============================================================================
# SCANNER
# ============================================================================

@dataclass
class ScannedItem:
    """Represents a scanned file or directory."""
    path: Path
    name: str
    is_dir: bool
    is_tracked: bool
    size: int
    
    def __str__(self):
        icon = "📁" if self.is_dir else "📄"
        status = "✓" if self.is_tracked else "✗"
        return f"{icon} {status} {self.name}"


class Scanner:
    """Scans home directory for untracked config files."""
    
    def __init__(self, config: Config, exclusions: ExclusionMatcher):
        self.config = config
        self.exclusions = exclusions
        self.home = Path.home()
    
    def scan(self) -> List[ScannedItem]:
        """Scan configured paths for untracked items."""
        items = []
        
        for scan_path in self.config.scan_paths:
            scan_path = scan_path.expanduser().resolve()
            if not scan_path.exists():
                continue
            
            # For home directory, only look at hidden files
            if scan_path == self.home:
                items.extend(self._scan_hidden_files(scan_path))
            else:
                items.extend(self._scan_directory(scan_path))
        
        return sorted(items, key=lambda x: (not x.is_dir, x.name.lower()))
    
    def _scan_hidden_files(self, path: Path) -> List[ScannedItem]:
        """Scan for hidden files in home directory."""
        items = []
        
        for entry in path.iterdir():
            # Only hidden files
            if not entry.name.startswith("."):
                continue
            
            # Skip exclusions
            rel_path = str(entry.relative_to(self.home))
            if self.exclusions.is_excluded(rel_path):
                continue
            
            is_tracked = self._is_tracked(entry)
            
            size = self._get_size(entry) if entry.is_dir() else entry.stat().st_size
            
            items.append(ScannedItem(
                path=entry,
                name=entry.name,
                is_dir=entry.is_dir(),
                is_tracked=is_tracked,
                size=size
            ))
        
        return items
    
    def _scan_directory(self, path: Path) -> List[ScannedItem]:
        """Scan a directory (like .config) for config directories."""
        items = []
        
        for entry in path.iterdir():
            # Skip exclusions
            rel_path = str(entry.relative_to(self.home))
            if self.exclusions.is_excluded(rel_path):
                continue
            
            is_tracked = self._is_tracked(entry)
            
            size = self._get_size(entry) if entry.is_dir() else entry.stat().st_size
            
            items.append(ScannedItem(
                path=entry,
                name=rel_path,
                is_dir=entry.is_dir(),
                is_tracked=is_tracked,
                size=size
            ))
        
        return items
    
    def _is_tracked(self, path: Path) -> bool:
        """Check if a path is already tracked in the repo."""
        rel_path = path.relative_to(self.home)
        repo_path = self.config.repo_root / rel_path
        
        # Check if corresponding path exists in repo
        if repo_path.exists():
            return True
        
        # Check if there's a symlink from home pointing to repo
        if path.is_symlink():
            try:
                target = path.resolve()
                return self.config.repo_root in target.parents or target == self.config.repo_root
            except:
                return False
        
        return False
    
    def _get_size(self, path: Path) -> int:
        """Get total size of a directory."""
        total = 0
        try:
            for entry in path.rglob("*"):
                if entry.is_file():
                    total += entry.stat().st_size
        except:
            pass
        return total
    
    def format_size(self, size: int) -> str:
        """Format size in human-readable format."""
        size_float = float(size)
        for unit in ["B", "KB", "MB", "GB"]:
            if size_float < 1024:
                return f"{size_float:.1f} {unit}"
            size_float /= 1024
        return f"{size_float:.1f} TB"


# ============================================================================
# COMMANDS
# ============================================================================

class DotfilesManager:
    """Main dotfiles management interface."""
    
    def __init__(self, config: Config):
        self.config = config
        self.exclusions = ExclusionMatcher.from_file(config.exclusions_file)
        self.file_manager = FileManager(config)
        self.scanner = Scanner(config, self.exclusions)
        self.os_detector = OSDetector()
    
    def cmd_link(self, dry_run: bool = False):
        """Create symlinks from repo to home."""
        out.header("LINK: Creating symlinks from repo to home")
        
        if dry_run:
            out.warning("DRY RUN MODE - No changes will be made")
        
        # Get all files in repo
        repo_files = list(self.config.repo_root.rglob("*"))
        
        # Filter: only files, exclude patterns
        files = []
        for f in repo_files:
            if not f.is_file():
                continue
            
            rel_path = str(f.relative_to(self.config.repo_root))
            
            # Skip exclusions
            if self.exclusions.is_excluded(rel_path):
                continue
            
            # Skip config files themselves
            if f.name in ["dotfiles.yaml", ".dotfiles_ignore", "link_all.py", "dotfiles.py"]:
                continue
            
            files.append(f)
        
        # Handle OS-specific files
        files = OSDetector.select_os_specific(files, self.config)
        
        # Create symlinks
        linked = 0
        skipped = 0
        failed = 0
        results = []
        
        for repo_file in files:
            rel_path = repo_file.relative_to(self.config.repo_root)
            home_path = Path.home() / rel_path
            
            success, message = self.file_manager.create_symlink(repo_file, home_path, dry_run)
            
            if success:
                if "already" in message:
                    skipped += 1
                else:
                    linked += 1
            else:
                failed += 1
            
            status = "✓" if success else "✗"
            results.append([status, str(rel_path), message])
        
        # Print results
        out.table(
            ["Status", "Path", "Result"],
            results,
            f"Linked {linked}, Skipped {skipped}, Failed {failed}"
        )
        
        if dry_run:
            out.warning("This was a dry run. No actual changes were made.")
            out.info("Run without --dry-run to apply changes.")
    
    def cmd_scan(self):
        """Scan for untracked config files."""
        out.header("SCAN: Finding untracked configuration files")
        
        items = self.scanner.scan()
        
        if not items:
            out.success("No untracked configuration files found!")
            return
        
        # Separate tracked and untracked
        untracked = [i for i in items if not i.is_tracked]
        tracked = [i for i in items if i.is_tracked]
        
        # Show untracked items
        if untracked:
            out.print(f"\n[bold cyan]Found {len(untracked)} untracked items:[/bold cyan]\n" if HAS_RICH else f"\nFound {len(untracked)} untracked items:\n")
            
            rows = []
            for i, item in enumerate(untracked, 1):
                icon = "📁" if item.is_dir else "📄"
                size = self.scanner.format_size(item.size)
                rows.append([str(i), icon, item.name, size])
            
            out.table(["#", "Type", "Path", "Size"], rows)
            
            # Show auto-import suggestions
            auto_matches = [item for item in untracked 
                          if any(pattern in item.name for pattern in self.config.auto_import)]
            if auto_matches:
                out.print(f"\n[bold green]Suggested for import (auto-detected):[/bold green]" if HAS_RICH else "\nSuggested for import (auto-detected):")
                for item in auto_matches:
                    out.print(f"  - {item.name}")
        
        # Show tracked count
        if tracked:
            out.info(f"\n{len(tracked)} items already tracked")
        
        out.print(f"\n[dim]Use './dotfiles.py import <numbers>' to import selected items[/dim]" if HAS_RICH else "\nUse './dotfiles.py import <numbers>' to import selected items")
    
    def cmd_import(self, selections: Optional[List[int]] = None, paths: Optional[List[str]] = None, dry_run: bool = False):
        """Import selected configs to repo and create symlinks."""
        out.header("IMPORT: Moving configs to repo and creating symlinks")
        
        if dry_run:
            out.warning("DRY RUN MODE - No changes will be made")
        
        # Get scanned items
        items = self.scanner.scan()
        untracked = [i for i in items if not i.is_tracked]
        
        if not untracked:
            out.info("No untracked items to import. Run './dotfiles.py scan' first.")
            return
        
        # Determine what to import
        to_import = []
        
        if paths:
            # Import specific paths
            for path_str in paths:
                path = Path(path_str).expanduser().resolve()
                for item in untracked:
                    if item.path == path:
                        to_import.append(item)
                        break
        elif selections:
            # Import by number
            for num in selections:
                if 1 <= num <= len(untracked):
                    to_import.append(untracked[num - 1])
                else:
                    out.warning(f"Invalid selection: {num}")
        else:
            # Interactive selection
            out.print("\nSelect items to import (comma-separated numbers, 'all', or 'suggested'):\n")
            
            for i, item in enumerate(untracked, 1):
                icon = "📁" if item.is_dir else "📄"
                is_suggested = any(pattern in item.name for pattern in self.config.auto_import)
                marker = " [suggested]" if is_suggested else ""
                out.print(f"  {i:3}. {icon} {item.name}{marker}")
            
            response = input("\n> ").strip()
            
            if response.lower() == "all":
                to_import = untracked
            elif response.lower() == "suggested":
                to_import = [item for item in untracked 
                           if any(pattern in item.name for pattern in self.config.auto_import)]
            else:
                try:
                    nums = [int(n.strip()) for n in response.split(",")]
                    for num in nums:
                        if 1 <= num <= len(untracked):
                            to_import.append(untracked[num - 1])
                except ValueError:
                    out.error("Invalid input. Please use numbers separated by commas.")
                    return
        
        if not to_import:
            out.info("Nothing selected for import.")
            return
        
        # Confirm
        out.print(f"\nWill import {len(to_import)} items:")
        for item in to_import:
            out.print(f"  - {item.name}")
        
        if not dry_run:
            response = input("\nProceed? [Y/n] ").strip().lower()
            if response and response not in ["y", "yes"]:
                out.info("Import cancelled.")
                return
        
        # Import each item
        imported = 0
        failed = 0
        results = []
        
        for item in to_import:
            # Calculate repo destination
            rel_path = item.path.relative_to(Path.home())
            repo_path = self.config.repo_root / rel_path
            
            # Move to repo
            success, final_path, message = self.file_manager.move_to_repo(
                item.path, repo_path, dry_run
            )
            
            if success:
                # Create symlink from original location to repo
                link_success, link_message = self.file_manager.create_symlink(
                    final_path, item.path, dry_run
                )
                
                if link_success:
                    imported += 1
                    status = "✓"
                else:
                    failed += 1
                    status = "✗"
                    message = f"moved but link failed: {link_message}"
            else:
                failed += 1
                status = "✗"
            
            results.append([status, item.name, message])
        
        out.table(["Status", "Item", "Result"], results)
        
        if dry_run:
            out.warning("This was a dry run. No actual changes were made.")
        else:
            out.success(f"Successfully imported {imported} items")
            if failed:
                out.error(f"Failed to import {failed} items")
    
    def cmd_status(self):
        """Check status of all symlinks."""
        out.header("STATUS: Checking symlink integrity")
        
        # Find all symlinks in home that point to repo
        symlinks = []
        home = Path.home()
        
        for path in home.rglob("*"):
            if not path.is_symlink():
                continue
            
            try:
                target = path.resolve()
                if self.config.repo_root in target.parents or target == self.config.repo_root:
                    symlinks.append((path, target))
            except:
                pass
        
        # Also check ~/.config
        config_dir = home / ".config"
        if config_dir.exists():
            for path in config_dir.rglob("*"):
                if not path.is_symlink():
                    continue
                
                try:
                    target = path.resolve()
                    if self.config.repo_root in target.parents or target == self.config.repo_root:
                        symlinks.append((path, target))
                except:
                    pass
        
        if not symlinks:
            out.info("No dotfile symlinks found.")
            return
        
        # Check each symlink
        ok = 0
        broken = 0
        wrong_target = 0
        results = []
        
        for link, target in symlinks:
            if not target.exists():
                status = "✗"
                message = "BROKEN - target does not exist"
                broken += 1
            elif not self._is_in_repo(target):
                status = "⚠"
                message = f"WRONG TARGET - points outside repo"
                wrong_target += 1
            else:
                status = "✓"
                message = "OK"
                ok += 1
            
            rel_link = str(link.relative_to(home))
            results.append([status, rel_link, message])
        
        out.table(
            ["Status", "Symlink", "Check"],
            results,
            f"OK: {ok}, Broken: {broken}, Wrong Target: {wrong_target}"
        )
        
        if broken > 0:
            out.error(f"Found {broken} broken symlinks. Run './dotfiles.py link' to fix.")
    
    def _is_in_repo(self, path: Path) -> bool:
        """Check if a path is within the repo."""
        try:
            path.relative_to(self.config.repo_root)
            return True
        except ValueError:
            return False
    
    def cmd_uninstall(self, restore: bool = True):
        """Remove symlinks and optionally restore backups."""
        out.header("UNINSTALL: Removing dotfile symlinks")
        
        # Find all symlinks pointing to repo
        symlinks = []
        home = Path.home()
        
        for path in home.rglob("*"):
            if path.is_symlink():
                try:
                    target = path.resolve()
                    if self.config.repo_root in target.parents:
                        symlinks.append(path)
                except:
                    pass
        
        # Also check ~/.config
        config_dir = home / ".config"
        if config_dir.exists():
            for path in config_dir.rglob("*"):
                if path.is_symlink():
                    try:
                        target = path.resolve()
                        if self.config.repo_root in target.parents:
                            symlinks.append(path)
                    except:
                        pass
        
        if not symlinks:
            out.info("No dotfile symlinks found to remove.")
            return
        
        out.print(f"Found {len(symlinks)} symlinks to remove")
        
        if restore:
            out.info("Backups will be restored where available")
        
        response = input("\nProceed? [Y/n] ").strip().lower()
        if response and response not in ["y", "yes"]:
            out.info("Uninstall cancelled.")
            return
        
        removed = 0
        restored = 0
        results = []
        
        for link in symlinks:
            success, message = self.file_manager.remove_symlink(link, restore)
            
            if success:
                removed += 1
                if "restored" in message:
                    restored += 1
            
            status = "✓" if success else "✗"
            rel_link = str(link.relative_to(home))
            results.append([status, rel_link, message])
        
        out.table(["Status", "Symlink", "Result"], results)
        out.success(f"Removed {removed} symlinks, restored {restored} backups")


# ============================================================================
# MAIN CLI
# ============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="Dotfiles Manager - Manage your dotfiles with symlinks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scan                    # Find untracked configs
  %(prog)s link --dry-run          # Preview what would be linked
  %(prog)s link                    # Create all symlinks
  %(prog)s import 1 2 3            # Import items #1, #2, #3 from scan
  %(prog)s import --path ~/.bashrc # Import specific path
  %(prog)s import                  # Interactive selection
  %(prog)s status                  # Check all symlinks
  %(prog)s uninstall               # Remove symlinks and restore backups
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Link command
    link_parser = subparsers.add_parser("link", help="Create symlinks from repo to home")
    link_parser.add_argument("--dry-run", "-n", action="store_true",
                           help="Show what would be done without making changes")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Find untracked configuration files")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import configs to repo and symlink")
    import_parser.add_argument("selections", nargs="*", type=int,
                             help="Item numbers from scan to import")
    import_parser.add_argument("--path", "-p", nargs="+",
                             help="Import specific paths")
    import_parser.add_argument("--dry-run", "-n", action="store_true",
                             help="Show what would be done without making changes")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check status of all symlinks")
    
    # Uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Remove symlinks and restore backups")
    uninstall_parser.add_argument("--no-restore", action="store_true",
                                help="Don't restore backups (just remove symlinks)")
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load configuration
    config = Config.load()
    
    # Create manager
    manager = DotfilesManager(config)
    
    # Execute command
    if args.command == "link":
        manager.cmd_link(dry_run=args.dry_run)
    elif args.command == "scan":
        manager.cmd_scan()
    elif args.command == "import":
        manager.cmd_import(
            selections=args.selections if args.selections else None,
            paths=args.path if args.path else None,
            dry_run=args.dry_run
        )
    elif args.command == "status":
        manager.cmd_status()
    elif args.command == "uninstall":
        manager.cmd_uninstall(restore=not args.no_restore)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
