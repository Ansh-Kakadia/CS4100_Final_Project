import math
import random
from src.data.item import FashionItem
from src.optimizer import energy
from src.optimizer.neighbor import NeighborFinder

def run(
    initial_fit: dict[str, FashionItem],
    finder: NeighborFinder,
    start: float = 1.0,
    min: float = 0.001,
    cooling: float = 0.995,
    max_iters: int = 2000,
) -> tuple[dict[str, FashionItem], list[float]]: # returns tuple that contains a dict and list of floats
    
    current = initial_fit
    current_energy = energy.compute(current)
    
    best = current
    best_energy = current_energy
    
    history = [current_energy]
    t = start
    
    for i in range(max_iters):
        if t < min:
            break
        
        candidate = finder.get_neighbors(current)
        candidate_energy = energy.compute(candidate)
        
        delta = candidate_energy - current_energy
        if delta < 0 or random.random() < math.exp(-delta / t):
            current = candidate
            current_energy = candidate_energy
            
            if current_energy < best_energy:
                best = current
                best_energy = current_energy
        
        history.append(current_energy)
        t *= cooling
        
    return best, history