import sys
import re

xml = open(sys.argv[1], "r")
terms = open("terms.txt", "w")
emails = open("emails.txt", "w")
dates = open("dates.txt", "w")
recs = open("recs.txt", "w")

def format_text(txt):
    return txt.replace('&amp;','&').replace('&#10;','\n').replace('&lt;','<').replace('&gt;','>')\
           .replace('&apos;',"'").replace('&quot;','"').replace('&',' ').replace(',',' ').replace('.',' ')\
           .replace('<',' ').replace('>',' ').replace("'" ,' ').replace('"',' ').replace(':',' ').replace(';',' ')\
           .replace('/',' ').replace('?',' ').replace("!",' ').replace('|',' ').replace("\\",' ').replace('(',' ')\
           .replace(')',' ').replace('%',' ').replace('=',' ').replace('$',' ').replace('+',' ').replace('@',' ')\
           .replace('#',' ').replace('^',' ').replace('*',' ').replace('{',' ').replace('}',' ').replace('[',' ')\
           .replace(']',' ').replace('`',' ').replace('~',' ').replace('=',' ').lower()
def write_to_terms(row, subject, body):
    if subject:
        subject = format_text(subject).split()
        for x in subject:
            if not(len(x) <= 2):
                terms.write("s-{}:{}\n".format(x.lower(),row))
    if body:
        body = format_text(body).split()
        for x in body:
            if not(len(x) <= 2):
                terms.write("b-{}:{}\n".format(x.lower(),row))


def write_to_emails(row, frm, to, cc, bcc):
    """
    One line per email (i.e. frm, to, produce 2 lines)
    All emails are made lowercase
    """

    if frm:
        frm = frm.split(",")
        for x in frm:
            emails.write("from-{}:{}\n".format(x.lower(), row))
    if to:
        to = to.split(",")
        for x in to:
            emails.write("to-{}:{}\n".format(x.lower(), row))
    if cc:
        cc = cc.split(",")
        for x in cc:
            emails.write("cc-{}:{}\n".format(x.lower(), row))
    if bcc:
        bcc = bcc.split(",")
        for x in bcc:
            emails.write("bcc-{}:{}\n".format(x.lower(), row))


def write_to_dates(row, date):
    if date and len(date):
        dates.write("{}:{}\n".format(date, row))


def write_to_recs(row, line):
    if line:
        recs.write("{}:{}".format(row, line))


def main():
    for l in xml:
        if re.match('<mail>.*</mail>', l):
            row = re.search("<row>(.*)</row>", l).group(1)
            date = re.search("<date>(.*)</date>", l).group(1)
            frm = re.search("<from>(.*)</from>", l).group(1)
            to = re.search("<to>(.*)</to>", l).group(1)
            bcc = re.search("<bcc>(.*)</bcc>", l).group(1)
            cc = re.search("<cc>(.*)</cc>", l).group(1)
            body = re.search("<body>(.*)</body>", l).group(1)
            subj = re.search("<subj>(.*)</subj>", l).group(1)

            write_to_terms(row, subj, body)
            write_to_emails(row, frm, to, bcc, cc)
            write_to_dates(row, date)
            write_to_recs(row, l)


if __name__ == "__main__":
    main()
