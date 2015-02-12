"""A small program to parse my old website text and extract journal
entries. Then place them in html code for use in an updated website.
"""
import codecs
import iptcinfo
import jinja2
import re


def parse_journal_text(text_file):
    """Parse the text version of the journal entries and return a list
    of dicts (date, info, journal_entry). Journal_values are a list of
    paragraphs.
    """
    journal_list = []
    journal_entry = ""
    date = None
    new_entry = {}
    with codecs.open(text_file, 'r', 'utf_8') as fpt:

        # The start of each journal entry, date, and info is on a new line
        for line in fpt:
            line = line.strip()

            # The line after the date is the info line
            if date:
                new_entry['info'] = line

                # Reset date to write journal entries that come after
                date = None

            # The first thee chars in the date line are the months
            elif line[:3].lower() in ['apr', 'may', 'jun', 'jul',
                                      'aug', 'sep', 'oct', 'nov']:

                # End of the current entry, add journal entry
                new_entry['journal_entry'] = journal_entry

                # Don't append the first time as it is empty
                if len(new_entry) > 1:
                    journal_list.append(new_entry)

                # Reset values to prep for next entry
                date = line
                new_entry = {}
                new_entry['date'] = date
                journal_entry = []

            # The line is a journal entry
            else:
                if line:
                    journal_entry.append(line)

        # Write final entry
        new_entry['journal_entry'] = journal_entry
        journal_list.append(new_entry)

        # Reverse list, descending chronological order (April -> September)
        journal_list = journal_list[::-1]

        # month_first is None unless it is the first instance
        month_list = ['april', 'may', 'june',
                      'july', 'august', 'september']
        for entry in journal_list:
            month = entry['date'].lower().split()[0]
            if month in month_list:
                entry['month_first'] = month
                month_list.remove(month)
            else:
                entry['month_first'] = None

        return journal_list


def journal_html(journal):
    """Takes a list of dicts and returns a rendered HTML page as a
    string, for use on the new site."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('../jinja_templates'))
    template = env.get_template('journal_template')
    return template.render(journal)


def img_html(img_folder):
    """Generates the HTML for my image page using the images in the
    folder passed in as a string. Returns the HTML as a string.
    """
    env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('../jinja_templates'))
    template = env.get_template('photo_template')
    html = ''
    for number in xrange(1, num+1):
        html += (html_template % number)

    return html


def write_file(text, file_name):
    """Write the string to the file name."""
    with codecs.open(file_name, 'w', 'utf_8') as fpt:
        fpt.write(text)

# Create journal dict list
journal_list = parse_journal_text('thewalk.txt')

# Using the template, render the HTML to a string
journal_str = journal_html({'journal': journal_list})

# Write HTML to a file
write_file(journal_str, 'journal.html')
