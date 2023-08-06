# -*- coding: UTF-8 -*-
"""
Unique syntax for formatting sample CLI commands
"""
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


class CmdExtension(Extension):
    def extendMarkdown(self, md, config):
        self.md = md
        MD_RE = r'\$\w(.*?)\$'
        md_pattern = CmdInlineProcessor(MD_RE)
        md_pattern.md = md
        md.inlinePatterns.register(md_pattern, 'cmd', 70)


class CmdInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        if m.group(0).strip():
            label = m.group(0).strip()[1:-1] # slice off the leading and trailing $
            cmd = etree.Element('code')
            cmd.text = label
            cmd.set('class', 'command')
        else:
            cmd = ''
        return cmd, m.start(0), m.end(0)


def makeExtension(**kwargs):
    return CmdExtension(**kwargs)
