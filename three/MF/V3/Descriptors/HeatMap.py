class HeatMap:

    """
     Heat map descriptor.
    """
    def __init__(self, count: int, min: float, max: float, median: float, mean: float, stddev: float, outlierDistance: float):
        # The of points included in the point-to-mesh statistics.
        self.count = count
        # The minimum point-to-mesh distance.
        self.min = min
        # The maximum point-to-mesh distance.
        self.max = max
        # The median point-to-mesh distance.
        self.median = median
        # The mean point-to-mesh distance.
        self.mean = mean
        # The standard deviation of the point-to-mesh distances.
        self.stddev = stddev
        # The point-to-mesh outlier distance.  Distances greater than this value are excluded from the statistics.
        self.outlierDistance = outlierDistance


