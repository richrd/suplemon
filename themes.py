#-*- encoding: utf-8
"""
Theme loader
"""
import os
import imp
from helpers import *

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class Theme:
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid
        self.scopes = {}

class ThemeLoader:
    def __init__(self, app=None):
        self.app = app

        self.curr_path = os.path.dirname(os.path.realpath(__file__))
        # The modules subdirectory
        self.theme_path = os.path.join(self.curr_path, "themes" + os.sep)
        # Module instances
        self.themes = {}
        self.current_theme = None


    def log(self, data, type=None):
        if self.app:
            self.app.log(data, type)
        else:
            print(data)


    def load(self, name):
        fullpath = ''.join([self.theme_path, name, '.tmTheme'])

        if not os.path.exists(fullpath):
            return None

        self.log("Loading theme " + name, LOG_INFO)

        tree = ET.parse(fullpath)
        root = tree.getroot()

        for child in root:
            config = self.parse(child)
            if config is None:
                return None

        name = config.get("name")
        uuid = config.get("uuid")

        theme = Theme(name, uuid)

        try:
            settings = config["settings"]
        except:
            return None

        self.set(theme, settings)


    def use(self, name):
        theme = None
        try:
            theme = self.themes[name]
        except:
            theme = self.load(name)
            self.themes[name] = theme

        if theme is None:
            return


    def set(self, theme, settings):
        for entry in settings:
            if not isinstance(entry, dict): 
                continue
            scope_str = entry.get("scope") or "global"
            scopes = scope_str.split(',')
            settings = entry.get("settings")
            if settings is not None:
                for scope in scopes:
                    theme.scopes[scope.strip()] = settings


    def parse(self, node):
        if node.tag == "dict":
            return self.parse_dict(node)
        elif node.tag == "array":
            return self.parse_array(node)
        elif node.tag == "string":
            return node.text

        return None


    def parse_dict(self, node):
        d = {}
        key = None
        value = None

        for child in node:
            if key is None:
                if child.tag != "key":  # key expected
                    return None
                key = child.text
            else:
                value = self.parse(child)
                if value is not None:
                    d[key] = value

                key = None
                value = None

        return d


    def parse_array(self, node):
        l = []
        for child in node:
            value = self.parse(child)
            if value is not None:
                l.append(value)

        return l
