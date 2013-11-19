#!/usr/bin/env python
import os
import sys
import re

skipline_prefix = 'Skipping'
filename_line_prefix = '----- FILE  :'
filename_line_suffix = '-----'
error_line_prefix = 'Line '
error_code_regex = 'E:\-?\d{3,4}:'

def convert(input, output):
    current_filename = False
    # write error list
    for line in input:
        if (is_skipping_line(line)):
            continue
        elif (is_filename_line(line)):
            current_filename = get_filename(line)
        elif (is_empty_line(line)):
            pass
        elif (is_error_line(line)):
            code_line_number = get_code_line_number(line)
            error_message = get_error_message(line)
            output.write('%s(%s) : error : %s\n' % (current_filename, code_line_number, error_message))
        else:
            break

def is_skipping_line(line):
    return 0 == line.find(skipline_prefix)


def is_empty_line(line):
    return '\n' == line


def is_filename_line(line):
    return 0 == line.find(filename_line_prefix)


def get_filename(line):
    filename = line
    filename = filename.replace(filename_line_prefix, '')
    filename = filename.replace(filename_line_suffix, '')
    filename = filename.strip()
    filename = os.path.abspath(filename)
    return filename


def is_error_line(line):
    return 0 == line.find(error_line_prefix)


def get_error_message(line):
    error_message_regex = error_code_regex + '(.*)$'
    matches = re.search(error_message_regex, line)
    message = matches.group(1)
    message = escape_xml_string(message)
    return message.strip()


def get_code_line_number(line):
    code_line_number_regex = error_line_prefix + '(\d+), ' + error_code_regex
    matches = re.search(code_line_number_regex, line)
    return matches.group(1).strip()


def escape_xml_string(string):
    string = string.replace('&', '&amp;')
    string = string.replace('"', '&quot;')
    string = string.replace('<', '&lt;')
    string = string.replace('>', '&gt;')
    return string


if __name__ == '__main__':
    convert(sys.stdin, sys.stdout)
