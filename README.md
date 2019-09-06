# ApiDocs.co - Code Search Sample

### How Does it Work?

[Apidocs.co](https://apidocs.co) uses Github Code Search API against this repo to provide Code Samples directly within pages.

Because Github Code Search API is limited to single user or repo, this repository aggregates multiple relevant repos so they can all be searchable in a single request.

### Limitations

* It's plain text search - some generic names like `Application` can have lot's of false positives.
* It's limited to certain entity types (eg `Class`, `Method`, `Property`, etc)

### How to Contribute?

* Fork this repo
* Add a relevant repo to repos.json
* run `python update.py`
* Send a Pull Request


