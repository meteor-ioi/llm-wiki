"""
Config Manager
=============
管理多个知识库配置，支持切换、添加、删除。
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_CONFIG_DIR = Path.home() / ".llm-wiki"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.json"
DEFAULT_WIKI_PATH = Path.home() / "Documents" / "llm-wiki" / "default"


class WikiConfig:
    def __init__(
        self,
        name: str,
        path: str,
        created_at: str,
    ):
        self.name = name
        self.path = path
        self.created_at = created_at


class Config:
    def __init__(
        self,
        version: str = "1.0",
        current_wiki: Optional[str] = None,
        wikis: Optional[List[WikiConfig]] = None,
    ):
        self.version = version
        self.current_wiki = current_wiki
        self.wikis = wikis or []

    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "current_wiki": self.current_wiki,
            "wikis": [
                {
                    "name": w.name,
                    "path": w.path,
                    "created_at": w.created_at,
                }
                for w in self.wikis
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Config":
        wikis = [
            WikiConfig(
                name=w["name"],
                path=w["path"],
                created_at=w["created_at"],
            )
            for w in data.get("wikis", [])
        ]
        return cls(
            version=data.get("version", "1.0"),
            current_wiki=data.get("current_wiki"),
            wikis=wikis,
        )


class ConfigManager:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config_dir = DEFAULT_CONFIG_DIR

    def load(self) -> Config:
        """加载配置，如果不存在返回空配置"""
        if not self.config_path.exists():
            return Config()

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Config.from_dict(data)

    def save(self, config: Config) -> None:
        """保存配置"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config.to_dict(), f, ensure_ascii=False, indent=2)

    def add_wiki(self, config: Config, name: str, path: str, created_at: str) -> Config:
        """添加一个新的知识库"""
        # 检查是否已存在同名
        for wiki in config.wikis:
            if wiki.name == name:
                # 同名，覆盖
                wiki.path = path
                config.current_wiki = path
                self.save(config)
                return config

        config.wikis.append(WikiConfig(name=name, path=path, created_at=created_at))
        config.current_wiki = path
        self.save(config)
        return config

    def switch_wiki(self, config: Config, name_or_path: str) -> Optional[str]:
        """切换当前知识库，返回切换后的路径，找不到返回 None"""
        # 先按名称找
        for wiki in config.wikis:
            if wiki.name == name_or_path:
                config.current_wiki = wiki.path
                self.save(config)
                return wiki.path

        # 按路径找
        for wiki in config.wikis:
            if wiki.path == name_or_path or wiki.path.endswith(name_or_path):
                config.current_wiki = wiki.path
                self.save(config)
                return wiki.path

        return None

    def get_current_wiki_path(self, config: Config) -> Optional[str]:
        """获取当前激活的知识库路径"""
        return config.current_wiki

    def remove_wiki(self, config: Config, name: str) -> bool:
        """从配置中移除一个知识库（不删除用户数据）"""
        original_len = len(config.wikis)
        config.wikis = [w for w in config.wikis if w.name != name]
        if len(config.wikis) == original_len:
            return False

        if config.current_wiki and any(w.path == config.current_wiki for w in config.wikis):
            pass
        elif config.wikis:
            config.current_wiki = config.wikis[0].path
        else:
            config.current_wiki = None

        self.save(config)
        return True
