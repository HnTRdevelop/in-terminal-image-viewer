# Terminal image viewer!

## View your images in terminal!
This is a simple python script that output images in terminal.

## Usage:

```
python3 main.py [OPTIONS...] [IMAGES-PATHS...]
```

You can specify as much images paths, as you want, if you do so, you will receive images one by one in order that you specified.

#### Examples:
```
python3 main.py -b test.png
```
```
python3 main.py 1.png 2.jpg 3.jpeg
```
```
python3 main.py image.jpeg
```

## Options:  

-b, --bypass-vertical  
bypass terminal vertical character limit.

-c, --character  [character]  
set your own character for pixels.
