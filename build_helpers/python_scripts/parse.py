"""A small program to parse my old website text and extract journal
entries. Then place them in html code for use in an updated website.
"""
import codecs
import jinja2
import re


def parse_journal_text(text_file):
    """Parse the text version of the journal entries and return a list
    of dicts (date, info, journal_entry).
    """
    journal_list = []
    journal_entry = ""
    date = None
    new_entry = {}
    with codecs.open(text_file, 'r', 'utf_8') as fpt:

        # The start of each journal entry, date, and info is on a new line
        for line in fpt:

            # The line after the date is the info line
            if date:
                new_entry['info'] = re.sub(r'\s{2,}', ' ',
                                           line.replace('\n', ''))

                # Reset date to write journal entries that come after
                date = None

            # The first thee chars in the date line are the months
            elif line[:3].lower() in ['apr', 'may', 'jun', 'jul',
                                      'aug', 'sep', 'oct', 'nov']:

                # End of the current entry, add journal entry
                new_entry['journal_entry'] = re.sub(
                    r'\s{2,}', ' ', journal_entry.replace('\n', ''))

                # Don't append the first time as it is empty
                if len(new_entry) > 1:
                    journal_list.append(new_entry)

                # Reset values to prep for next entry
                date = line
                new_entry = {}
                new_entry['date'] = re.sub(r'\s{2,}', ' ',
                                           date.replace('\n', ''))
                journal_entry = ""

            # The line is a journal entry
            else:
                journal_entry += line

        # Write final entry
        new_entry['journal_entry'] = re.sub(r'\s{2,}', ' ',
                                            journal_entry.replace('\n', ''))
        journal_list.append(new_entry)
        return journal_list


def journal_html(journal):
    """Takes a list of dicts and returns a rendered HTML page as a
    string, for use on the new site."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('../jinja_templates'))
    template = env.get_template('journal_template.html')
    return template.render(journal)


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
journal_list = parse_journal_text('thewalk.txt')
journal_str = journal_html({'journal': journal_list})
write_file(journal_str, 'journal.html')
