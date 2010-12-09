.PHONY: create infinite

create:
	./src/main.py --generate "/Users/hortont/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/3" -o 3.cty

infinite:
	./src/main.py --infinite-focus 3.cty -o 3-inf.jpg