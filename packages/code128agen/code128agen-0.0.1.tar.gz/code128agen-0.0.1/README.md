# Code128a Generator

A simple barcode generator (full python solution)

This library makes use of Pillow  to generate the barcode image, 
it also fully supports extended ASCII which I found most other libraries did not support except GNU barcode in raw mode.


### Installation
```bash
python -m pip install code128agen
```

### Usage
#### 
```python
from code128agen import generate_bar_widths, write_barcode_to_image_file, write_barcode_to_image

test_str_unicode = '12345678ÐEª2345FD'
bars = generate_bar_widths(test_str_unicode) # generates the bar widths for generating image.
pil_image = write_barcode_to_image(bars) # if you want to manipulation the image with PIL.
write_barcode_to_image_file(bars, 'test.png') # writes out file to specified file name.
```
