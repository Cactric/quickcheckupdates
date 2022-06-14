#!/usr/bin/python
# A python script to check for updates for an Arch Linux information by utilising Arch's RSS feeds
# This should result in less data needing to be downloaded, at the cost of a less complete update list

# Need the python-feedparser package
import feedparser
# argparse, from the standard library
import argparse

# You may want to change this to a different URL for an Arch-based distro or if you want to have this work with the testing repos (check https://archlinux.org/feeds)
# This default is for all stable repos, and all architectures
# This line just stores the default, you can use the --feed-url argument to change it
RSS_FEED_URL = "https://archlinux.org/feeds/packages/all/stable-repos/"

def main():
    parser = argparse.ArgumentParser(description="Quickly check for Arch Linux updates")
    parser.add_argument('--feed-url', help=f"URL of the feed you want to use, default is {RSS_FEED_URL} (all stable Arch repos)", dest="feed_url", type=str, default=RSS_FEED_URL)
    
    args = parser.parse_args()
    
    feed_url = args.feed_url
    print(f"feed url is {feed_url}")

if __name__ == '__main__':
    main()
