"""A small program to parse my old website text and extract journal
entries. Then place them in html code for use in an updated website.
"""
import codecs
import jinja2
import re


def parse_journal_text(text_file):
    """Parse the text version of the journal entries and return a list
    of tuples (date, info, journal_entry).
    """
    journal_list = []
    journal_entry = ""
    date = None
    new_entry = []
    with codecs.open(text_file, 'r', 'utf_8') as fpt:

        # The start of each journal entry, date, and info is on a new line
        for line in fpt:

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


def gen_img_html(num):
    """Simple method to generate HTML for my image page. Returns the
    HTML as a string.
    """
    html_template = ('<div class="img-wrapper row">\n  ' +
                     '<img src="img/PCT-Ferd-%.3d.jpg" ' +
                     'class="img-responsive col-xs-12">\n</div>\n')
    html = ''
    for number in xrange(1, num+1):
        html += (html_template % number)

    return html


def write_file(text, file_name):
    """Write the string to the file name."""
    with codecs.open(file_name, 'w', 'utf_8') as fpt:
        fpt.write(text)

# Print result of journal text parse
journal = parse_journal_text('thewalk.txt')
journal_str = u''
for entry in journal:
    journal_str += ('\n'.join(entry) + '\n\n')
write_file(journal_str, 'journal.tmp')
