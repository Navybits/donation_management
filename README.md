# Donation Management
Donation management is an Odoo module that handles the donation management between sponsors and beneficiaries. The goal of this module is to create the missing links between Odoo profit accounting and the non-profit accounting.

## Purpose
The purpose of this module was to create a simpler interface for the donation process within the charity organizations, not necessarily having a base knowledge in accounting processes or how odoo works with accounting internally.

You can read more in my blog post on medium here: https://blog.navybits.com/non-profit-acounting-challenge-in-odoo-10-0-9f0fe7b73d57

### Prerequisites

The modules _Accounting and Finance_ and _Invoicing_ are required for this module works. By default, since there's a dependancy between those modules in the `manifest.py` file, they should be installed automatically within the installation.

### Installation

1. Copy the module to the addons folder
2. Update Apps list (_developer mode should be activated_)
3. Install the module
4. Activate Analytic account in Accounting

## Known Issues

This module is still in developement, so there is bugs here and there, it is not complete yet, but i think there is information  in it that worth spreading, since there is a little documentation on Odoo 10

## Built with

- [Sublime Text](https://www.sublimetext.com) - The text editor
- [FileZilla](https://filezilla-project.org) - To upload the files when editing them, i was working remotely with the files

## Authors

- **AbdelRahman Sanjekdar** - [AbdelRahmanSnjk](https://github.com/AbdelRahmanSnjk)

## Acknowledgments

- Ton of thanks to NavyBits for giving me the oppurtinity to be able to host my first real project online on GitHub.
- Special thanks to Mr. [Hassan Tabbal](http://www.hassantabbal.com) for his constant guidance and instructions on my tasks and for his insight on how Accounting works.
