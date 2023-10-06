import numpy as np
import matplotlib.pyplot as plt


class Field:
    def __init__(self, width_meters, height_meters, depth_meters, cell_resolution_meters):
        self.width = width_meters  # width is the X axis
        self.height = height_meters  # height is the Y axis
        self.depth = depth_meters  # depth is the Z axis
        self.cell_resolution = cell_resolution_meters

        self.cells = np.zeros(
            (int(self.width / self.cell_resolution),
             int(self.height / self.cell_resolution),
             int(self.depth / self.cell_resolution)))

        self.rng = np.random.default_rng(
            729572037593715194)  # The integer is a seed

    def add_gold_nuggets(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                location = self.rng.integers(low=0, high=10, size=3)
                cell_x = int(x / self.cell_resolution) + location[0]
                cell_y = int(y / self.cell_resolution) + location[1]
                cell_z = location[2]
                self.cells[cell_x, cell_y, cell_z] = 1.0

    def save_as_image(self, filename):
        # sum over depth dimension
        array = np.sum(self.cells, 2)

        # normalize to 0-255
        array *= 255.0/np.max(array)

        # create 3 channels and convert to uint8
        as_image = np.dstack([array]*3)
        as_image = as_image.astype(np.uint8)

        plt.imsave(filename, as_image)

    def sample(self, num_samples):
        x_coords = self.rng.integers(
            low=0, high=self.cells.shape[0], size=num_samples)
        y_coords = self.rng.integers(
            low=0, high=self.cells.shape[1], size=num_samples)
        z_coords = self.rng.integers(
            low=0, high=self.cells.shape[2], size=num_samples)

        sample_sites = np.stack((x_coords, y_coords, z_coords), axis=1)
        # print("Sample sites: ", sample_sites.shape)

        sample_values = self.cells[x_coords, y_coords, z_coords]
        # print("Sample values: ", sample_values)
        return sample_values

    def estimate_stock(self, num_samples):
        samples = self.sample(num_samples)
        total_gold_mass = np.sum(samples)
        total_gold_volume = num_samples * 0.001
        gold_density = total_gold_mass / total_gold_volume
        total_gold_stock = gold_density * self.width * self.height * self.depth
        return total_gold_stock

    def histogram(self, num_samples, num_runs):
        estimates = [self.estimate_stock(num_samples)
                     for i in range(num_runs)]

        counts, bins = np.histogram(estimates, bins=100)
        counts = counts / num_runs

        plt.figure(figsize=(8, 4))
        plt.hist(bins[:-1], bins, weights=counts)
        plt.axvline(x=10000, color='r', label='Truth')
        plt.xlabel("Estimated Gold Stock (kg)")
        plt.ylabel("Probability")
        plt.title("Estimated Gold Stock")
        # plt.show()
        plt.savefig("gold_stock_histogram.png")


def main():
    field_width_meters = 100
    field_height_meters = 100
    field_depth_meters = 1
    cell_resolution_meters = 0.1

    field = Field(field_width_meters, field_height_meters,
                  field_depth_meters, cell_resolution_meters)

    print("Field cells: ", field.cells.shape)
    field.add_gold_nuggets()
    field.save_as_image("gold_nuggets.png")

    field.histogram(100, 1000)


if __name__ == "__main__":
    main()
