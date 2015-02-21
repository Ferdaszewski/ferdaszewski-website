# The Walk
## A website documenting Joshua Ferdaszewski's 2004 thru-hike of the PCT

The original size was built in 2004 during my thru-hike of the Pacific Crest Trail. I wanted to keep the original content (photos and journal entries) and update the format. I created Jinja2 templates for each of the pages on the site and wrote a pythons script to parse the original journal entry text and load it into the new template. For the photo page, I read the EXIF/IPTC data from the jpg files and created caption and alt tag text programmatically. The photos use JavaScript to 'lazy load' on scroll.

You can view the live site at:
[http://pct.ferdaszewski.com]