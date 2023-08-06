#!/usr/bin/env python3
"""
Converst symlinks into text files
"""

import argparse
import os
from os import path

__author__ = "Owen T. Parkins"

BACKUP_EXT = ".symconv.bak"
CONVERTED_EXT = ".symconv.txt"



def convertLinkToFile(linkLocation, dryRun=True):
	# Sanity Check
	if path.islink(linkLocation) is False:
		return

	if dryRun:
		print("DRYRUN: " + linkLocation)
		return

	targetLocation = os.readlink(linkLocation)

	# Move file to backup location just in case the program gets interrupted
	os.rename(linkLocation, linkLocation + BACKUP_EXT)

	with open(linkLocation + CONVERTED_EXT, 'w') as f:
		f.write("# Symlink Convertor: https://github.com/oparkins/symlink-converter\n")
		f.write("# Run with --undo option to change all files to symlinks again\n")
		f.write("# Write comments with a '#' in the first character of a line.\n")
		f.write(targetLocation)

	# Delete backup link
	os.remove(linkLocation + BACKUP_EXT)

	print("Converted: " + linkLocation)


def convertFileToLink(fileLocation, dryRun=True):
	# Sanity Check
	splitPath1 = path.splitext(fileLocation)
	splitPath2 = path.splitext(splitPath1[0])

	if CONVERTED_EXT != splitPath2[1] + splitPath1[1]:
		return

	if dryRun:
		print("DRYRUN: " + fileLocation)
		return

	originalLocation = ""
	with open(fileLocation, 'r') as f:
		lines = f.readlines()
		for line in lines:
			if line[0] == '#':
				continue
			else:
				if originalLocation != "":
					print("FILE MALFORMED")
					return
				originalLocation = line

	# Backup file just in case
	os.rename(fileLocation, fileLocation + BACKUP_EXT)

	os.symlink(originalLocation, splitPath2[0])

	# Remove backup file
	os.remove(fileLocation + BACKUP_EXT)

	print("Converted: " + fileLocation)

def main(args):
	""" Main entry point of the app """
	for dirpath, dirnames, filenames in os.walk(args.target, followlinks=False):
		for filename in filenames:
			fullPath = path.join(dirpath, filename)
			if path.islink(fullPath) and args.undo is False:
				convertLinkToFile(fullPath, args.dry_run)
			if CONVERTED_EXT in filename and args.undo is True:
				convertFileToLink(fullPath, args.dry_run)
			
		# Only do top directory if not recursive
		if args.recursive is False:
			break


def parseArgs():
	parser = argparse.ArgumentParser(prog="symlinkConverter", description="Convert bad symlinks into rsync-able content")
	parser.add_argument('--dry-run', '-n', help="Just list files that would be changed", action="store_true")
	parser.add_argument('target', type=str, help="The directory to run in")
	parser.add_argument('--recursive', '-r', help="Run recursively", action="store_true")
	parser.add_argument('--undo', help="Turn text files into symlinks", action="store_true")
	return parser.parse_args()

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main(parseArgs())