"""A short script to parse my old website text and extract journal
entries. Then place them in html code for use in an updated website.
"""
import re
import pystache
import codecs


def text_parse(text_file):
    """Parse the text version of the journal entries and return a list of
    tuples (date, info, journal_entry).
    """
    journal_list = []
    journal_entry = ""
    date = None
    new_entry = []
    with codecs.open(text_file, 'r', 'UTF-8') as f:

        # The start of each journal entry, date, and info is on a new line
        for line in f:
            # The line after the date is the info line
            if date:
                new_entry.append(line)

                # Reset date to write journal entries that come after
                date = None

            # The first thee chars in the date line are the months
            elif line[:3].lower() in ['apr', 'may', 'jun', 'jul',
                                      'aug', 'sep', 'oct', 'nov']:
                # End of the current entry, add journal entry
                new_entry.append(journal_entry)

                # Remove extra spaces and line brakes
                new_entry = tuple([re.sub(r'\s{2,}', ' ', im.replace('\n', ''))
                                  for im in new_entry])

                # Don't append the first time as it is empty
                if new_entry[0]:
                    journal_list.append(new_entry)

                # Reset values to prep for next entry
                date = line
                new_entry = [date]
                journal_entry = ""

            # The line is a journal entry
            else:
                journal_entry += line

        # Write final entry
        new_entry.append(journal_entry)
        new_entry = tuple([re.sub(r'\s{2,}', ' ', im.replace('\n', ''))
                          for im in new_entry])
        journal_list.append(new_entry)

        return journal_list

def img_html(num):
    """Simple function to generate html for my image page."""
    html_template = '<div class="img-wrapper row">\n  <img src="img/PCT-Ferd-%.3d.jpg" class="img-responsive col-xs-12">\n</div>\n'
    html = ''
    for number in xrange(1, num+1):
        html += (html_template % number)

    return html

journal = text_parse("thewalk.txt")
for entry in journal:
    print unicode(entry)
    print '+' * 100
print len(journal)

with open("img-html.tmp", 'w') as f:
    f.write(img_html(447))
