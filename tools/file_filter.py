"""
File Filter
===========
递归扫描目录，过滤掉不需要处理的文件（二进制、依赖、构建产物）。
支持自定义 .llm-wiki-ignore 规则。
"""

import os
from pathlib import Path
from typing import List, Set, Pattern
import re


DEFAULT_IGNORE_PATTERNS = {
    # 版本控制
    ".git/",
    ".svn/",
    ".hg/",
    ".gitignore",
    # 依赖
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    "venv/",
    "env/",
    ".env/",
    "*.egg-info/",
    # 构建输出
    "dist/",
    "build/",
    "*.o",
    "*.so",
    "*.dylib",
    "*.a",
    # 二进制和媒体文件（默认跳过）
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.ico",
    "*.svg",
    "*.pdf",
    "*.zip",
    "*.tar.gz",
    "*.rar",
    "*.exe",
    "*.dmg",
    "*.app",
    # 大文件（超过 1MB 跳过）
}

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".c", ".cpp",
    ".h", ".hpp", ".rb", ".php", ".sh", ".bash", ".zsh",
    ".html", ".css", ".scss", ".md", ".markdown", ".rst",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".conf",
}


class FileFilter:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.ignore_patterns: Set[str] = DEFAULT_IGNORE_PATTERNS.copy()
        self._load_custom_ignore()

    def _load_custom_ignore(self):
        """加载用户自定义的 .llm-wiki-ignore"""
        ignore_file = self.root_path / ".llm-wiki-ignore"
        if not ignore_file.exists():
            return

        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    self.ignore_patterns.add(line)

    def _should_ignore(self, path: Path) -> bool:
        """检查是否应该忽略这个路径"""
        path_str = str(path)

        for pattern in self.ignore_patterns:
            if pattern.endswith("/"):
                # 目录匹配
                if any(part == pattern[:-1] for part in path.parts):
                    return True
            elif pattern.startswith("*."):
                # 扩展名匹配
                if path_str.endswith(pattern[1:]):
                    return True

        # 检查文件大小，超过 1MB 跳过
        if path.is_file():
            try:
                size = path.stat().st_size
                if size > 1 * 1024 * 1024:  # 1MB
                    return True
            except OSError:
                return True

        return False

    def scan(self) -> List[Path]:
        """递归扫描目录，返回所有需要处理的文件路径"""
        result: List[Path] = []

        for root, dirs, files in os.walk(self.root_path):
            # 过滤掉忽略的目录
            dirs[:] = [
                d for d in dirs
                if not self._should_ignore(Path(root) / d)
            ]

            for file in files:
                file_path = Path(root) / file
                if not self._should_ignore(file_path):
                    result.append(file_path)

        return sorted(result)

    @staticmethod
    def is_code_file(path: Path) -> bool:
        """判断是否是代码文件"""
        return path.suffix.lower() in CODE_EXTENSIONS

    @staticmethod
    def is_doc_file(path: Path) -> bool:
        """判断是否是文档文件"""
        doc_ext = {".md", ".markdown", ".rst", ".txt", ".readme", ".license"}
        return path.suffix.lower() in doc_ext or path.name.lower().startswith("readme")
