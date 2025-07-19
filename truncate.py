import random

class TauProtein:
    def __init__(self, id, isoform='4R'):
        self.id = id
        self.isoform = isoform
        self.phospho_sites = set()
        self.bound_state = 'bound'  # 'bound' or 'unbound'
        self.aggregation_state = 'monomer'  # 'monomer', 'oligomer', 'fibril'
        self.truncated = False
        self.truncation_site = None
        self.aggregation_sensitivity = 1  # increases after truncation
        self.history = []

    def phospho_random_site(self):
        site = f"S{random.randint(200, 450)}"
        self.phospho_sites.add(site)
        self.history.append(f"Phosphorylated at {site}")

    def unbind_microtubule(self):
        self.bound_state = 'unbound'
        self.history.append("Unbound from microtubule")

    def truncate(self, site='D421'):
        """
        Truncates the tau protein at a given site (default: D421).
        - Makes the protein aggregation-prone
        - Unbinds it from microtubules
        """
        if not self.truncated:
            self.truncated = True
            self.truncation_site = site
            self.aggregation_sensitivity *= 2
            self.history.append(f"Truncated at {site}")
            if self.bound_state == 'bound':
                self.unbind_microtubule()

    def maybe_truncate(self, threshold=4, chance=0.1):
        """
        Checks if the tau protein should truncate:
        - Only if not already truncated
        - If phospho site count >= threshold
        - With some random chance
        """
        if not self.truncated and len(self.phospho_sites) >= threshold:
            if random.random() < chance:
                self.truncate()

    def update_state(self):
        """
        Call this once per timestep:
        - Adds a new phospho site
        - Possibly triggers truncation
        """
        self.phospho_random_site()
        self.maybe_truncate()

# === Simulate ===

# Create a small population of tau proteins
tau_population = [TauProtein(id=i) for i in range(5)]

# Run simulation for 10 time steps
for t in range(10):
    for tau in tau_population:
        tau.update_state()

# Print results
for tau in tau_population:
    print(f"\nTau {tau.id} - Truncated: {tau.truncated}, Site: {tau.truncation_site}")
    for event in tau.history:
        print(f"  - {event}")
