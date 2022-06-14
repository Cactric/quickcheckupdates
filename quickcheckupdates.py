#!/usr/bin/python
# A python script to check for updates for an Arch Linux information by utilising Arch's RSS feeds
# This should result in less data needing to be downloaded, at the cost of a less complete update list

# Need the python-feedparser package
import feedparser
# Need the pyalpm package
from pyalpm import Handle
# argparse and os, from the standard library
import argparse, os

# You may want to change this to a different URL for an Arch-based distro or if you want to have this work with the testing repos (check https://archlinux.org/feeds)
# This default is for all stable repos, and all architectures
# This line just stores the default, you can use the --feed-url argument to change it
RSS_FEED_URL = "https://archlinux.org/feeds/packages/all/stable-repos/"

class DebugPrinter:
    _verbosity = 0
    
    def info(self, message, min_verbosity):
        if self._verbosity >= min_verbosity:
            print(message)
    
    # Prints a message so that it gets overwritten (an example is for a downloading feed message)
    # Make sure the next message is longer than this one, else part of it will be left on the terminal
    def transient(self, message, min_verbosity):
        if self._verbosity >= min_verbosity:
            print(message, end='\r', flush=True)
        
    
    def __init__(self, verbosity):
        self._verbosity = verbosity

def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Quickly check for Arch Linux updates (with some caveats)")
    parser.add_argument('--feed-url', help=f"URL of the feed you want to use, default is {RSS_FEED_URL} (all stable Arch repos)", dest="feed_url", type=str, default=RSS_FEED_URL)
    parser.add_argument('--verbose', '-v', action='count', default=0, help="Verbose output. May be specified multiple times for even more output")
    parser.add_argument('--quiet', '-q', dest="quiet", action="store_true", default=False, help="Don't output the packages - the return code will still be affected")
    parser.add_argument('--root', dest="rootdir", type=str, default="/")
    parser.add_argument('--dbpath', dest="dbpath", type=str, default="/var/lib/pacman")
    
    args = parser.parse_args()
    
    debug = DebugPrinter(args.verbose)
    
    feed_url = args.feed_url
    debug.info(f"Feed url is {feed_url}", 1)
    debug.info(f"Verbosity is {args.verbose}", 1)
    
    # The arguments have been parsed
    # Fetch the feed
    debug.transient("Fetching feed...\r",1)
    parsed_feed = feedparser.parse(feed_url)
    debug.info(f"Feed’s title is “{parsed_feed['feed']['title']}”",1)
    
    # Count number of entries
    debug.info(f"There are {len(parsed_feed.entries)} entries in this feed.", 1)
    
    alpm_handle = Handle(args.rootdir, args.dbpath)
    alpm_localdb = alpm_handle.get_localdb()
    
    pkg_names = []
    pkg_versions = []
    
    updated = []
    
    for package in alpm_localdb.pkgcache:
        pkg_names.append(package.name)
        pkg_versions.append(package.version)
    
    for entry in parsed_feed.entries:
        package_name, new_version, architecture = entry['title'].split()
        debug.info(f"Package: {package_name}, New version: {new_version}, Architecture: {architecture}", 2)
        # Checks if this updated package is installed
        try:
            index = pkg_names.index(package_name)
            if pkg_names.index(package_name) != 0:
                # If it is, check the version
                # For simplicity, just check if the version is different
                if new_version != pkg_versions:
                    updated.append((pkg_names[index], pkg_versions[index]))
        except ValueError: # from not having it installed
            continue
    
    # Got the list of updated things, now what to do with them?
    
    # If nothing, return 2 (like checkupdates)
    if len(updated) == 0:
        exit(2)
    
    for package in updated:
        if not args.quiet:
            print(package[0])

if __name__ == '__main__':
    main()
