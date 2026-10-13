#!/usr/bin/env python3
"""Fetch only a public Scholar profile's all-time metrics; fail without overwriting."""

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


USER_AGENT = "PersonalScholarStats/1.0"
METRICS = {"Citations": "citations", "h-index": "h_index", "i10-index": "i10_index"}


class MetricsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.table_depth = 0
        self.in_cell = False
        self.cells = []
        self.text = []
        self.metrics = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "table" and (self.table_depth or attributes.get("id") == "gsc_rsb_st"):
            self.table_depth += 1
        if self.table_depth and tag == "tr":
            self.cells = []
        if self.table_depth and tag == "td":
            self.in_cell = True
            self.text = []

    def handle_data(self, data):
        if self.in_cell:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.in_cell:
            self.cells.append("".join(self.text).strip())
            self.in_cell = False
        if tag == "tr" and self.table_depth and self.cells:
            label = self.cells[0]
            if label in METRICS:
                key = METRICS[label]
                if key in self.metrics or len(self.cells) != 3:
                    raise ValueError("Unexpected or duplicate Scholar metric row")
                value = self.cells[1].replace(",", "").replace("\xa0", "").replace(" ", "")
                if not re.fullmatch(r"[0-9]+", value):
                    raise ValueError("Scholar metric is not a number")
                self.metrics[key] = int(value)
        if tag == "table" and self.table_depth:
            self.table_depth -= 1


def parse_metrics(html):
    parser = MetricsParser()
    parser.feed(html)
    metrics = parser.metrics
    if set(metrics) != set(METRICS.values()):
        raise ValueError("Scholar metrics missing (blocked request or changed page)")
    if metrics["h_index"] ** 2 > metrics["citations"] or metrics["i10_index"] * 10 > metrics["citations"]:
        raise ValueError("Inconsistent Scholar metrics")
    return metrics


def robots_allows_profile(robots, url):
    # Use longest-match precedence, including Google's query-string rules.
    groups = []
    agents, rules = [], []
    for line in robots.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.lower())
        elif key in ("allow", "disallow") and agents and value:
            rules.append((key == "allow", value))
    groups.append((agents, rules))
    specific = [r for a, r in groups if any(x != "*" and x in USER_AGENT.lower() for x in a)]
    selected = specific or [r for a, r in groups if "*" in a]
    if not selected:
        raise ValueError("No applicable robots.txt group")
    parts = urlsplit(url)
    target = parts.path + ("?" + parts.query if parts.query else "")
    matches = []
    for rules in selected:
        for allow, pattern in rules:
            anchor = pattern.endswith("$")
            pattern = pattern[:-1] if anchor else pattern
            expression = "^" + ".*".join(re.escape(p) for p in pattern.split("*")) + ("$" if anchor else "")
            if re.search(expression, target):
                matches.append((len(pattern.replace("*", "")), allow))
    return max(matches)[1] if matches else True


def read_url(url):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en"})
    with urlopen(request, timeout=25) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read(2_000_000).decode(charset)


def update(author_id, output):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", author_id):
        raise ValueError("Invalid Scholar author ID")
    url = "https://scholar.google.com/citations?user=" + author_id + "&hl=en"
    robots = read_url("https://scholar.google.com/robots.txt")
    if not robots_allows_profile(robots, url):
        raise ValueError("Profile fetching is disallowed by robots.txt")
    metrics = parse_metrics(read_url(url))
    result = {
        "schema_version": 1,
        "author_id": author_id,
        "source": url,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        **metrics,
    }
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)
    return result


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("--author-id", required=True)
    argument_parser.add_argument("--output", required=True)
    arguments = argument_parser.parse_args()
    try:
        data = update(arguments.author_id, arguments.output)
        print("Scholar metrics refreshed:", data["citations"], data["h_index"], data["i10_index"])
    except Exception as error:
        argument_parser.exit(1, "Scholar refresh failed; previous data preserved: " + str(error) + "\n")
