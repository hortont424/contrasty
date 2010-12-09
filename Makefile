.PHONY: create infinite

create:
	./src/main.py --generate "/Users/hortont/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/4" -o 4.cty

infinite:
	./src/main.py --infinite-focus 4.cty -o 4-inf.jpg