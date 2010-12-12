./src/main.py --generate "/Users/hortont/Documents/School/RPI/2010 (Senior)/Computational Vision/final project/focus/$1" -o $1.cty
./src/main.py --infinite-focus $1.cty -o $1-inf.jpg
./src/main.py --anaglyph $1.cty -o $1-ana.png