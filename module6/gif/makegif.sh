# Thanks chatgpt
rm -rf output.gif palette.png
ffmpeg -framerate 5 -i tree%03d.png -vf "scale=320:-1:flags=lanczos,palettegen" -y palette.png
ffmpeg -framerate 5 -i tree%03d.png -i palette.png -lavfi "scale=320:-1:flags=lanczos [x]; [x][1:v] paletteuse" -y output.gif

