# covid19_hoaxbust

These scripts help in translating English posters which do hoax busting to
regional languages as an effort by the community group "Indian Scientists
Response to COVID19". The script takes a csv file in a particular format which
has stored translations for all the different languages and questions.

`modify_poster` is a class which is able to insert the required translated
strings at the right places.

The fonts and the fontsizes are stored in the `Master_config.yaml` file. The
placement of the various strings in the file are listed for each of the
questions in the file `language/placements_language.txt`.

```
python modify_poster.py language
```

It will take an example poster and then put the strings extracted from the csv
file into `Sample_images/000xx.jpg` at the locations specified in the
placements file.

You need to have the correct fonts in the "Noto/" folder. Download these fonts
from https://www.google.com/get/noto
