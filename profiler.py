import cProfile
import pstats
from trainer import Trainer

cProfile.run("Trainer().train()", "restats")
p = pstats.Stats("restats")
p.sort_stats("cumulative").print_stats(30)
