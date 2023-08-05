# Regex Cleaner

This is a simple python package that can be used to clean a verbose regex pattern of the comments and new lines and return the basic underlying pattern.

## Installation

```bash
python -m pip install regex-cleaner
```

## Usage

To clean a regex pattern, simply pass the verbose pattern string to the function `clean_regex`.

```python
from regex_cleaner import clean_regex

pattern = r"""
    \w\d{3} # Matches any letter followed by 3 digits.
"""
cleaned_regex = clean_regex(pattern)

print(cleaned_regex)
```

```bash
\w\d{3}
```

It should be noted that the pattern is cleaned by removing all comments from the string, then removing any whitespace left in the pattern.
*This means that if you are using whitespace to represent space characters in your pattern they will be trimmed out.*

```python
import regex_cleaner

pattern = r"""
    \w* # Any letter repeated zero or more times.
    [. ] # Full stop followed by a space.
"""

cleaned_pattern = regex_cleaner.clean_regex(pattern)

print(cleaned_pattern)
```

```bash
\w*[.]
```

## Testing

Tests can be run using `pytest ` or `tox`. To test, clone down the repository and from the root of the repository do either

```bash
python -m pytest
```

or

```bash
python -m tox
```
