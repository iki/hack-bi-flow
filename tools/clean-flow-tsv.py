#!/usr/bin/env python

from __future__ import print_function
import re
import os
import sys
import glob

import langid

LF = '\n'

# Config

fieldNames = 'timestamp id title unknown url text source'.split()
requiredFieldNames = 'timestamp id text'.split()
replaceSepField = textField = fieldNames.index('text')
sep = '\t'
valid = re.compile('^\d+' + sep)
quote = '"'
replaceLF = ' '
replaceSep = ' '
appendEmptyFieldsUpTo = False # textField + 1
addHeader = True
skipHeader = False

updatedFieldNames = fieldNames
updateFields = False

'''
textField = fieldNames.index('text')
updatedFieldNames = fieldNames[:textField] + ['lang', 'lp'] + fieldNames[textField:]

def updateFields(fields):
  fields[textField:textField] = map(str, langid.classify(str(fields[textField])) if fields[textField] else ('', 0))
  return True
'''


# Init

totalFields = len(fieldNames)
requiredFields = dict(zip(map(fieldNames.index, requiredFieldNames), requiredFieldNames))


# Methods

def log(msg, flog = None):
  (flog or sys.stderr).write('{0}\n'.format(msg))

def error(msg, ferr = None):
  (ferr or sys.stderr).write('Error: {0}\n'.format(msg))

def check(line, lineNo = 0, ferr = None):
  fields = line.split(sep)
  count = len(fields)
  fixed = False

  for index in requiredFields:
    if index >= count or not fields[index]:
      error('Missing line {lineNo} field {field}: \'{line}\''.format(
        lineNo = lineNo, field = requiredFields[index], line = line), ferr)
      return None

  if count > totalFields:
    log('Join {count} - {total} = {joined} {name} fields on line {lineNo}: \'{line}\''.format(
      lineNo = lineNo, total = totalFields, count = count + 1, joined = count + 1 - totalFields, line = line,
      name = fieldNames[replaceSepField]), ferr)
    replaceToField = replaceSepField + count + 1 - totalFields
    fields[replaceSepField:replaceToField] = [replaceSep.join(fields[replaceSepField:replaceToField])]
    count = len(fields)
    fixed = True

  elif appendEmptyFieldsUpTo and count < appendEmptyFieldsUpTo:
    required = appendEmptyFieldsUpTo
    log('Append {required} - {count} = {added} empty fields on line {lineNo}: \'{line}\''.format(
      lineNo = lineNo, required = required, count = count, added = required - count, line = line), ferr)
    fields[count:count] = [''] * (required - count)
    count = len(fields)
    fixed = True

  for index, field in zip(range(count), fields):
    if field and (field is quote or field.startswith(quote) and not field.endswith(quote)):
      fields[index] += quote
      fixed = True
      log('End-quote field {name} on line {lineNo}: \'{field}\''.format(
        lineNo = lineNo, field = field, line = line, name = fieldNames[index]), ferr)

  if updateFields and updateFields(fields):
    fixed = True

  return sep.join(fields) if fixed else line

def write(fout, line, lineNo = 0, ferr = None):
  if line:
    line = check(line, lineNo, ferr)

    if line:
      fout.write(line + LF)
      return 1

  return 0

def files(masks, process):
  for mask in masks:
    files = glob.glob(mask)

    if not files:
      error('No files matching \'{0}\' found.'.format(mask))
      continue

    for infile in files:
      process(infile)

def process(infile):
  global skipHeader

  outfile = '{0}-clean{1}'.format(*os.path.splitext(infile))
  errfile = '{0}-error{1}'.format(*os.path.splitext(infile))

  with file(infile) as fin:
    with file(outfile, 'w') as fout:
      with file(errfile, 'w') as ferr:
        linesIn = linesOut = 0
        multiline = ''

        if addHeader:
          fout.write(sep.join(updatedFieldNames) + LF)

        for line in fin:
          if skipHeader:
            skipHeader = False
            continue

          if linesIn and not linesIn % 100000:
            print('{name}: {linesIn} -> {linesOut}'.format(name = outfile, linesIn = linesIn, linesOut = linesOut))

          linesIn += 1

          line = line.strip()

          if not line:
            continue

          if valid.match(line):
            linesOut += write(fout, multiline, linesIn, ferr)
            multiline = line

          elif multiline:
            multiline += replaceLF + line

          else:
            error('Invalid line {lineNo}: \'{line}\''.format(lineNo = linesIn, line = line))

        linesOut += write(fout, multiline, linesIn, ferr)

        print('{name}: {linesIn} -> {linesOut}'.format(name = outfile, linesIn = linesIn, linesOut = linesOut))


# Run

if __name__ == '__main__':
  files(sys.argv[1:], process)
