# Photobook

## Install

    pip install photobook

## Notes

Crooping a image to get the larger square on the middle

    convert <source> -gravity center -crop `identify -format "%[fx:min(w,h)]x%[fx:min(w,h)]+0+0" rose:` +repage <cible>


