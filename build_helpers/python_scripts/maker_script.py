"""A small program to parse my old website text and extract journal
entries. Then place them in html code for use in an updated website.
"""
import codecs
from iptcinfo import IPTCInfo
import jinja2
import os
from PIL import Image


# Module contestants
IMG_TYPES = ['jpg', 'jpeg', 'tiff', 'gif']
IPTC_KEYS = {'tags': 25, 'caption': 120}


def journal_html(text_file):
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

        return render_html({'journal': journal_list}, 'journal_template')


def render_html(html, template):
    """Render out the HTML string and return it."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('../jinja_templates'))
    template = env.get_template(template)
    return template.render(html)


def img_html(img_folder):
    """Generates the HTML for my image page using the images in the
    folder passed in as a string. Returns the HTML as a string.
    """
    img_list = [f for f in os.listdir(img_folder) if
                os.path.isfile(os.path.join(img_folder, f)) and
                f.split('.')[-1].lower() in IMG_TYPES]
    img_list.sort()

    img_info_list = []
    for img in img_list:
        img_info = {}

        # Get IPTC info from file
        with open(os.path.join(img_folder, img)) as img_file:
            iptc_info = IPTCInfo(img_file)
            for tag, iptc_tag in IPTC_KEYS.items():
                img_info[tag] = iptc_info.data[iptc_tag]

        # Get size of file in pixels
        width, height = Image.open(os.path.join(img_folder, img)).size
        img_info['width'] = width
        img_info['height'] = height
        img_info_list.append(img_info)

    # month_first is None unless it is the first instance
    month_list = ['may', 'june', 'july', 'august', 'september']
    for entry in img_info_list:

        # tags is a list with 'MM 2004' and 'PCT' only
        entry['tags'].remove('PCT')
        month = entry['tags'][0].split()[0].lower()

        if month in month_list:
            entry['month_first'] = month
            month_list.remove(month)
        else:
            entry['month_first'] = None

    images = zip(img_list, img_info_list)
    return render_html({'images': images}, 'photo_template')


def write_file(text, file_name):
    """Write the string to the file name."""
    with codecs.open(file_name, 'w', 'utf_8') as fpt:
        fpt.write(text)


if __name__ == '__main__':
    # Create journal page and write to HTML file
    write_file(journal_html('thewalk.txt'), '../../web/journal.html')

    # Create photo page and write to HTML file
    write_file(img_html('../../web/assets/img/pct'), '../../web/photos.html')

    # Create index page and write to HTML file
    write_file(render_html({}, 'index_template'), '../../web/index.html')

    # Create about page and write to HTML file
    write_file(render_html({}, 'about_template'), '../../web/about.html')
