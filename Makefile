.PHONY: create infinite

usage:
	echo "make createN\nmake infiniteN"

create1:
	./src/main.py --generate "/Users/hortont/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/1" -o 1.cty

infinite1:
	./src/main.py --infinite-focus 1.cty -o 1-inf.jpg

create4:
	./src/main.py --generate "/Users/hortont/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/4" -o 4.cty

infinite4:
	./src/main.py --infinite-focus 4.cty -o 4-inf.jpg

view4:
	./src/main.py --view 4.cty