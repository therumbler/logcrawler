#!/usr/bin/env python3
"""kick it all off"""
from logcrawler.web import make_api

def main():
    api = make_api()
    api.run(port=9393)

if __name__ == "__main__":
    main()