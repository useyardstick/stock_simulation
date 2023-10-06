import numpy as np


class Field:
    def __init__(self, width_meters, height_meters, depth_meters, cell_resolution_meters):
        self.width = width_meters
        self.height = height_meters
        self.depth = depth_meters
        self.cell_resolution = cell_resolution_meters

        self.cells = np.zeros(
            (int(self.width / self.cell_resolution),
             int(self.height / self.cell_resolution),
             int(self.depth / self.cell_resolution)))


def main():
    field_width_meters = 100
    field_height_meters = 100
    field_depth_meters = 1
    cell_resolution_meters = 0.1

    field = Field(field_width_meters, field_height_meters,
                  field_depth_meters, cell_resolution_meters)

    print("Field cells: ", field.cells.shape)


if __name__ == "__main__":
    main()
