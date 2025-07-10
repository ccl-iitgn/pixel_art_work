from Tiles import get_tiles
import pulp
import itertools


class PixelModel:
    def __init__(self, rows, cols, tile_placements, grid_face_data):
        self._rows = rows
        self._cols = cols
        self.default_tiles = get_tiles()
        self.tile_placement = tile_placements
        self.grid_face_data = grid_face_data
        self._milp_model = pulp.LpProblem("TilesPlacement", pulp.LpMinimize)
        self._variables = self._create_variables()
        self._create_objectives()
        self._create_constraints()

    def _create_variables(self):
        variables = dict()

        variables['tile_at_place'] = pulp.LpVariable.dicts(
            "tile_at_place",
            (tile_key for tile_key in self.tile_placement.keys()),
            cat="Binary"
        )
        return variables

    def _create_objectives(self) -> None:
        diff_brightness_numbers = pulp.lpSum(
            self._variables["tile_at_place"][tile_key] * (
                    self.tile_placement[tile_key]['diff'] * (
                1 if self.grid_face_data[tile_key[1][0]][tile_key[1][1]] is None else
                self.grid_face_data[tile_key[1][0]][tile_key[1][1]]))
            for tile_key in self.tile_placement.keys()
        )

        self._milp_model.setObjective(diff_brightness_numbers)

    def _create_constraints(self):
        for x, y in itertools.product(range(self._rows), range(self._cols)):
            covered_block = pulp.lpSum(
                self._variables["tile_at_place"][tile_key]
                for tile_key, data in self.tile_placement.items()
                if tile_key[1] == (x, y)
            )
            self._milp_model.addConstraint(
                covered_block == 1,
                f"cover_field_once_{x}_{y}"
            )
        for tile_id in range(1, 301):
            count_tile_usage = pulp.lpSum(
                self._variables["tile_at_place"][tile_key]
                for tile_key in self.tile_placement.keys()
                if tile_key[0] == tile_id
            )
            self._milp_model.addConstraint(
                count_tile_usage == 1,
                f"use_tile_once_{tile_id}"
            )

    def solve(self) -> list:
        self._milp_model.solve(
            pulp.PULP_CBC_CMD(
                msg=True,
                mip=True
            )
        )
        print(f'Solved model with status {self._milp_model.status}')
        diff = 0
        solution = [[None for i in range(self._cols)] for _ in range(self._rows)]
        for tile_key, value in self.tile_placement.items():
            if pulp.value(self._variables["tile_at_place"][tile_key]) == 1:
                diff += value["diff"]
                solution[tile_key[1][0]][tile_key[1][1]] = value
        print(diff)
        return solution
