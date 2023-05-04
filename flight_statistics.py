import pstats
from pstats import SortKey
p = pstats.Stats('yeager.stats')
p.strip_dirs().sort_stats(0).print_stats()