echo "\n--------Extracting Training Slices--------\n"
python sliceExtraction.py
echo "\n--------Extracting Validation Slices------\n"
python sliceExtraction.py -v
echo "\n--------Converting Training slices for Lua compatibility and Data augmentation------\n"
th sliceConverter.lua
echo "\n--------Converting Validation slices for Lua compatibility--------------------------\n"
th sliceConverter.lua -mode validation
