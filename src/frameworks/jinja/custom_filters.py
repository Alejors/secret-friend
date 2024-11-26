import re


def _regex_match(text, pattern):
  return bool(re.search(pattern, text))

custom_methods = {
  "regex_match": _regex_match
}