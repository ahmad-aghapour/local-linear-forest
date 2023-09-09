import random
from typing import List
from typing import List, Dict
from typing import List, Set
import random

class SamplingOptions:
    def __init__(self, samples_per_cluster: int = 0, sample_clusters: List[int] = None):
        self.num_samples_per_cluster = samples_per_cluster
        
        if sample_clusters is None:
            self.clusters = []
            return

        # Map the provided clusters to IDs in the range 0 ... num_clusters.
        cluster_ids: Dict[int, int] = {}
        for cluster in sample_clusters:
            if cluster not in cluster_ids:
                cluster_id = len(cluster_ids)
                cluster_ids[cluster] = cluster_id

        # Populate the index of each cluster ID with the samples it contains.
        self.clusters = [[] for _ in range(len(cluster_ids))]
        for sample, cluster in enumerate(sample_clusters):
            cluster_id = cluster_ids[cluster]
            self.clusters[cluster_id].append(sample)

    def get_samples_per_cluster(self) -> int:
        return self.num_samples_per_cluster

    def get_clusters(self) -> List[List[int]]:
        return self.clusters


class RandomSampler:

    def __init__(self, seed: int, options: SamplingOptions):
        self.options = options
        self.random_number_generator = random.Random(seed)
        random.seed(seed)

    def sample_clusters(self, num_rows: int, sample_fraction: float) -> List[int]:
        samples = []
        if not self.options.get_clusters():
            samples = self.sample(num_rows, sample_fraction)
        else:
            num_samples = len(self.options.get_clusters())
            samples = self.sample(num_samples, sample_fraction)
        return samples

    def sample(self, num_samples: int, sample_fraction: float) -> List[int]:
        num_samples_inbag = int(num_samples * sample_fraction)
        return self.shuffle_and_split(num_samples, num_samples_inbag)

    def shuffle_and_split(self, num_samples: int, num_samples_inbag: int) -> List[int]:
        samples = list(range(num_samples))
        random.shuffle(samples)
        return samples[:num_samples_inbag]

    def subsample(self, samples: List[int], sample_fraction: float) -> List[int]:
        shuffled_sample = samples.copy()
        random.shuffle(shuffled_sample)

        subsample_size = int(len(samples) * sample_fraction)
        return shuffled_sample[:subsample_size]

    def subsample_with_size(self, samples: List[int], subsample_size: int) -> List[int]:
        shuffled_sample = samples.copy()
        random.shuffle(shuffled_sample)
        return shuffled_sample[:subsample_size]

    def subsample_and_oob(self, samples: List[int], sample_fraction: float) -> (List[int], List[int]):
        shuffled_sample = samples.copy()
        random.shuffle(shuffled_sample)

        subsample_size = int(len(samples) * sample_fraction)
        subsamples = shuffled_sample[:subsample_size]
        oob_samples = shuffled_sample[subsample_size:]
        
        return subsamples, oob_samples



    def sample_from_clusters(self, clusters: List[int]) -> List[int]:
        samples = []
        if not self.options.get_clusters():
            samples = clusters.copy()
        else:
            samples_by_cluster = self.options.get_clusters()
            for cluster in clusters:
                cluster_samples = samples_by_cluster[cluster]

                # Draw samples_per_cluster observations from each cluster.
                # If the cluster is smaller than the samples_per_cluster parameter,
                # just use the whole cluster.
                if len(cluster_samples) <= self.options.get_samples_per_cluster():
                    samples.extend(cluster_samples)
                else:
                    subsamples = self.subsample_with_size(cluster_samples, self.options.get_samples_per_cluster())
                    samples.extend(subsamples)
        return samples

    def get_samples_in_clusters(self, clusters: List[int]) -> List[int]:
        samples = []
        if not self.options.get_clusters():
            samples = clusters.copy()
        else:
            for cluster in clusters:
                cluster_samples = self.options.get_clusters()[cluster]
                samples.extend(cluster_samples)
        return samples



   




    def draw(self, result, max_value, skip, num_samples):
        if num_samples < max_value / 10:
            self.draw_simple(result, max_value, skip, num_samples)
        else:
            self.draw_fisher_yates(result, max_value, skip, num_samples)

    def draw_simple(self, result, max_value, skip, num_samples):
        result.clear()

        # Set all to not selected
        temp = [False] * max_value

        for i in range(num_samples):
            draw = None
            while True:
                draw = self.random_number_generator.randint(0, max_value - 1 - len(skip))
                for skip_value in sorted(skip):
                    if draw >= skip_value:
                        draw += 1
                if not temp[draw]:
                    break

            temp[draw] = True
            result.append(draw)

    def draw_fisher_yates(self, result, max_value, skip, num_samples):
        # Populate result list with 0,...,max_value-1
        result.clear()
        result.extend(range(max_value))

        # Remove values that are to be skipped
        for i in sorted(skip, reverse=True):
            result.pop(i)

        # Draw without replacement using Fisher Yates algorithm
        for i in range(num_samples):
            j = i + int(self.random_number_generator.uniform(0, 1) * (max_value - len(skip) - i))
            result[i], result[j] = result[j], result[i]

        del result[num_samples:]

    def sample_poisson(self, mean):
        return self.random_number_generator.poisson(mean)