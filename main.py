#!/usr/bin/env python3

import argparse
import logging

from db.utils import persist

_version = "0.0.0"


class Command:
    pass



if __name__ == "__main__":
    # logging
    logger = logging.root
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # welcome message
    welcome = f"""
    Axie Scholar Tracker
    ====================
    """
    logger.info(welcome)


    # end
    logger.info("Goodbye.")