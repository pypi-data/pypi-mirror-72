# Changelog

Here we list the history of changes in remo across the various releases.


## Coming up in the next releases

This is what we plan to work on next. If you have any feedback or preference, we would love to hear them in our support forum.

**Improved dataset experience**

- list view for images details
- folders to organise your images
- sticky bar for easier exploration of data


**More options around export of data**

- option to export list of Classes and empty annotation files (for images without annotations)
- ability to download datasets


**Increase supported Computer Vision tasks**

- pose estimation
- keypoints
- support for videos

**Code level: faster processing and robustness**

- switching to FastAPI
- increase test coverage

---

## v0.4.8 - 28 Jun 20

* Fixed postgres installation issue

---

## v0.4.7 - 26 Jun 20

Most of the work on this release has been around annotations upload and export.
We are adding the ability to upload and export tags, and some nice convenience functions for annotation exporting.

* ability to add and export tags

* export annotations: functionality to include or exclude images with no annotations

* export annotations: option to append paths to filenames

* more clear counting on annotation statistics in Annotations Tab: now displaying annotated as the count of images actual having annotations

* removing truncation for long filename on dataset page

---

## v0.4.5 - 19 Jun 20

We are introducing a check for the latest version on command line, particularly useful given we are iterating quite fast.

We also fixed some small reported bugs:


* installation issues with PostgresSQL on Windows

* installation script to use pip3 instead of pip when python 2 is installed

* sort by TODO in annotation page occasionally not working

---

## v0.4.4 - 09 Jun 20

Cosmetic changes to address links behaviour and formatting in documentation and discuss forum


---
## v0.4.3 - 04 Jun 20

Some small changes:

* Fixed bug with upload folder when using electron
* Added license page

---
## v0.4.2 - 03 Jun 20

Some quick fixes post the bigger release:

* CSS on loading bar
* demo access occasional login fail
* handling of tags: now it's case insensitive

---
## v0.4.1 - 29 May 20

**Main Changes**

Most of the work has been about introducing a notification system to inform on progress for images and annotation uploading and parsing, including a detailed breakdown of any error. Nothing fancy, but a great improvement to reliability of the app.

We also expanded the Command Line Interface, allowing for more options (such as kill remo, delete datasets), and simplified the connection between the sdk and the remo server.

For the rest, we completed a series of smaller UX-driven changes to improve usability (including showing selected annotation sizes) and fixed few reported bugs.

**Breakdown**

Bug fixes:

* Delete all images from dataset causes error
* Delete an image and re-upload it: should be allowed
* Up-to-date count of images after fast deleting
* Fix download latest available electron app

Changes:

* Notification system for data upload. You can now monitor the upload of data and get a breakdown of errors that occur.
* Expanded Command Line Interface suit of options
* SDK: rework the connection with remo app and introduce clear option to connect to a remote remo server. "import remo" in conda now does not launch the server
* Annotation tool, delete object: ask for confirmation
* Image view and Annotation tool - objects height and width information

---
## v0.3.42 - 19 May 20

Quick fix to handle directories with space within their name

* Edited installation scripts to handle folder names containing a space e.g. 'C:/remo ai/script'

---

## v0.3.41 - 8 May 20

**Main Changes**

Switched to PostgresSQL for database management, instead of SQLlite. This makes the whole app more responsive and reliable.
For the rest, we implemented a number of small fixes aimed at making making remo more robust

**Breakdown**

Bug fixes:

* Fixed annotation statistics inconsistencies for image classification
* Fixed sending feedback form
* Fixed autologin in browser, and in electron after user changes password
* Fixed rename annotation set
* Fixed export annotation form - missing annotation set name
* Fixed Windows installation in conda env - pip failed to install package
* Fixed duplicate annotation objects

Changes:

* Added support for PostgresSQL as main database
* Improved duplicate annotation set flow
* After annotations uploaded - images marked as annotated
* Improved create annotation set flow
* Improved save annotations behaviour
* Improved data uploading and parsing - moved it to a separate process, which allows to use remo while long uploads are in progress
* Added ability to bulk delete annotations for an image in annotation tool
* Added ability to mark image as TODO in annotation tool
* Improved description of installation steps. Also we are now asking user for explicit permission to install PostgresSQL and additional packages
