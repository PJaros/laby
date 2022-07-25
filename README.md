# Laby

I'm collecting here some of my current efforts to create my labyrinth generators. All of them have only a single
way from the top left to the bottom right.

`laby/python/relational/relational.py` is currently the most advanced programm is written in Python which features bridges, calculates mutliple labyrinths
and chooses the one with the longes solution path. The labyrinth is drawn with the turtle library, allows to be
traversed with a turtle (arrow keys) and allows to show the sollution ('s' key).

`laby/python/laby/arr_1d.py` is a reimplementationf of `relational.py` which replaces the hashmap data with a 1-dimensional array. I build it as a prototype
for the rust version.

`laby/rust/macroquad` is the rust version of `arr_1d.py` with marcoquad-crate as a output.

Measured on my T550 Lenovo Laptop with a 331 * 201 sized labyrinth:

- `arr_1d.py` uses 216.8 ms
- `macroquad` uses 3.17 ms 
