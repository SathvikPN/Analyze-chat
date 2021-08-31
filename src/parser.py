import re
import pandas as pd
import numpy as np

from src.configurations import LANGUAGE, PATTERN
from src.emojis import EMOJI, DEMOJI, CLEANER

# Pattern Objects 
emoji_pattern = re.compile('|'.join(sorted([re.escape(emo) for emo in EMOJI], key=len, reverse=True)))
demoji_pattern = re.compile('|'.join(DEMOJI))
cleaner_pattern = re.compile('|'.join([re.escape(c) for c in CLEANER]))
