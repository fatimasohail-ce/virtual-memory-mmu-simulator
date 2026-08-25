import json
import math
from collections import OrderedDict

class MMUSimulator:
    def __init__(self, config_file, algorithm='FIFO', ram_frames=None):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.page_size = self.config['page_size_bytes']
        # If we provide ram_frames manually, use it; otherwise use config
        if ram_frames:
            self.max_frames = ram_frames
        else:
            self.max_frames = (self.config['ram_size_kb'] * 1024) // self.page_size
            
        self.algorithm = algorithm
        self.shift = int(math.log2(self.page_size))
        
        self.ram = OrderedDict() # Used for FIFO and LRU
        self.page_faults = 0
        self.trace_data = [] # To store trace for OPT look-ahead

    def load_trace(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) == 2:
                    self.trace_data.append((int(parts[0], 16) >> self.shift, parts[1]))

    def run(self):
        for i, (vpn, op) in enumerate(self.trace_data):
            if vpn not in self.ram:
                self.page_faults += 1
                if len(self.ram) >= self.max_frames:
                    self.evict(i)
                self.ram[vpn] = True
            elif self.algorithm == 'LRU':
                self.ram.move_to_end(vpn)
        return self.page_faults

    def evict(self, current_index):
        if self.algorithm == 'FIFO' or self.algorithm == 'LRU':
            self.ram.popitem(last=False)
        elif self.algorithm == 'OPT':
            # Optimal: Look ahead to see which page is used furthest in the future
            furthest_index = -1
            victim_vpn = None
            for vpn in self.ram:
                try:
                    next_usage = next(j for j in range(current_index + 1, len(self.trace_data)) if self.trace_data[j][0] == vpn)
                except StopIteration:
                    next_usage = float('inf')
                
                if next_usage > furthest_index:
                    furthest_index = next_usage
                    victim_vpn = vpn
            del self.ram[victim_vpn]

# --- EXECUTION BLOCK ---
trace_file = 'trace.txt'
config_file = 'config.json'

print(f"{'Algorithm':<12} | {'Frames':<8} | {'Total Faults':<12}")
print("-" * 40)

# Run for 3 Algorithms
for algo in ['FIFO', 'LRU', 'OPT']:
    sim = MMUSimulator(config_file, algorithm=algo)
    sim.load_trace(trace_file)
    faults = sim.run()
    print(f"{algo:<12} | {sim.max_frames:<8} | {faults:<12}")

# --- BELADY'S ANOMALY TEST ---
print("\nTesting for Belady's Anomaly (FIFO)...")
for f_count in [3, 4]:
    sim = MMUSimulator(config_file, algorithm='FIFO', ram_frames=f_count)
    sim.load_trace(trace_file)
    print(f"FIFO with {f_count} frames: {sim.run()} faults")