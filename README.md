# RejectionRadar

A script to detect job rejections from your Gmail inbox.

## Motivation

I've applied to lots of jobs.. easily in thousands by now. Anyway, I'm tired of
having my inbox flooded by rejections and wanted to create something that will
solve this problem for me.

![RejectonRadar GIF demo](https://i.imgur.com/2uL8lWS.gif)

## Problems I encounted

Gmail has a feature that allows incoming mail to be filtered. I used this feature
before starting the project, and realized that there were many limitation to the
Gmail query filter: there is a limit to the amount of keywords I can use, and
using too many keywords will produce incorrect results.

For example, I might get an email that happens to have the phrases "not
considered" and "unfortunately" but it can be anything-- not just related to job
search.

This is when I though about AI and how I can utilize it to read my emails and
determine if they are job-related rejections.

## How does it work?

1. A connection to the Google API is established using OAuth credentials.
1. The Gmail service is contacted.
1. Any new and unread emails are pulled. There is a default limit of the 10 most
   recent emails. This limit can be changed within the code.
1. Emails are parsed using BeautifulSoup to extract all the paragraphs within it.
1. A connection is established to OpenAI.
1. The emails pulled are fed into a function where GPT 3.5 will determine if an
   email is a job rejection.
1. Emails marked as "rejected" will have a label applied to them.

## Usage

To run the program, you will need

- a Google and OpenAI account,
- to create a [Google Cloud Application](https://cloud.google.com/docs) and
- generate an OpenAI API token.

Follow the steps in the Google Cloud documentation to create an application.
After creating your application, you'll receive a `credentials.json` file. You can
review `credentials.example.json` to see what `credentials.json` should look like.

Refer to the
[OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
documentation to get an API token. I have my OpenAI API
token loaded into an environment variable.

Install all the dependencies within the `requirements.txt` file.

## Project roadmap

Here's a project roadmap to see what's available:

- [x] Google API integration for Gmail authorization
- [x] OpenAI integration for AI usage
- [x] Job rejection status output
- [ ] Script may be ran as a CRON job for constant updates
- [ ] Indication of which emails are being processed
- [ ] Fetched mail and labels are cached locally to reduce wait times
